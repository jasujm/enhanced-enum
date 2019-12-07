# Adapted from the blog post:
# https://devblogs.microsoft.com/cppblog/clear-functional-c-documentation-with-sphinx-breathe-doxygen-cmake/

find_package(Doxygen)
find_package(Sphinx)

if(Doxygen_FOUND AND Sphinx_FOUND)
  set(DOXYGEN_OUTPUT_DIR "${CMAKE_CURRENT_BINARY_DIR}/doxygen")
  set(DOXYGEN_INDEX_FILE "${DOXYGEN_OUTPUT_DIR}/xml/index.xml")
  set(DOXYFILE_IN ${CMAKE_CURRENT_SOURCE_DIR}/Doxyfile.in)
  set(DOXYFILE_OUT ${CMAKE_CURRENT_BINARY_DIR}/Doxyfile)
  file(GLOB_RECURSE ENHANCEDENUM_HEADERS "${ENHANCEDENUM_INCLUDE_DIR}/*.hh")
  configure_file(${DOXYFILE_IN} ${DOXYFILE_OUT} @ONLY)
  add_custom_command(OUTPUT ${DOXYGEN_INDEX_FILE}
    COMMAND Doxygen::doxygen ${DOXYFILE_OUT}
    MAIN_DEPENDENCY ${DOXYFILE_IN}
    DEPENDS ${ENHANCEDENUM_HEADERS}
    COMMENT "Generating Doxygen docs")

  set(SPHINX_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR})
  set(SPHINX_BUILD "${CMAKE_CURRENT_BINARY_DIR}/sphinx")
  set(SPHINX_INDEX_FILE "${SPHINX_BUILD}/index.html")
  set(ENHANCEDENUM_SPHINX_CONFIG "${SPHINX_SOURCE_DIR}/conf.py")
  set(ENHANCEDENUM_PROJECT_README "${PROJECT_SOURCE_DIR}/README.rst")
  set(ENHANCEDENUM_PROJECT_CHANGELOG "${PROJECT_SOURCE_DIR}/CHANGELOG.rst")
  file(GLOB_RECURSE ENHANCEDENUM_RSTS "${SPHINX_SOURCE_DIR}/*.rst")
  file(GLOB_RECURSE ENHANCEDENUM_ENUMECG_PYS "${SPHINX_SOURCE_DIR}/../python/enumecg/*.py")
  file(GLOB_RECURSE ENHANCEDENUM_EXAMPLES "${SPHINX_SOURCE_DIR}/examples/*")
  add_custom_command(OUTPUT ${SPHINX_INDEX_FILE}
    COMMAND ${SPHINX_EXECUTABLE} -b html
    "-Dbreathe_projects.EnhancedEnum=${DOXYGEN_OUTPUT_DIR}/xml"
    ${SPHINX_SOURCE_DIR} ${SPHINX_BUILD}
    MAIN_DEPENDENCY ${ENHANCEDENUM_SPHINX_CONFIG}
    DEPENDS ${DOXYGEN_INDEX_FILE} ${ENHANCEDENUM_PROJECT_README}
      ${ENHANCEDENUM_PROJECT_CHANGELOG} ${ENHANCEDENUM_RSTS}
      ${ENHANCEDENUM_ENUMECG_PYS} ${ENHANCEDENUM_EXAMPLES}
    COMMENT "Generating Sphinx documentation")

  add_custom_target(docs ALL DEPENDS ${SPHINX_INDEX_FILE} ${DOXYGEN_INDEX_FILE})

  if (ENHANCEDENUM_BUILD_TESTS)
    add_test(NAME EnumECGDoctest
      COMMAND ${SPHINX_EXECUTABLE} -b doctest
        ${SPHINX_SOURCE_DIR} ${SPHINX_BUILD})
  endif()
else()
  message(STATUS "Doxygen and/or Sphinx not found. Skipping documentation.")
endif()
