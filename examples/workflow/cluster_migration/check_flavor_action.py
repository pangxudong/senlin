import sys
from mistral.actions.openstack.actions import NovaAction


class CheckFlavorAction(NovaAction):

    def __init__(self, migrate, tenant_id, flavor_id):
        self._flavor_id = flavor_id
        self._tenant_id= tenant_id
        self._migrate= migrate

    def run(self):
        client = self._get_client()

        if self._migrate:
            flavor_dict = client.flavors.find(id=self._flavor_id).to_dict()
            limits_dict = client.limits.get().absolute
            # if (server.flavor['id'] != str(self._flavor_id)):
            #     sys.exit("flavor not correct!")
