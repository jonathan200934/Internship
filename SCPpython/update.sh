#!/bin/sh

function log()
{
	echo $1
#	echo "[fw-update] $1" >> /dev/kmsg
}

log "Updating"

cd /tmp/

md5=$(md5sum v1.1.0.6_update.tar.gz|cut -d' ' -f1)
echo $md5
if [ $md5 = "91ac640df44ecc009bdb3f457b0c1bb0" ]; then
        log "MD5 Sum Match"
else
        log "MD5 Mismatch"
        exit 
fi

version=$(cat /etc/version|cut -d' ' -f1)
echo $version
if [ $version = "V1.1.0-5" ]; then
        log "Proceed to update"
else
        log "This is not older version"
        exit 2
fi

log "Updating started.."
tar -xzf v1.1.0.6_update.tar.gz

log "Updating NTP"
cp /tmp/ntp.conf /etc/ntp.conf

log "Updating bs configuration"
cp /tmp/bs.conf /run/media/mmcblk0p1/bs.conf

cp /tmp/bsconfig /run/media/mmcblk0p1/bsconfig

log "Removing sensitive file from SD"
rm /run/media/mmcblk0p2/mnt/nand.tgz
rm -rf /run/media/mmcblk0p2/mnt/nand/*
rm /run/media/mmcblk0p1/i2c.conf

mkdir /run/media/mmcblk0p2/mnt/nand/log/

log "Fixing UBIIK ssh issue"
chown ubiik:ubiik /mnt/nand/fs/.ssh
rm /home/ubiik/.ssh
su ubiik -c "ln -sf /mnt/nand/fs/.ssh /home/ubiik/.ssh"

log "Updating Version"
echo "V1.1.0-6" > /etc/version
sync

log "Update completed"
