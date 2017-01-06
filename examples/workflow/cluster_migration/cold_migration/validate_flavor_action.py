import sys
from mistral.actions.openstack.actions import NovaAction


class ValidateFlavorAction(NovaAction):

    def __init__(self, migrate, uuid, flavor_id):
        self._flavor_id = flavor_id
        self._migrate = migrate
        self._uuid= uuid

    def run(self):
        client = self._get_client()

        if self._migrate:
            server = client.servers.find(id=self._uuid)
            if (server.flavor['id'] != str(self._flavor_id)):
                sys.exit("flavor not correct!")
