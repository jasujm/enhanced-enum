cmake_minimum_required(VERSION 3.11)
project("Enhanced Enum"
  DESCRIPTION "First class enums in C++"
  VERSION "0.0.1")

set(ENHANCEDENUM_LIB "EnhancedEnum")
set(ENHANCEDENUM_INCLUDE_DIRS "${PROJECT_SOURCE_DIR}/cxx-include")

add_library(${ENHANCEDENUM_LIB} INTERFACE)
target_include_directories(${ENHANCEDENUM_LIB} INTERFACE
  ${ENHANCEDENUM_INCLUDE_DIRS})
target_compile_features(${ENHANCEDENUM_LIB} INTERFACE cxx_std_17)

install(DIRECTORY ${PROJECT_SOURCE_DIR}/cxx-include/ DESTINATION include)

set(ENHANCEDENUM_BUILD_TESTS ON CACHE BOOL "Build tests")
if(ENHANCEDENUM_BUILD_TESTS)
  enable_testing()
  add_subdirectory(cxx-tests)
endif()
