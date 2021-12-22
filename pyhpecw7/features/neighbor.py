"""Gather LLDP neighbor information from HPCOM7 devices.
"""
from lxml import etree
from ncclient.xml_ import qualify
from pyhpecw7.utils.xml.namespaces import HPDATA, HPDATA_C
from pyhpecw7.utils.xml.lib import *


class Neighbors(object):
    """Gather LLDP neighbor information from a HP COM7 switch.

    Args:
        device (HPCOM7): connected instance of a ``pyhpecw7.comware.HPCOM7``
            object.

    Attributes:
        device (HPCOM7): connected instance of a ``pyhpecw7.comware.HPCOM7``
            object.
        lldp (lldp): dictionary containing LLDP neighbors
        cdp (cdp): dictionary containing CDP neighbors

    """
    def __init__(self, device):

        self.device = device

        self.lldp = self._get_neighbors(ntype='lldp')
        self.cdp = self._get_neighbors(ntype='cdp')

    def _get_interface_from_index(self, index):
        """ Returns interface name based on a given ifindex
        """
        E = data_element_maker()
        top = E.top(
            E.Ifmgr(
                E.Interfaces(
                    E.Interface(
                        E.IfIndex(index),
                        E.Name()
                    )
                )
            )
        )
        nc_get_reply = self.device.get(('subtree', top))
        interface_name = find_in_data('Name', nc_get_reply.data_ele).text

        return interface_name

    def refresh(self):
        """Refreshes the "ldp" and "cdp" attributes of the class
        """

        self.lldp = self._get_neighbors(ntype='lldp')
        self.cdp = self._get_neighbors(ntype='cdp')

    def _get_neighbors(self, ntype='lldp'):
        """Gets neighbors of device (HPCOM7)

            Args:
                ntype (str): must be "lldp" or "cdp"

            Returns:
                List of dicts with the following k/v pairs:
                    :local_intf (str): local interface of HP device
                    :neighbor_intf (str): remote interface of the neighbor
                        device
                    :neighbor (str): hostname of the neighbor device for lldp
                        and mgmt IP addr when cdp
        """
        E = data_element_maker()
        if ntype == 'cdp':
            top = E.top(
                E.LLDP(
                    E.CDPNeighbors(
                        E.CDPNeighbor()
                    )
                )
            )
        else:
            top = E.top(
                E.LLDP(
                    E.LLDPNeighbors(
                        E.LLDPNeighbor()
                    )
                )
            )

        nc_get_reply = self.device.get(('subtree', top))
        return self._build_response(nc_get_reply.data_ele, ntype=ntype)

    def _build_response(self, nc_reply, ntype='lldp'):
        """Builds dictionary from XML response coming from device

        Args:
            nc_reply (lxml.etree._Element): NETCONF
                response from device as etree element

        Returns:
            It returns a list of dictionary objects and each neighbor
            is represented as a dictionary object with the following k/v
            pairs:
                :local_intf (str): local interface of HP device
                :neighbor_intf (str): remote interface of the neighbor
                    device
                :neighbor (str): hostname of the neighbor device for lldp
                    and mgmt IP addr when cdp
        """

        if ntype == 'lldp':
            key_map = {
                'neighbor': 'SystemName',
                'neighbor_intf': 'PortId',
            }
            neighbors = findall_in_data('LLDPNeighbor', nc_reply)
        else:
            key_map = {
                'neighbor': 'ManageAdress',
                'neighbor_intf': 'PortId',
            }
            neighbors = findall_in_data('CDPNeighbor', nc_reply)

        return_neigh = []

        for neigh in neighbors:
            temp = {}
            index = find_in_data('IfIndex', neigh).text
            interface = self._get_interface_from_index(index)
            temp['local_intf'] = interface
            for new_key, xml_tag in key_map.items():
                obj = find_in_data(xml_tag, neigh)
                if obj is not None:
                    value = obj.text
                    temp[new_key] = value
            return_neigh.append(temp)

        return return_neigh
