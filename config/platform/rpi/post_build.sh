#!/bin/bash

# This script is executed for Raspberry Pi after a build

# TODO: Check that we've actually installed a custom kernel,
#  otherwise, leave the default from the RPI Foundation in place


echo ""
echo "#################################################################"
echo "#################################################################"
echo "##                                                             ##"
echo "##                                                             ##"
echo ""
echo "                     _   _            _ "
echo "                    | | | | ___ _   _| |"
echo "                    | |_| |/ _ \ | | | |"
echo "                    |  _  |  __/ |_| |_|"
echo "                    |_| |_|\___|\__, (_)"
echo "                                |___/   "
echo ""
echo "issue the following command(s) to complete your raspberry pi image"

if [ -f ${TOP}/rootfs/boot/zImage ] ; then 
    echo ""
    echo "# Copy the newly-built kernel to kernel.img"
    echo sudo cp ${TOP}/rootfs/boot/zImage ${TOP}/rootfs/boot/kernel.img
fi

echo ""
echo sudo ${PLATFORM_PATH}/rpi_mksdimage.sh -B ${DEV_IMAGE}/boot/ -R ${TOP}/rootfs.ext2.gz
echo ""
echo "##                                                             ##"
echo "##                                                             ##"
echo "#################################################################"
echo "#################################################################"
echo ""

