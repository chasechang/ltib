#!/bin/bash
#!/bin/bash -x

PATH=/sbin:${PATH}

set -e

usage()
{
cat <<EOF

  `basename $0`: 

     Make a Raspberry Pi SD card image

       -h                     : This help message
       -o <image_name>        : What to name the image ( `basename ${IMGFILE}` )
       -s <MB>                : Size of image in MB ( ${IMG_MBYTES} )
       -b <MB>                : Size of boot partition in MB ( ${BOOT_MBYTES} )
       -B </path/to/bootfs>   : Path to files to be copied into boot partition
       -R </path/to/rootfs.gz>: Path to compressed rootfs file
       -v                     : Turn on verbose output
EOF
}

while getopts “ho:s:b:B:R:v” OPTION
do
     case $OPTION in
         h)
	     HELP_OPT=1
             ;;
         o)
             OUTFILE_OPT=$OPTARG
             ;;
	 s)
	     SIZE_OPT=$OPTARG
	     ;;
	 s)
	     BOOT_SIZE_OPT=$OPTARG
	     ;;
	 B)
	     BOOTFS_OPT=$OPTARG
	     ;;
	 R)
	     ROOTFS_OPT=$OPTARG
	     ;;
         v)
             VERBOSE=1
             ;;
         ?)
             usage
             exit
             ;;
     esac
done

IMGFILE=${OUTFILE_OPT:-rpi_sdcard.img}
IMG_MBYTES=${SIZE_OPT:-300}
BOOT_MBYTES=${BOOT_SIZE_OPT:-50}
BOOTFS_PATH=${BOOTFS_OPT:-""}
ROOTFS_PATH=${ROOTFS_OPT:=""}


BOOT_BYTES=`expr ${BOOT_MBYTES} \* 1024 \* 1024`
BOOT_BLOCKS=`expr ${BOOT_MBYTES} \* 1024`

if [ ! -z "${HELP_OPT:-}" ] ; then
    usage
    exit
fi

if [[ ${EUID} != 0 && ${UID} != 0 ]] ; then
    echo "$0 must be run as root"
    usage
    exit -1
fi

if [ ! -z "$BOOTFS_PATH" ] ; then
    if [ ! -e "$BOOTFS_PATH" ] ; then
	echo "Boot path $BOOTFS_PATH does not exist"
	exit -1;
    fi
    if [ ! -d "$BOOTFS_PATH" ] ; then
	echo "Boot path $BOOTFS_PATH is not a directory"
	exit -1
    fi
fi

if [ ! -z "$ROOTFS_PATH" ] ; then
    if [ ! -e "$ROOTFS_PATH" ] ; then 
	echo "Root path $ROOTFS_PATH does not exist"
	exit -1;
    fi
    if [ ! -f "$ROOTFS_PATH" ] ; then
	echo "Root path $ROOTFS_PATH is not a file"
	exit -1
    fi
fi


# Create the empty image file of the proper size
rm -f ${IMGFILE}
dd if=/dev/zero of=$IMGFILE bs=1M count=${IMG_MBYTES}

# Create a W95 FAT partition 1
#   The remainder of the file to a Linux partition
# fdisk is "scriptable".   Yuck

fdisk $IMGFILE >/dev/null <<EOF
n
p
1

+${BOOT_MBYTES}M
t
c
n
p
2


w
EOF

BYTES_PER_SECTOR=`fdisk -lu ${IMGFILE} | grep ^Units | awk '{print $9}'`
BOOT_START_SECTOR=`fdisk -lu ${IMGFILE} | grep ^${IMGFILE}1 | awk '{print $2}'`
LINUX_START_SECTOR=`fdisk -lu ${IMGFILE} | grep ^${IMGFILE}2 | awk '{print $2}'`
BOOT_OFFSET=`expr ${BOOT_START_SECTOR} \* ${BYTES_PER_SECTOR}`
LINUX_OFFSET=`expr ${LINUX_START_SECTOR} \* ${BYTES_PER_SECTOR}`


# Make a loop device for the boot partition at the correct offset
#   in the disk image file; use that device for mkfs
# This avoids error messages about "you must provide an fstype" to mount
#
#   Note that this is race-y; something else could get our DEVICE before
#   we do.
DEVICE=`losetup -f`
losetup -o ${BOOT_OFFSET} --sizelimit ${BOOT_BYTES} ${DEVICE} ${IMGFILE}
mkfs.msdos -F 32 ${DEVICE} -n BOOT ${BOOT_BLOCKS}
sync
losetup -d ${DEVICE}


if [ ! -z "${BOOTFS_PATH}" ] ; then
    # Mount our shiny new filesystem and copy things to it
    BOOTMOUNT="__bootmount.$$"
    mkdir -p ${BOOTMOUNT}
    mount -o loop,sizelimit=${BOOT_BYTES},offset=${BOOT_OFFSET} ${IMGFILE} ${BOOTMOUNT}
    BOOTFS_PATH=`readlink -f ${BOOTFS_PATH}`
    pushd ${BOOTMOUNT}
    ( cd ${BOOTFS_PATH}; tar cvf - `find . ! -type l -a ! -name .`) | tar xf -
    popd
    sync
    umount ${BOOTMOUNT}
    rm -rf ${BOOTMOUNT}
fi

if [ ! -z "${ROOTFS_PATH}" ] ; then
    # Get the name of the next free loop device
    DEVICE=`losetup -f`
    # create a loop device for the image file at the offset appropriate for the Linux partition
    losetup -o ${LINUX_OFFSET} ${DEVICE} ${IMGFILE}
    # dd the ROOTFS to the Linux partition
    zcat ${ROOTFS_PATH} | dd of=${DEVICE}
    sync
    losetup -d ${DEVICE}
fi

#DEVICE=`losetup -f`
#losetup -o ${LINUX_OFFSET} ${DEVICE} ${IMGFILE}
#mkfs.ext4 ${DEVICE} 
#losetup -d ${DEVICE}

# Mount our shiny new filesystem and copy things to it
#LINUXMOUNT="__linuxmount.$$"
#mkdir -p ${LINUXMOUNT}
#mount -o loop,offset=${LINUX_OFFSET} ${IMGFILE} ${LINUXMOUNT}
#sleep 2
#umount ${LINUXMOUNT}
#rm -rf ${LINUXMOUNT}

