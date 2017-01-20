from mistral.actions.openstack.actions import NovaAction
import time

class ColdMigrateVmAction(NovaAction):

    def __init__(self, uuid, migrate, flavor_id):
        self._uuid = uuid
        self._flavor_id = flavor_id
        self._migrate = migrate

    def run(self):
        client = self._get_client()

        if self._migrate:
            client.servers.resize(self._uuid, flavor=self._flavor_id)
