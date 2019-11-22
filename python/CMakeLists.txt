include(FindPython)

find_package(Python)

if(Python_FOUND)
  set(PYTHON_BUILD_DIR "${CMAKE_CURRENT_BINARY_DIR}/build/lib")

  set(ENUMECG_SETUP_IN "${PYTHON_SOURCE_DIR}/setup.py.in")
  set(ENUMECG_SETUP_OUT "${CMAKE_CURRENT_BINARY_DIR}/setup.py")
  set(ENUMECG_OUTPUT "${PYTHON_BUILD_DIR}/enumecg/__init__.py")
  configure_file(${ENUMECG_SETUP_IN} ${ENUMECG_SETUP_OUT} @ONLY)
  add_custom_command(OUTPUT ${ENUMECG_OUTPUT}
    COMMAND Python::Interpreter ${ENUMECG_SETUP_OUT} build
    MAIN_DEPENDENCY ${ENUMECG_SETUP_IN}
    DEPENDS ${ENUMECG_SOURCE_FILES}
    COMMENT "Building python packages")

  add_custom_target(EnumECG ALL DEPENDS ${ENUMECG_OUTPUT})

  if (ENHANCEDENUM_BUILD_TESTS)
    add_test(NAME EnumECGTest
      COMMAND Python::Interpreter -m unittest
      WORKING_DIRECTORY ${PYTHON_SOURCE_DIR})
  endif()
else()
  message(STATUS "Python not found. Skipping building python packages.")
endif()
