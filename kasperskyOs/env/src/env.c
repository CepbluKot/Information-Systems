#include <env/env.h>
#include <vfs/rumpfs_client.h>
#include <vfs/vfs.h>
#include <stdio.h>
#include <stdlib.h>


/* Add an automatically generated config file. */
#include "config.h"

#define NET_VFS_CONNECTION       "VfsNet"
#define RAM_FS_VFS_CONNECTION    "VfsRamFs"
#define SDCARD_FS_VFS_CONNECTION "VfsSdcardFs"

#define WHITE "\033[1;37m"
#define NC    "\033[0m"

int main(int argc, char** argv)
{
    /*FIXME: VFS with _VFS_NETWORK_BACKEND can't print any messages and the printf will not work!
     * And in the future, it needs to replace all printf to fprintf(stderr) and OutString/printk in rump and etc.
    */
    const char* VfsNetArgs[] = {
        "-l", "devfs /dev devfs 0"
    };
    const char* VfsNetEnvs[] = {
        _VFS_NETWORK_BACKEND"=server:"NET_VFS_CONNECTION,
        _VFS_FILESYSTEM_BACKEND"=server:"NET_VFS_CONNECTION,
    };
    ENV_REGISTER_PROGRAM_ENVIRONMENT("VfsNet", VfsNetArgs, VfsNetEnvs);

    const char* VfsRamFsArgs[] = {
    };
    const char* VfsRamFsEnvs[] = {
        "ROOTFS=ramdisk0,0 / ext4 0",
        _VFS_FILESYSTEM_BACKEND"=server:"RAM_FS_VFS_CONNECTION,
    };
    ENV_REGISTER_PROGRAM_ENVIRONMENT("VfsRamFs", VfsRamFsArgs, VfsRamFsEnvs);

    const char* VfsSdcardFsArgs[] = {
        "-l", "nodev /tmp ramfs 0",
        "-l", "nodev /var ramfs 0"
    };
    const char* VfsSdcardFsEnvs[] = {
        "ROOTFS=mmc0,0 / fat32 0",
        _VFS_FILESYSTEM_BACKEND"=server:"SDCARD_FS_VFS_CONNECTION,
    };

    ENV_REGISTER_PROGRAM_ENVIRONMENT("VfsSdcardFs", VfsSdcardFsArgs, VfsSdcardFsEnvs);

    const char* ClientEnvs[] = {
        _VFS_NETWORK_BACKEND"=client:"NET_VFS_CONNECTION,
    };
    ENV_REGISTER_VARS("Client", ClientEnvs);

    const char* DhcpcdEnvs[] = {
#if defined(DHCPCD_SDCARD) && defined(__arm__)
        _VFS_FILESYSTEM_BACKEND"="RUMPFS_CLIENT_FS_BACKEND":"SDCARD_FS_VFS_CONNECTION,
#else
        _VFS_FILESYSTEM_BACKEND"="RUMPFS_CLIENT_FS_BACKEND":"RAM_FS_VFS_CONNECTION,
#endif
        _VFS_NETWORK_BACKEND"=client:"NET_VFS_CONNECTION,
    };

#if defined(DHCPCD_SDCARD)
    const char* DhcpcdRootFsDevice = "sdcard";
#else
    const char* DhcpcdRootFsDevice = "ramfs";
#endif

#if defined(DHCPCD_FALLBACK)
    const char* DhcpcdArgs[] = {
        "-4",
        "-f", "/etc/dhcpcd.conf"
    };

    fprintf(stderr, "[ENV] Used " WHITE "dynamic" NC " network configuration "
            WHITE "with fallback to static" NC " configuration by "
            WHITE "%s" NC ":/etc/dhcpcd.conf\r\n",
            DhcpcdRootFsDevice);

#elif defined(DHCPCD_DYNAMIC)
    const char* DhcpcdArgs[] = {
        "-4",
        "-f", "/etc/dhcpcd_dynamic.conf"
    };

    fprintf(stderr, "[ENV] Used " WHITE "dynamic" NC " network configuration by "
            WHITE "%s" NC ":/etc/dhcpcd_dynamic.conf\r\n",
            DhcpcdRootFsDevice);

#elif defined(DHCPCD_STATIC)
    const char* DhcpcdArgs[] = {
        "-4",
        "-f", "/etc/dhcpcd_static.conf"
    };

    fprintf(stderr, "[ENV] Used " WHITE "static" NC " network configuration by "
            WHITE "%s" NC ":/etc/dhcpcd_static.conf\r\n",
            DhcpcdRootFsDevice);

#else
    const char* DhcpcdArgs[] = {
        "-4",
        "-f", "/etc/dhcpcd.conf"
    };

    fprintf(stderr, "[ENV] Used " WHITE "default dynamic" NC
            " network configuration " WHITE "with fallback to static" NC
            " configuration by " WHITE "%s" NC ":/etc/dhcpcd.conf\r\n",
            DhcpcdRootFsDevice);
#endif

    ENV_REGISTER_PROGRAM_ENVIRONMENT("Dhcpcd", DhcpcdArgs, DhcpcdEnvs);

    envServerRun();

    return EXIT_SUCCESS;
}
