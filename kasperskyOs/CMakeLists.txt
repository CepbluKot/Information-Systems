cmake_minimum_required (VERSION 3.12)

project (multi_vfs_dhcpcd)

# Initialize CMake library for Kaspersky OS SDK.
include (platform)
initialize_platform ()

# Connect artifact installation functions.
include (platform/install)

# Attach project tests
include (platform/tests)
add_project_tests_main_target ()

# Attach project dDocumentation
include (platform/doxygen)
add_project_documentation_main_target ()

# Platform definitions
include (platform/options)

# Build idl/cdl/edl files
include (platform/nk)
nk_build_edl_files (multi_vfs_dhcpcd_vfs_ram_fs
                    NK_MODULE "multi_vfs_dhcpcd"
                    EDL "resources/edl/VfsRamFs.edl")

nk_build_edl_files (multi_vfs_dhcpcd_vfs_sdcard_fs
                    NK_MODULE "multi_vfs_dhcpcd"
                    EDL "resources/edl/VfsSdcardFs.edl")

nk_build_edl_files (multi_vfs_dhcpcd_vfs_net
                    NK_MODULE "multi_vfs_dhcpcd"
                    EDL "resources/edl/VfsNet.edl")

nk_build_edl_files (multi_vfs_dhcpcd_env
                    NK_MODULE "multi_vfs_dhcpcd"
                    EDL "resources/edl/Env.edl")

nk_build_edl_files (multi_vfs_dhcpcd_client
                    NK_MODULE "multi_vfs_dhcpcd"
                    EDL "resources/edl/Client.edl")

# Attach a package with the virtual file system implementation.
find_package (vfs REQUIRED)
include_directories (${vfs_INCLUDE})

# Attach a package with the dhcpcd entity implementation.
find_package (rump REQUIRED COMPONENTS DHCPCD_ENTITY)
include_directories (${rump_INCLUDE})

# Attach a package with the ramdisk implementation.
find_package (ramdisk REQUIRED)
include_directories (${ramdisk_INCLUDE})

# Attach a package with the Ext4 file system implementation.
find_package (LWEXT4 REQUIRED)
include_directories (${LWEXT4_INCLUDE})

# Attach a package with the sdcard suppport implementation.
find_package (sdcard REQUIRED)
include_directories (${sdcard_INCLUDE})

# Attach a package with the FAT file system implementation.
find_package (VFAT REQUIRED)
include_directories (${VFAT_INCLUDE})

# Attach a package with the DNET file system implementation.
find_package (dnet REQUIRED COMPONENTS IMPLEMENTATION_LIB)

# Choose the storage devices for the configuration files and the network
# configuration mode.
# If none of the options are selected, the ramfs device and the dynamic
# network configuration with fallback to static mode are used.
option(DHCPCD_SDCARD   "Use SD card to get configuration file"       OFF)
option(DHCPCD_FALLBACK "Configuration by /etc/dhcpcd.conf"           OFF)
option(DHCPCD_DYNAMIC  "Configuration by /etc/dhcpcd_dynamic.config" OFF)
option(DHCPCD_STATIC   "Configuration by /etc/dhcpcd_static.config"  OFF)

# Build configuration header files from a configuration file template
configure_file(resources/include/config.h.in config.h)

# Attach the directory with the generated config header files
include_directories(${CMAKE_CURRENT_BINARY_DIR})

# Attach the directories with entities.
add_subdirectory (client)
add_subdirectory (custom_vfs)
add_subdirectory (env)

# Attach the directory with the Einit entity to create a solution image
# based on Kaspersky OS.
add_subdirectory (einit)
