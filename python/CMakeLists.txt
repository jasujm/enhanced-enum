include(FindPython)

find_package(Python)

if(Python_FOUND)
  set(ENUMECG_SETUP_IN "${CMAKE_CURRENT_SOURCE_DIR}/setup.py.in")
  set(ENUMECG_SETUP_OUT "${CMAKE_CURRENT_BINARY_DIR}/setup.py")
  file(GLOB_RECURSE ENUMECG_PYS "${CMAKE_CURRENT_SOURCE_DIR}/enumecg/*.py")
  set(ENUMECG_OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/build/lib/enumecg/__init__.py")
  configure_file(${ENUMECG_SETUP_IN} ${ENUMECG_SETUP_OUT} @ONLY)
  add_custom_command(OUTPUT ${ENUMECG_OUTPUT}
    COMMAND Python::Interpreter ${ENUMECG_SETUP_OUT} build
    MAIN_DEPENDENCY ${ENUMECG_SETUP_IN}
    DEPENDS ${ENUMECG_PYS}
    COMMENT "Building python packages")

  add_custom_target(EnumECG ALL DEPENDS ${ENUMECG_OUTPUT})
else()
  message(STATUS "Python not found. Skipping building python packages.")
endif()
