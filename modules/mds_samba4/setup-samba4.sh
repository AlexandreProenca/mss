#!/bin/bash

. ../functions.sh

check_mmc_configured

python ./provision.py $1 $2 $3
if [ "$?" != "0" ]; then
    exit $?
fi

# confirmation
info_b $"You can now use the management interface to manage your Windows users and shares at https://@HOSTNAME@/mmc/."

exit 0
