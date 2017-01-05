from mistral.actions.openstack.actions import NovaAction
from mistral.workflow.utils import Result

class ValidateFlavorAction(NovaAction):

    def __init__(self, migrate, flavor_id):
        self._flavor_id = flavor_id
        self._migrate = migrate

    def run(self):
        client = self._get_client()

        if self._migrate:
            client.servers.find(id=self._uuid, flavor=self._flavor_id)
