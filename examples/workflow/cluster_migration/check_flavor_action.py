import sys
from mistral.actions.openstack.actions import NovaAction

# check hypervisor free resource to allocate for a instance of the flavor type
class CheckFlavorAction(NovaAction):

    def __init__(self, migrate, hostname, flavor_id):
        self._flavor_id = flavor_id
        self._hostname = hostname
        self._migrate = migrate

    def run(self):
        client = self._get_client()

        if self._migrate:
            flavor_dict = client.flavors.find(id=str(self._flavor_id)).to_dict()
            limits_dict = client.hypervisors.find(hypervisor_hostname=self._hostname).to_dict()
            # if (server.flavor['id'] != str(self._flavor_id)):
            #     sys.exit("flavor not correct!")
