project (client)

# Toolkit for working with NK parser.
include (platform/nk)

# Setting compilation flags.
project_header_default ("STANDARD_GNU_11:YES" "STRICT_WARNINGS:NO")

add_executable (Client "src/client.c" ${EDL_FILES})
add_dependencies(Client multi_vfs_dhcpcd_client)
target_link_libraries (Client
                       ${${PROJECT_NAME}_LIBS}
                       rump::dhcpcd_client
                       ${vfs_CLIENT_LIB})

# We do not need default VFS entity here, which comes from ${vfs_CLIENT_LIB}
set_target_properties (Client PROPERTIES ${vfs_ENTITY}_REPLACEMENT "")

