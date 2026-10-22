# blosc does not provide the cmake package, so we provide a dummy config file
# This file replicates the interface provided by conan using the pkg-config file
# - https://conan.io/center/recipes/c-blosc
include(CMakeFindDependencyMacro)
find_dependency(PkgConfig)

pkg_search_module(
    c-blosc
    IMPORTED_TARGET
    blosc
)
add_library(c-blosc::c-blosc ALIAS PkgConfig::c-blosc)

# Some compatibility layers for some dependencies found
set(BLOSC_LIBRARY c-blosc::c-blosc)
