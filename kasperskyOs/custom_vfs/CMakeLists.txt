project (customvfs)

# Toolkit for working with NK parser.
include (platform/nk)

# Setting compilation flags.
project_header_default ("STANDARD_GNU_11:YES" "STRICT_WARNINGS:NO")

add_executable (VfsRamFs "src/vfs.c")
add_dependencies(VfsRamFs multi_vfs_dhcpcd_vfs_ram_fs)
target_link_libraries (VfsRamFs
                       ${vfs_SERVER_LIB}
                       ${LWEXT4_LIB}
                       ${vfs_FS_LIB})
set_target_properties (VfsRamFs PROPERTIES ${blkdev_ENTITY}_REPLACEMENT ${ramdisk_ENTITY})

add_executable (VfsSdcardFs "src/vfs.c")
add_dependencies(VfsSdcardFs multi_vfs_dhcpcd_vfs_sdcard_fs)
target_link_libraries (VfsSdcardFs
                       ${vfs_SERVER_LIB}
                       ${VFAT_LIB}
                       ${vfs_FS_LIB})
set_target_properties (VfsSdcardFs PROPERTIES ${blkdev_ENTITY}_REPLACEMENT ${sdcard_ENTITY})

add_executable (VfsNet "src/vfs.c")
add_dependencies(VfsNet multi_vfs_dhcpcd_vfs_net)
target_link_libraries (VfsNet
                       ${vfs_SERVER_LIB}
                       ${vfs_IMPLEMENTATION_LIB}
                       ${dnet_IMPLEMENTATION_LIB})
set_target_properties (VfsNet PROPERTIES ${blkdev_ENTITY}_REPLACEMENT "")
