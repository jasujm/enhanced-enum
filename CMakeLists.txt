cmake_minimum_required(VERSION 3.11)
project("Enhanced Enum"
  DESCRIPTION "First class enums in C++"
  VERSION "0.4")

set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake" ${CMAKE_MODULE_PATH})

set(ENHANCEDENUM_LIB "EnhancedEnum")
set(ENHANCEDENUM_INCLUDE_DIR "${PROJECT_SOURCE_DIR}/cxx/include")

add_library(${ENHANCEDENUM_LIB} INTERFACE)
target_include_directories(${ENHANCEDENUM_LIB} INTERFACE
  $<BUILD_INTERFACE:${ENHANCEDENUM_INCLUDE_DIR}>
  $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)
target_compile_features(${ENHANCEDENUM_LIB} INTERFACE cxx_std_17)

# Only expose headers if this is a subproject of another project
# Otherwise proceed with install targets, tests etc.

get_directory_property(IS_SUBPROJECT PARENT_DIRECTORY)
if(NOT IS_SUBPROJECT)
  include(GNUInstallDirs)
  include(CMakePackageConfigHelpers)

  set(PYTHON_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/python")
  file(GLOB_RECURSE ENUMECG_SOURCE_PYS "${PYTHON_SOURCE_DIR}/enumecg/**.py")
  file(GLOB ENUMECG_SOURCE_TEMPLATES "${PYTHON_SOURCE_DIR}/enumecg/templates/*.in")
  set(ENUMECG_SOURCE_FILES ${ENUMECG_SOURCE_PYS} ${ENUMECG_SOURCE_TEMPLATES})

  # Building exportable C++ lib adapted from blog post:
  # http://dominikberner.ch/cmake-interface-lib/

  set(ENHANCEDENUM_TARGETS "${ENHANCEDENUM_LIB}_Targets")
  set(ENHANCEDENUM_CONFIGVERSION "${ENHANCEDENUM_LIB}ConfigVersion.cmake")
  set(ENHANCEDENUM_CONFIG "${PROJECT_BINARY_DIR}/${ENHANCEDENUM_LIB}Config.cmake")

  install(TARGETS ${ENHANCEDENUM_LIB}
    EXPORT ${ENHANCEDENUM_TARGETS}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})

  write_basic_package_version_file(${ENHANCEDENUM_CONFIGVERSION}
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion)

  configure_package_config_file(
    "${PROJECT_SOURCE_DIR}/cmake/${ENHANCEDENUM_LIB}Config.cmake.in"
    ${ENHANCEDENUM_CONFIG}
    INSTALL_DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/${ENHANCEDENUM_LIB}/cmake)

  install(EXPORT ${ENHANCEDENUM_TARGETS}
    FILE ${ENHANCEDENUM_LIB}Targets.cmake
    NAMESPACE ${ENHANCEDENUM_LIB}::
    DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/${ENHANCEDENUM_LIB}/cmake)

  install(FILES ${ENHANCEDENUM_CONFIG}
    "${PROJECT_BINARY_DIR}/${ENHANCEDENUM_CONFIGVERSION}"
    DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/${ENHANCEDENUM_LIB}/cmake)

  install(DIRECTORY ${ENHANCEDENUM_INCLUDE_DIR}/ DESTINATION include)

  set(ENHANCEDENUM_BUILD_TESTS OFF CACHE BOOL "Build tests")
  if(ENHANCEDENUM_BUILD_TESTS)
    enable_testing()
  endif()

  set(ENHANCEDENUM_BUILD_DOCS OFF CACHE BOOL "Build documentation")
  if(ENHANCEDENUM_BUILD_DOCS)
    add_subdirectory(docs)
  endif()

  if(ENHANCEDENUM_BUILD_TESTS)
    add_subdirectory(cxx/tests)
  endif()

  set(ENHANCEDENUM_BUILD_PYTHON OFF CACHE BOOL "Build python modules")
  if(ENHANCEDENUM_BUILD_PYTHON)
    add_subdirectory(python)
  endif()
endif()
