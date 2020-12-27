include(FetchContent)
include(GoogleTest)
include(FindPython)

find_package(Python)

if (Python_FOUND)
  set(INSTALL_GTEST OFF CACHE BOOL "" FORCE)

  # The following snippets for including googletest is adapted from Henry
  # Schreiner et al.: Modern CMake (https://cliutils.gitlab.io/modern-cmake/)
  # released under CC BY-NC-SA 4.0
  # (https://creativecommons.org/licenses/by-nc-sa/4.0/)
  FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG release-1.10.0
    INSTALL_DIR "${CMAKE_BINARY_DIR}"
    CMAKE_ARGS "-DCMAKE_INSTALL_PREFIX=${CMAKE_BINARY_DIR}")

  FetchContent_GetProperties(googletest)
  if(NOT googletest_POPULATED)
    FetchContent_Populate(googletest)
    add_subdirectory(${googletest_SOURCE_DIR} ${googletest_BINARY_DIR})
  endif()
  mark_as_advanced(
    BUILD_GMOCK BUILD_GTEST BUILD_SHARED_LIBS INSTALL_GTEST
    gmock_build_tests gtest_build_samples gtest_build_tests
    gtest_disable_pthreads gtest_force_shared_crt gtest_hide_internal_symbols)

  set(STATUS_DEFINITIONS_INCLUDE_DIR "${CMAKE_CURRENT_BINARY_DIR}/include")
  file(MAKE_DIRECTORY ${STATUS_DEFINITIONS_INCLUDE_DIR})
  set(STATUS_DEFINITIONS_HEADER "${STATUS_DEFINITIONS_INCLUDE_DIR}/status.hh")
  set(STATUS_DEFINITIONS_GENERATOR_PY "${CMAKE_CURRENT_SOURCE_DIR}/generate_status_hh.py")
  add_custom_command(OUTPUT ${STATUS_DEFINITIONS_HEADER}
    COMMAND ${CMAKE_COMMAND} -E env PYTHONPATH=${PYTHON_SOURCE_DIR}
      $<TARGET_PROPERTY:Python::Interpreter,LOCATION>
      ${STATUS_DEFINITIONS_GENERATOR_PY} ${STATUS_DEFINITIONS_HEADER}
    DEPENDS ${ENUMECG_SOURCE_FILES} "${PYTHON_SOURCE_DIR}/tests/conftest.py"
    MAIN_DEPENDENCY ${STATUS_DEFINITIONS_GENERATOR_PY})

  set(ENHANCEDENUM_TEST "${ENHANCEDENUM_LIB}Test")
  add_executable(${ENHANCEDENUM_TEST} test.cc ${STATUS_DEFINITIONS_HEADER})
  target_include_directories(${ENHANCEDENUM_TEST} PRIVATE ${STATUS_DEFINITIONS_INCLUDE_DIR})
  target_link_libraries(${ENHANCEDENUM_TEST} ${ENHANCEDENUM_LIB} gtest gtest_main)
  gtest_discover_tests(${ENHANCEDENUM_TEST})

  set(ENHANCEDENUM_CXX20_TEST "${ENHANCEDENUM_LIB}TestC++20")
  add_executable(${ENHANCEDENUM_CXX20_TEST} test.cc ${STATUS_DEFINITIONS_HEADER})
  target_include_directories(${ENHANCEDENUM_CXX20_TEST} PRIVATE ${STATUS_DEFINITIONS_INCLUDE_DIR})
  target_link_libraries(${ENHANCEDENUM_CXX20_TEST} ${ENHANCEDENUM_LIB} gtest gtest_main)
  target_compile_features(${ENHANCEDENUM_CXX20_TEST} PRIVATE cxx_std_20)
  gtest_discover_tests(${ENHANCEDENUM_CXX20_TEST} TEST_PREFIX "C++20/")
else()
  message(STATUS "Python not found. Skipping building tests.")
endif()
