include(FindPython)

find_package(Python)

if(Python_FOUND)
  set(ENUMECG_OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/timestamp")
  set(ENUMECG_PYPROJECT_FILE "${CMAKE_CURRENT_SOURCE_DIR}/pyproject.toml")

  add_custom_command(OUTPUT ${ENUMECG_OUTPUT}
    COMMAND Python::Interpreter -m flit -f ${ENUMECG_PYPROJECT_FILE} build
    COMMAND ${CMAKE_COMMAND} -E touch ${ENUMECG_OUTPUT}
    DEPENDS ${ENUMECG_SOURCE_FILES}
    COMMENT "Building python packages")

  add_custom_target(EnumECG ALL DEPENDS ${ENUMECG_OUTPUT})

  get_target_property(PYTHON_EXECUTABLE Python::Interpreter LOCATION)
  install(
    CODE "execute_process(
      COMMAND ${PYTHON_EXECUTABLE} -m flit -f ${ENUMECG_PYPROJECT_FILE} install
    )")

  if (ENHANCEDENUM_BUILD_TESTS)
    add_test(NAME EnumECGTest
      COMMAND Python::Interpreter -m tox
      WORKING_DIRECTORY ${PYTHON_SOURCE_DIR})

    add_test(NAME EnumECGLint
      COMMAND Python::Interpreter -m pylint enumecg
      WORKING_DIRECTORY ${PYTHON_SOURCE_DIR})
endif()
else()
  message(STATUS "Python not found. Skipping building python packages.")
endif()
