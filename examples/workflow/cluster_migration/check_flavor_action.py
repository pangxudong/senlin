import sys
from mistral.actions.openstack.actions import NovaAction


class CheckFlavorAction(NovaAction):

    def __init__(self, tenant_id, flavor_id):
        self._flavor_id = flavor_id
        self._tenant_id= tenant_id

    def run(self):
        client = self._get_client()

        if self._migrate:
            quota = client.quotas.find(tenant_id = self._tenant_id)
            usage = client.usage.get(tenant_id = self._tenant_id)
            flavor = client.flavors.find(id=self._flavor_id)
            # if (server.flavor['id'] != str(self._flavor_id)):
            #     sys.exit("flavor not correct!")
