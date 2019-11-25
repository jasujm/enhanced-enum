cmake_minimum_required(VERSION 3.11)
project("Enhanced Enum"
  DESCRIPTION "First class enums in C++"
  VERSION "0.0.1")

set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake" ${CMAKE_MODULE_PATH})

set(ENHANCEDENUM_LIB "EnhancedEnum")
set(ENHANCEDENUM_INCLUDE_DIRS "${PROJECT_SOURCE_DIR}/cxx/include")

set(PYTHON_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/python")
file(GLOB_RECURSE ENUMECG_SOURCE_PYS "${PYTHON_SOURCE_DIR}/enumecg/*.py")
file(GLOB ENUMECG_SOURCE_TEMPLATES "${PYTHON_SOURCE_DIR}/enumecg/templates/*.in")
set(ENUMECG_SOURCE_FILES ${ENUMECG_SOURCE_PYS} ${ENUMECG_SOURCE_TEMPLATES})

add_library(${ENHANCEDENUM_LIB} INTERFACE)
target_include_directories(${ENHANCEDENUM_LIB} INTERFACE
  ${ENHANCEDENUM_INCLUDE_DIRS})
target_compile_features(${ENHANCEDENUM_LIB} INTERFACE cxx_std_17)

install(DIRECTORY ${ENHANCEDENUM_INCLUDE_DIRS}/ DESTINATION include)

set(ENHANCEDENUM_BUILD_DOCS ON CACHE BOOL "Build documentation")
if(ENHANCEDENUM_BUILD_DOCS)
  add_subdirectory(docs)
endif()

set(ENHANCEDENUM_BUILD_TESTS ON CACHE BOOL "Build tests")
if(ENHANCEDENUM_BUILD_TESTS)
  enable_testing()
  add_subdirectory(cxx/tests)
endif()

set(ENHANCEDENUM_BUILD_PYTHON ON CACHE BOOL "Build python modules")
if(ENHANCEDENUM_BUILD_PYTHON)
  add_subdirectory(python)
endif()
