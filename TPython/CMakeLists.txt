cmake_minimum_required(VERSION 3.12)

# Set the CMP0140 policy to NEW
message("Import TPython module")

cmake_policy(SET CMP0140 NEW)


# prepare to use python
macro(SET_PYTHON)
    if(NOT DEFINED PYTHON_EXECUTABLE)
        if(WIN32)
            set(PYTHON_EXECUTABLE "python" CACHE STRING "")
        else()
            set(PYTHON_EXECUTABLE "python3" CACHE STRING "")
        endif()
    endif()
endmacro(SET_PYTHON)

# #
function(check_python_support result)
    run_python("--version" RetVal)
    return_(result RetVal)
endfunction(check_python_support)

function(run_python python_file result)
    SET_PYTHON()
    execute_process(
        COMMAND ${PYTHON_EXECUTABLE} ${python_file}
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        RESULT_VARIABLE RetVal
    )
    return_(result RetVal)
endfunction(run_python)
