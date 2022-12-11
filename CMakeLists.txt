cmake_minimum_required(VERSION 3.12)

set(CXXVERSION 17)



macro(TINCLUDE file)
    include(./TMake/${file}/CMakeLists.txt)
endmacro(TINCLUDE file)

TINCLUDE(TLog)
TINCLUDE(TProject)

# Excute the Bootstrap.py
function(Bootstrap json)
    if(WIN32)
        set(PYTHON_EXECUTABLE "python")
    else()
        set(PYTHON_EXECUTABLE "python3")
    endif()

    if((NOT EXISTS json_file) OR("${CMAKE_CURRENT_SOURCE_DIR}/CMakeLists.txt" IS_NEWER_THAN json_file))
        execute_process(
            COMMAND ${PYTHON_EXECUTABLE} "bootstrap.py"
            WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
            RESULT_VARIABLE bootstrap_result
        )

        if(NOT(${bootstrap_result} EQUAL 0))
            message(FATAL_ERROR "Cannot run bootstrap.py")
        endif()
    endif()
endfunction(Bootstrap)

# ignore the CRT_SECURE_WARNING for WIN32
macro(IGNORE_CRT_WARNING)
    if(WIN32)
        add_definitions(-D_CRT_SECURE_NO_WARNINGS)
        LOG_INFO("Ignoring the CRT SECURE WARNING")
    endif()
endmacro(IGNORE_CRT_WARNING)

# set project compile as executeable
macro(SET_EXE prjname)
    SETUP_APP(${prjname})
endmacro(SET_EXE)

# set project compile as static lib
macro(SET_STACTIC prjname)
    set(TBUILD_STATIC TRUE)
    set(TBUILD_SHARED FALSE)
    SETUP_APP(${prjname})
endmacro(SET_STACTIC prjname)

# set project compile as shared lib
macro(SET_SHARE prjname)
    set(TBUILD_STATIC FALSE)
    set(TBUILD_SHARED TRUE)
    SETUP_APP(${prjname})
endmacro(SET_SHARE prjname)

# set CXX VERSION for all sub project
macro(SET_CXX_VERSION ver)
    LOG_INFO("Set CXX Version ${ver}")
    set(CXXVERSION ${ver})
endmacro(SET_CXX_VERSION ver)
