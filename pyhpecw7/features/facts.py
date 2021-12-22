"""Gather device facts on HPCOM7 devices.
"""
import collections
from pyhpecw7.utils.xml.lib import *


class Facts(object):
    """Gather device facts from a HP Comware 7 device.

    Args:
        device (HPCOM7): connected instance of a ``pyhpecw7.comware.HPCOM7``
            object.

    Attributes:
        device (HPCOM7): connected instance of a ``pyhpecw7.comware.HPCOM7``
            object.
        facts (dict): this is a read-only attribute. Details can be seen
            in ``get_facts``.

    """
    def __init__(self, device):
        self.device = device
        self.em = data_element_maker()

    @property
    def facts(self):
        return self.get_facts()

    def get_facts(self):
        """Gather facts from the HP Comware 7 device

        Returns:
            This returns a dictionary with several key/value
            pairs describing the device.  See example below.

            Example::

                {
                    'hostname': 'HP5930_1',
                    'interface_list': ["FortyGigE1/0/1", "FortyGigE1/0/2",
                        "FortyGigE1/0/3", "FortyGigE1/0/4"],
                    'localtime': '2016-01-30T01:47:07',
                    'model': 'HP FF 5930-32QSFP+ Switch',
                    'os': '7.1.045 Release 2418P01',
                    'serial_number': 'CN43G9800T',
                    'uptime': '6d 23hr 25min 18sec',
                    'vendor': 'hp',
                    'hardware': 'Ver.A'
                }
        """

        facts = collections.OrderedDict()
        facts.update(self._get_inventory())
        facts.update(self._get_base())
        facts.update(self._get_interface_list())

        return facts

    def _get_interface_list(self):
        """Get interface list that will be added to facts.
        """
        E = self.em
        top = E.top(
                E.Ifmgr(
                    E.Interfaces(
                        E.Interface(
                            E.Name()
                        )
                    )
                )
            )

        nc_get_reply = self.device.get(('subtree', top))

        intfs_xml = findall_in_data('Name', nc_get_reply.data_ele)
        interfaces = [intf.text for intf in intfs_xml]
        intfs = dict(interface_list=interfaces)

        return intfs

    def _get_uptime(self, seconds):
        """Convert seconds to d, hr, min, sec format.
        """
        m, s = divmod(int(seconds), 60)
        h, m = divmod(m, 60)
        d = 0
        if h > 23:
            d, h = divmod(h, 24)
        uptime = '{0}d {1}hr {2}min {3}sec'.format(d, h, m, s)

        return uptime

    def _get_inventory(self):
        """Get os, serial number, and model that will be added to facts.
        """
        key_map = {
            'os': 'SoftwareRev',
            'serial_number': 'SerialNum',
            'model': 'ModelName',
            'hardware': 'HardwareRev'
        }

        E = self.em
        top = E.top(
            E.LLDP(
                E.Inventory(
                    E.SoftwareRev(),
                    E.SerialNum(),
                    E.ModelName(),
                    E.HardwareRev(),

                )
            )
        )
        nc_get_reply = self.device.get(('subtree', top))

        inventory = data_elem_to_dict(nc_get_reply.data_ele, key_map)
        inventory['vendor'] = 'hp'

        return inventory

    def _get_base(self):
        """Get hostname, localtime, and uptime that will be added to facts.
        """
        key_map = {
            'hostname': 'HostName',
            'localtime': 'LocalTime',
            'uptime': 'Uptime'
        }

        E = self.em
        top = E.top(
            E.Device(
                E.Base(
                    E.HostName(),
                    E.LocalTime(),
                    E.Uptime(),
                )
            )
        )
        nc_get_reply = self.device.get(('subtree', top))

        basefacts = data_elem_to_dict(nc_get_reply.data_ele, key_map)
        basefacts['uptime'] = self._get_uptime(basefacts.get('uptime', 0))

        return basefacts
