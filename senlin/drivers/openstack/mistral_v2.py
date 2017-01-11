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
    def workflow_create(self, definition, scope):
        attrs = {
            'definition':definition,
            'scope':scope
        }
        return self.conn.workflow.create_workflow(**attrs)

    @sdk.translate_exception
    def workflow_delete(self, value, ignore_missing=True):
        return self.conn.workflow.delete_workflow(value, ignore_missing=ignore_missing)

    @sdk.translate_exception
    def workflow_find(self, name_or_id):
        return self.conn.workflow.find_workflow(name_or_id, ignore_missing=True)

    @sdk.translate_exception
    def execution_create(self, workflow_name, input):
        attrs = {
            'workflow_name':workflow_name,
            'input':input
        }
        return self.conn.workflow.create_execution(**attrs)

    @sdk.translate_exception
    def execution_delete(self, value, ignore_missing=True):
        return self.conn.workflow.delete_execution(value, ignore_missing=ignore_missing)

    @sdk.translate_exception
    def execution_find(self, name_or_id):
        return self.conn.workflow.find_execution(name_or_id, ignore_missing=True)
