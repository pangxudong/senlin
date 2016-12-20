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

from senlin.drivers import base
from senlin.drivers.openstack import sdk


class MistralClient(base.DriverBase):
    '''Mistral V2 driver.'''

    def __init__(self, params):
        super(MistralClient, self).__init__(params)
        self.conn = sdk.create_connection(params)
        self.session = self.conn.session

    @sdk.translate_exception
    def workflow_create(self, **attrs):
        return self.conn.workflow.create_workflow(**attrs)

    @sdk.translate_exception
    def workflow_delete(self, workflow, ignore_missing=True):
        return self.conn.workflow.delete_workflow(workflow, ignore_missing)

    @sdk.translate_exception
    def workflow_get(self, *attrs):
        return self.conn.workflow.get_workflow(*attrs)

    @sdk.translate_exception
    def execution_create(self, workflow_name, **attrs):
        return self.conn.workflow.create_execution(workflow_name, **attrs)

    @sdk.translate_exception
    def execution_delete(self, workflow_name, execution,
                            ignore_missing=True):
        return self.conn.workflow.delete_execution(workflow_name, execution,
                                                     ignore_missing)
    @sdk.translate_exception
    def execution_get(self, *attrs):
        return self.conn.workflow.get_execution(*attrs)
