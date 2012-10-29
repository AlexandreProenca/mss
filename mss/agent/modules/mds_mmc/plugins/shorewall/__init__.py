#
# (c) 2012 Mandriva, http://www.mandriva.com
#
# This file is part of Mandriva Management Console (MMC).
#
# MMC is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# MMC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MMC.  If not, see <http://www.gnu.org/licenses/>.
#

"""
MDS shorewall plugin for the MMC agent.
"""

import os
import glob

from mmc.core.version import scmRevision
from mmc.plugins.shorewall.io import ShorewallConf

VERSION = "2.4.3"
APIVERSION = "6:2:4"
REVISION = scmRevision("$Rev$")

def getVersion(): return VERSION
def getApiVersion(): return APIVERSION
def getRevision(): return REVISION

def activate():
    return True


class ShorewallZones(ShorewallConf):

    def __init__(self):
        ShorewallConf.__init__(self, '/etc/shorewall/zones',
                               r'^(?P<name>[\w\d]+)\s+(?P<type>[\w\d]+)')
        self.read()

    def get(self, type = ""):
        zones = []
        for line in self.get_conf():
            if line[0].startswith(type):
                zones.append(line[0])
        return zones


class ShorewallRules(ShorewallConf):

    def __init__(self):
        ShorewallConf.__init__(self, '/etc/shorewall/rules',
            r'^(?P<action>[\w\d/]+)\s+(?P<src>[\w\d:.]+)\s+(?P<dst>[\w\d:.]+)\s*(?P<proto>[\w\d]*)\s*(?P<dst_port>[:\w\d]*)')
        self.read()

    def add(self, action, src, dst, proto = "", dst_port = ""):
        action = action.split('/')
        if len(action) == 2:
            if not os.path.exists(os.path.join('/usr', 'share', 'shorewall', 'macro.%s' % action[1])) and \
               not os.path.exists(os.path.join('/etc', 'shorewall', 'macro.%s' % action[1])):
                raise ShorewallMacroDoesNotExists("Macro %s does not exists" % action[1])
        action = "/".join(action)
        self.add_line([action, src, dst, proto, dst_port])

    def delete(self, action, src, dst, proto = "", dst_port = ""):
        self.del_line([action, src, dst, proto, dst_port])

    def get(self, action = "", src = "", dst = "", filter = ""):
        rules = []
        for line in self.get_conf():
            use = True
            if action and action not in line[0]:
                use = False
            if src and src not in line[1]:
                use = False
            if dst and dst not in line[2]:
                use = False
            if use:
                rules.append(line)
        return rules


class ShorewallPolicies(ShorewallConf):

    def __init__(self):
        ShorewallConf.__init__(self, '/etc/shorewall/policy',
            r'^(?P<src>[\w]+)\s+(?P<dst>[\w]+)\s+(?P<policy>ACCEPT|DROP|REJECT)\s*(?P<log>[\w]*)')
        self.read()

    def get(self, src, dst, filter = ""):
        policies = []
        for line in self.get_conf():
            use = True
            if src and src not in line[0]:
                use = False
            if dst and dst not in line[1]:
                use = False
            if use:
                policies.append(line)
        return policies

    def change(self, src, dst, policy, log = ""):
        policies = self.get(src, dst)
        if policies:
            for p in policies:
                old = p[:]
                new = list(p[:])
                new[2] = policy
                new[3] = log
                self.replace_line(old, new)
            self.write()
            return True
        return False

class ShorewallMasq(ShorewallConf):

    def __init__(self):
        ShorewallConf.__init__(self, '/etc/shorewall/masq',
            r'^(?P<lan_if>[\w]+)\s+(?P<wan_if>[\w]+)')
        self.read()

    def get(self):
        return self.get_conf()

    def add(self, wan_if, lan_if):
        return self.add_line([wan_if, lan_if])
    
    def delete(self, wan_if, lan_if):
        return self.del_line([wan_if, lan_if])


class ShorewallInterfaces(ShorewallConf):

    def __init__(self):
        ShorewallConf.__init__(self, '/etc/shorewall/interfaces',
            r'^(?P<zone>[\w]+)\s+(?P<if>[\w]+)')
        self.read()

    def get(self, type = ""):
        zones = []
        for line in self.get_conf():
            if line[0].startswith(type):
                zones.append(line)
        return zones


class ShorewallMacroDoesNotExists(Exception):
    pass

# XML-RPC methods
def get_zones(type = ""):
    return ShorewallZones().get(type)

def get_zones_interfaces(type = ""):
    return ShorewallInterfaces().get(type)

def add_rule(action, src, dst, proto = "", dst_port = ""):
    return ShorewallRules().add(action, src, dst, proto, dst_port)

def del_rule(action, src, dst, proto = "", dst_port = ""):
    return ShorewallRules().delete(action, src, dst, proto, dst_port)

def get_rules(action = "", src = "", dst = "", filter = ""):
    return ShorewallRules().get(action, src, dst, filter)

def get_services():
    services = [ os.path.basename(m)[6:] for m in glob.glob('/usr/share/shorewall/macro.*') ] + \
               [ os.path.basename(m)[6:] for m in glob.glob('/etc/shorewall/macro.*') ]
    services.sort()
    return services

def get_policies(src = "", dst = "", filter = ""):
    return ShorewallPolicies().get(src, dst, filter)

def change_policies(src, dst, policy, log = ""):
    return ShorewallPolicies().change(src, dst, policy, log)

def get_masquerade_rules():
    return ShorewallMasq().get()

def del_masquerade_rule(wan_if, lan_if):
    return ShorewallMasq().delete(wan_if, lan_if)

def add_masquerade_rule(wan_if, lan_if):
    return ShorewallMasq().add(wan_if, lan_if)
