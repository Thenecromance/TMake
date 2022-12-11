cmake_minimum_required(VERSION 3.17)

# Set the CMP0140 policy to NEW
message("Import TPython module")

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

# check this system does not support the python
# ``result``: if support it will return TRUE else return FALSE
function(TPythonSupport result)
    TPythonRun("--version" RetVal _)

    if(NOT ${RetVal} EQUAL 0)
        set(RetVal FALSE)
    else()
        set(RetVal TRUE)
    endif()

    return_(result RetVal)
endfunction(TPythonSupport)

# run Python script file with return value
# ``python_file``: script file
# ``result``: the python's return value
function(TPythonRun python_file result)
    SET_PYTHON()

    execute_process(
        COMMAND ${PYTHON_EXECUTABLE} ${python_file}
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        RESULT_VARIABLE RetVal
        OUTPUT_VARIABLE OutputVal
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
    TLog("Python" ${OutputVal})
    return_(result RetVal)
endfunction(TPythonRun)
