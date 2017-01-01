# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import json
import six

from senlin.common import exception
from senlin.drivers import base as driver_base
from senlin.common import constraints
from senlin.common import consts
from senlin.common.i18n import _
from senlin.common import schema
from senlin.engine import health_manager
from senlin.policies import base


class HealthPolicy(base.Policy):
    '''Policy for health management of a cluster.'''

    VERSION = '1.0'

    PRIORITY = 600

    TARGET = [
        ('BEFORE', consts.CLUSTER_CHECK),
        ('BEFORE', consts.CLUSTER_RECOVER),
    ]

    # Should be ANY if profile provides health check support?
    PROFILE_TYPE = [
        'os.nova.server',
        'os.heat.stack',
    ]

    KEYS = (DETECTION, RECOVERY) = ('detection', 'recovery')

    _DETECTION_KEYS = (
        DETECTION_TYPE, DETECTION_OPTIONS,
    ) = (
        'type', 'options'
    )

    DETECTION_TYPES = (
        VM_LIFECYCLE_EVENTS, NODE_STATUS_POLLING, LB_STATUS_POLLING,
    ) = (
        'VM_LIFECYCLE_EVENTS', 'NODE_STATUS_POLLING', 'LB_STATUS_POLLING',
    )

    _DETECTION_OPTIONS = (
        DETECTION_INTERVAL,
    ) = (
        'interval',
    )

    _RECOVERY_KEYS = (
        RECOVERY_ACTIONS, RECOVERY_FENCING
    ) = (
        'actions', 'fencing'
    )

    RECOVERY_ACTION_VALUES = (
        REBOOT, REBUILD, MIGRATE, EVACUATE, RECREATE, WORKFLOW, NOP
    ) = (
        'REBOOT', 'REBUILD', 'MIGRATE', 'EVACUATE', 'RECREATE', 'WORKFLOW', 'NOP',
    )

    FENCING_OPTION_VALUES = (
        COMPUTE, STORAGE, NETWORK,
    ) = (
        'COMPUTE', 'STORAGE', 'NETWORK'
    )

    ACTION_KEYS = (
        ACTION_NAME, ACTION_TYPE, ACTION_PARAMS,
    ) = (
        'name', 'type', 'params',
    )

    properties_schema = {
        DETECTION: schema.Map(
            _('Policy aspect for node failure detection.'),
            schema={
                DETECTION_TYPE: schema.String(
                    _('Type of node failure detection.'),
                    constraints=[
                        constraints.AllowedValues(DETECTION_TYPES),
                    ],
                    required=True,
                ),
                DETECTION_OPTIONS: schema.Map(
                    schema={
                        DETECTION_INTERVAL: schema.Integer(
                            _("Number of seconds between pollings. Only "
                              "required when type is 'NODE_STATUS_POLLING'."),
                            default=60,
                        ),
                    }
                ),
            },
            required=True,
        ),
        RECOVERY: schema.Map(
            _('Policy aspect for node failure recovery.'),
            schema={
                RECOVERY_ACTIONS: schema.List(
                    _('List of actions to try for node recovery.'),
                    schema=schema.Map(
                        _('Action to try for node recovery.'),
                        schema={
                            ACTION_NAME: schema.String(
                                _("Name of action to execute."),
                                constraints=[
                                    constraints.AllowedValues(
                                        RECOVERY_ACTION_VALUES),
                                ],
                                required=True
                            ),
                            ACTION_TYPE: schema.String(
                                _("Type of action to execute."),
                                constraints=[
                                    constraints.AllowedValues(
                                        RECOVERY_ACTION_VALUES),
                                ],
                            ),
                            ACTION_PARAMS: schema.Map(
                                _("Parameters for the action")
                            ),
                        }
                    )
                ),
                RECOVERY_FENCING: schema.List(
                    _('List of services to be fenced.'),
                    schema=schema.String(
                        _('Service to be fenced.'),
                        constraints=[
                            constraints.AllowedValues(FENCING_OPTION_VALUES),
                        ],
                        required=True,
                    ),
                ),
            }
        ),
    }

    def __init__(self, name, spec, **kwargs):
        super(HealthPolicy, self).__init__(name, spec, **kwargs)

        self.check_type = self.properties[self.DETECTION][self.DETECTION_TYPE]
        options = self.properties[self.DETECTION][self.DETECTION_OPTIONS]
        self.interval = options[self.DETECTION_INTERVAL]
        recover_settings = self.properties[self.RECOVERY]
        self.recover_actions = recover_settings[self.RECOVERY_ACTIONS]
        self._workflowclient = None

    def do_workflow(self, obj, cluster, workflow_name, **params):
        if not obj.physical_id:
            return False

        self.server_id = obj.physical_id
        wfc = self.workflow(cluster)
        def_path = params.pop('definition')
        input_dict = {
            'cluster_id': obj.cluster_id,
            'node_id': obj.physical_id,
        }
        input_dict.update(params)

        try:
            workflow = wfc.workflow_find(workflow_name)
            if workflow is None:
                definition = open(def_path, 'r').read()
                wfc.workflow_create(definition, scope="private")

            input_str = json.dumps(input_dict)

            wfc.execution_create(workflow_name, input_str)
        except exception.InternalError as ex:
            raise exception.EResourceUpdate(type='server', id=obj.physical_id,
                                      message=six.text_type(ex))

        return self.server_id

    def workflow(self, cluster):
            if self._workflowclient is not None:
                return self._workflowclient
            params = self._build_conn_params(cluster)
            self._workflowclient = driver_base.SenlinDriver().workflow(params)
            return self._workflowclient

    def attach(self, cluster):
        """"Hook for policy attach.

        Register the cluster for health management.
        """

        kwargs = {
            'check_type': self.check_type,
            'interval': self.interval,
            'params': {},
        }

        health_manager.register(cluster.id, engine_id=None, **kwargs)

        data = {
            'check_type': self.check_type,
            'interval': self.interval,
        }
        for node in cluster.nodes:
            if node.status == 'ACTIVE':
                continue
            workflow_name = self.recover_actions[0]['name']
            params = self.recover_actions[0]['params']
            self.do_workflow(node, cluster, workflow_name, **params)

        return True, self._build_policy_data(data)

    def detach(self, cluster):
        '''Hook for policy detach.

        Unregister the cluster for health management.
        '''

        health_manager.unregister(cluster.id)
        return True, ''

    def pre_op(self, cluster_id, action, **args):
        # Ignore actions that are not required to be processed at this stage
        if action.action != consts.CLUSTER_RECOVER:
            return True

        pd = {
            'recover_action': self.recover_actions[0],
        }
        action.data.update({'health': pd})
        action.store(action.context)

        return True

    def post_op(self, cluster_id, action, **args):
        # Ignore irrelevant action here
        if action.action not in (consts.CLUSTER_CHECK,
                                 consts.CLUSTER_RECOVER):
            return True

        # TODO(anyone): subscribe to vm-lifecycle-events for the specified VM
        #               or add vm to the list of VM status polling
        return True
