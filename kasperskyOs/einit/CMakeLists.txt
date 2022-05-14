project (einit)

# Toolkit for working with NK parser.
include (platform/image)

# Set compilation flags.
project_header_default ("STANDARD_GNU_11:YES" "STRICT_WARNINGS:NO")

# Define an ENTITIES variable with a list of entities.
set (ENTITIES
     Env
     Client
     VfsRamFs
     VfsSdcardFs
     VfsNet
     ${rump_DHCPCD_ENTITY})

if ("${CMAKE_SYSTEM_PROCESSOR}" STREQUAL "arm")
     set(SECURITY_PSL_FILE "src/security.arm.psl")
else ()
    set(SECURITY_PSL_FILE "src/security.x86.psl")
endif ()

set_target_properties(${rump_DHCPCD_ENTITY} PROPERTIES
            EXTRA_CONNECTIONS
"  - target: multi_vfs_dhcpcd.Env
    id: {var: ENV_SERVICE_NAME, include: env/env.h}
  - target: multi_vfs_dhcpcd.VfsNet
    id: VfsNet
  - target: multi_vfs_dhcpcd.VfsRamFs
    id: VfsRamFs
  - target: multi_vfs_dhcpcd.VfsSdcardFs
    id: VfsSdcardFs")


set_target_properties(${rump_DHCPCD_ENTITY} PROPERTIES DEPENDS_ON_ENTITY "")

# Add a target with making and copying the disk image to the example build
# directory.
add_custom_command (OUTPUT ramdisk0.img
                    COMMAND ${CMAKE_COMMAND} -E make_directory
                        ${CMAKE_BINARY_DIR}/hdd
                    COMMAND ${CMAKE_COMMAND} -E copy_directory
                        ${CMAKE_SOURCE_DIR}/resources/ramfs
                        ${CMAKE_BINARY_DIR}/hdd
                    COMMAND $ENV{SDK_PREFIX}/common/prepare_hdd_img.sh -d ${CMAKE_BINARY_DIR}/hdd -img ramdisk0.img -f ext4 -s 128)
add_custom_target (ramdisk0.img DEPENDS ramdisk0.img)

# Add a target with making and copying the disk image to the example build
# directory.
add_custom_command (OUTPUT sdcard0.img
                    COMMAND ${CMAKE_COMMAND} -E make_directory
                        ${CMAKE_BINARY_DIR}/hdd
                    COMMAND ${CMAKE_COMMAND} -E copy_directory
                        ${CMAKE_SOURCE_DIR}/resources/sdcard
                        ${CMAKE_BINARY_DIR}/hdd
                    COMMAND $ENV{SDK_PREFIX}/common/prepare_hdd_img.sh -d ${CMAKE_BINARY_DIR}/hdd -img sdcard0.img -f fat32)
add_custom_target (sdcard0.img DEPENDS sdcard0.img)

if ("${CMAKE_SYSTEM_PROCESSOR}" MATCHES "arm")
    set (QEMU_FLAGS "-sd sdcard0.img")
else ()
    if (DHCPCD_SDCARD)
        set (QEMU_FLAGS "-drive id=disk0,file=sdcard0.img,if=none \
                         -device ahci,id=ahci0 \
                         -device ide-drive,drive=disk0,bus=ahci0.0")
    else ()
        set (QEMU_FLAGS "-drive id=disk0,file=ramdisk0.img,if=none \
                         -device ahci,id=ahci0 \
                         -device ide-drive,drive=disk0,bus=ahci0.0")
    endif ()
endif ()

set (FILES
        ${CMAKE_BINARY_DIR}/einit/ramdisk0.img)

# Building Kaspersky OS solution image for a hardware platform.
build_kos_hw_image (kos-image
                    EINIT_ENTITY EinitHw
                    CONNECTIONS_CFG "src/init.yaml.in"
                    SECURITY_PSL  ${SECURITY_PSL_FILE}
                    IMAGE_FILES ${ENTITIES}
                                ${FILES})
add_dependencies (kos-image ramdisk0.img)

# Building Kaspersky OS solution image for a QEMU platform.
build_kos_qemu_image (kos-qemu-image
                      EINIT_ENTITY EinitQemu
                      CONNECTIONS_CFG "src/init.yaml.in"
                      SECURITY_PSL  ${SECURITY_PSL_FILE}
                      QEMU_FLAGS "${QEMU_FLAGS}"
                      IMAGE_FILES ${ENTITIES}
                                  ${CMAKE_BINARY_DIR}/einit/sdcard0.img
                                  ${FILES})
add_dependencies (kos-qemu-image ramdisk0.img sdcard0.img)

#set_target_properties (einit PROPERTIES LINK_FLAGS "-Ttext 0x00200000")
