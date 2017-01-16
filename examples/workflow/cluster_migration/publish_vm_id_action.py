from mistral.actions.openstack.actions import NovaAction
from mistral.workflow.utils import Result


class PublishVmIdAction(NovaAction):

    def __init__(self, migrate, uuid):
        self._migrate = migrate
        self._uuid= uuid

    def run(self):
        client = self._get_client()

        if self._migrate:
            return Result(data={self._uuid})
