cmake_minimum_required(VERSION 3.12)

# Set the CMP0140 policy to NEW
message("Import TPython module")

# cmake_policy(SET CMP0140 NEW)
macro(return_)
    set(${ARGS} ${ARGN} PARENT_SCOPE)
    return()
endmacro()

macro(SET_PYTHON)
    if(NOT DEFINED PYTHON_EXECUTABLE)
        if(WIN32)
            set(PYTHON_EXECUTABLE "python" CACHE STRING "")
        else()
            set(PYTHON_EXECUTABLE "python3" CACHE STRING "")
        endif()
    endif()
endmacro(SET_PYTHON)

function(check_python_support)
    run_python("--version" python_check_result)
    return_("${python_check_result}")
endfunction(check_python_support)

function(run_python python_file)
    SET_PYTHON()
    execute_process(
        COMMAND ${PYTHON_EXECUTABLE} ${python_file}
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        RESULT_VARIABLE python_check_result
    )
    return_("${python_check_result}")
endfunction(run_python)
