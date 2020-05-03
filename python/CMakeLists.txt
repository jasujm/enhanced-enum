include(FindPython)

find_package(Python)

if(Python_FOUND)
  get_target_property(PYTHON_EXECUTABLE Python::Interpreter LOCATION)
  set(PYTHON_BUILD_DIR "${CMAKE_CURRENT_BINARY_DIR}/build/lib")
  file(MAKE_DIRECTORY ${PYTHON_BUILD_DIR})

  set(ENUMECG_SETUP "${CMAKE_CURRENT_SOURCE_DIR}/setup.py")
  set(ENUMECG_OUTPUT "${PYTHON_BUILD_DIR}/timestamp")
  add_custom_command(OUTPUT ${ENUMECG_OUTPUT}
    COMMAND ${CMAKE_COMMAND} -E env IS_CMAKE_BUILD=1
      ${PYTHON_EXECUTABLE} ${ENUMECG_SETUP} build
    COMMAND ${CMAKE_COMMAND} -E touch ${ENUMECG_OUTPUT}
    DEPENDS ${ENUMECG_SOURCE_FILES}
    COMMENT "Building python packages")

  add_custom_target(EnumECG ALL DEPENDS ${ENUMECG_OUTPUT})

  install(
    CODE "execute_process(
      COMMAND ${CMAKE_COMMAND} -E env IS_CMAKE_BUILD=1
        ${PYTHON_EXECUTABLE} ${ENUMECG_SETUP} install
    )")

  if (ENHANCEDENUM_BUILD_TESTS)
    add_test(NAME EnumECGTest
      COMMAND Python::Interpreter -m tox
      WORKING_DIRECTORY ${PYTHON_SOURCE_DIR})
  endif()
else()
  message(STATUS "Python not found. Skipping building python packages.")
endif()
