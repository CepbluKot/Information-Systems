project (env)

# Toolchain for work with NK-parser.
include (platform/nk)

# Set compilation flags.
project_header_default ("STANDARD_GNU_11:YES" "STRICT_WARNINGS:NO")

add_executable (Env "src/env.c" ${EDL_FILES})
add_dependencies(Env multi_vfs_dhcpcd_env)
target_link_libraries (Env ${ENV_SERVER_LIB})
