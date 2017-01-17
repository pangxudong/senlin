"""
FilterVmAction - custom action.

Simple action for filtering VM on the presence of metadata "cluster_id"
"""
from mistral.actions.openstack.actions import NovaAction
from mistral.workflow.utils import Result


class FilterVmException(Exception):
    pass


class FilterVmAction(NovaAction):
    """
    Filter and return VMs whith the flag 'cluster_id' either on vm metadtata.
    """

    def __init__(self, metadata, flavor, uuid, cluster_id, node_id):
        """init."""
        self._metadata = metadata
        self._flavor = flavor
        self._uuid = uuid
        self._cluster_id = cluster_id
        self._node_id = node_id

    def run(self):
        """Entry point for the action execution."""
        client = self._get_client()
        metadata = self._metadata

        if str(metadata.get('cluster_id')) == str(self._cluster_id):
            if str(self._uuid) == str(self._node_id):
                hypervisor_hostname = client.servers.find(id=self._uuid).to_dict()['OS-EXT-SRV-ATTR:hypervisor_hostname']
                return Result(data={'migrate': True, 'uuid': self._uuid, 'hypervisor_hostname': hypervisor_hostname})

        return Result(data={'migrate': False, 'uuid': self._uuid, 'hypervisor_hostname': ""})
