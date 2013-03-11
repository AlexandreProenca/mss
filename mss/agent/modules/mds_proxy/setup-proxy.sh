#!/bin/bash
# Copyright Mandriva S/A all rights reserved
# This file is part of Mandriva Server Setup
#
# MSS is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# MSS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MSS; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.
# ######################   Description of this program  ###################################
#
#  This program basically does 5 things
#  * backup squid configuration file squid.conf
#  * query existing settings in the base.ini file generated by MDS installer and
#  configure the template files with the information collected
#  *creates 3 new user groups in LDAP base
#  *replace original files for templates files
#  *restart squid and validates installation
# Autor: Alexandre Proença - alexandre@mandriva.com.br | linuxloco@gmail.com
#        Jean-Philippe Braun - jpbraun@mandriva.com
# Date: 10/08/2012

. '../functions.sh'

check_mmc_configured

proxy_template="templates/squid.conf.tpl"
sarg_template="templates/sarg.conf.tpl"
proxy_conf="/etc/squid/squid.conf"
sarg_conf="/etc/sarg/sarg.conf"

echo "0Configuring squid..."
backup $proxy_conf
cat $proxy_template > $proxy_conf
sed -i "s/\@DN\@/$MDSSUFFIX/" $proxy_conf
# handle 64bit
if [ -d /usr/lib64 ]; then
    sed -i "s!/usr/lib!/usr/lib64!g" $proxy_conf
fi

backup $sarg_conf
cat $sarg_template > $sarg_conf
sed -i "s/\@DN\@/$MDSSUFFIX/" $sarg_conf
sed -i "s/\@PASS\@/$MDSPASS_E/" $sarg_conf

echo "Creating groups..."
python create-groups.py
if [ $? -ne 0 ]; then
	error $"Something went wrong while creating the user groups."
	exit 1
else
	echo "Groups created successfully."
fi

enable_service squid
restart_service squid
restart_service mmc-agent

info_b $"The Proxy service is running"
info $"You can manage the proxy rules from the management interface : https://@HOSTNAME@/mmc/"

exit 0
