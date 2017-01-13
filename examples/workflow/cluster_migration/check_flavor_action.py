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

            mem  = limits_dict['memory_mb'] - flavor_dict['ram']
            disk = limits_dict['free_disk_gb'] - flavor_dict['disk']
            vcpu = limits_dict['vcpus']-(limits_dict['vcpus_used'] - flavor_dict['vcpus']

            if ((mem) || () ):
                sys.exit("hypervisor resource shortage for this flavor!")
