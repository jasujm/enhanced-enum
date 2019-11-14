# The following snippets for including googletest is adapted from
# Henry Schreiner et al.: Modern CMake (https://cliutils.gitlab.io/modern-cmake/)
# released under CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/)

include(FetchContent)
include(GoogleTest)

FetchContent_Declare(
  googletest
  GIT_REPOSITORY https://github.com/google/googletest.git
  GIT_TAG        release-1.10.0
)
FetchContent_GetProperties(googletest)
if(NOT googletest_POPULATED)
  FetchContent_Populate(googletest)
  add_subdirectory(${googletest_SOURCE_DIR} ${googletest_BINARY_DIR})
  set(INSTALL_GTEST OFF CACHE BOOL "" FORCE)
endif()
mark_as_advanced(
    BUILD_GMOCK BUILD_GTEST BUILD_SHARED_LIBS INSTALL_GTEST
    gmock_build_tests gtest_build_samples gtest_build_tests
    gtest_disable_pthreads gtest_force_shared_crt gtest_hide_internal_symbols
)

set(ENHANCEDENUM_TEST "${ENHANCEDENUM_LIB}Test")
add_executable(${ENHANCEDENUM_TEST} test.cc)
target_link_libraries(${ENHANCEDENUM_TEST} ${ENHANCEDENUM_LIB} gtest gtest_main)
gtest_discover_tests(${ENHANCEDENUM_TEST})
