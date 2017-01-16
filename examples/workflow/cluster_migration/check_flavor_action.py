import sys
from mistral.actions.openstack.actions import NovaAction

# check hypervisor free resource to allocate for a instance of the flavor type
class CheckFlavorAction(NovaAction):

    def __init__(self, migrate, hypervisor_hostname, flavor_id):
        self._flavor_id = flavor_id
        self._hypervisor_hostname = hypervisor_hostname
        self._migrate = migrate

    def run(self):
        client = self._get_client()

        if self._migrate:
            flavor_dict = client.flavors.find(id=str(self._flavor_id)).to_dict()
            limits_dict = client.hypervisors.find(hypervisor_hostname=self._hypervisor_hostname).to_dict()

            mem = limits_dict['memory_mb'] - flavor_dict['ram']
            disk = limits_dict['free_disk_gb'] - flavor_dict['disk']
            vcpus = (limits_dict['vcpus']-limits_dict['vcpus_used']) - flavor_dict['vcpus']#vcpu could be over used?

            if ((mem<0) or (disk<0) or (vcpus<0)):
                sys.exit("hypervisor resource shortage for allocating this flavor!")
