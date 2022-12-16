cmake_minimum_required(VERSION 3.17)

# set the Default version for all subproject
set(CXXVERSION 17)

# using a easy way to include the other CMakeLists.txt
macro(TINCLUDE file)
    include(${CMAKE_SOURCE_DIR}/TMake/${file}/CMakeLists.txt)
endmacro(TINCLUDE file)

TINCLUDE(TLog) # Logs
TINCLUDE(TMacro)
TINCLUDE(TProject) # more easy way to build Project and subproject
TINCLUDE(TPython) # execute python script project
TINCLUDE(TConfigFile)

function(TRunBootstrap)
    TPythonSupport(result)
    if( ${result} EQUAL FALSE)
        TLogError("Base " "could not support the Python")
    else()
        if((NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/.bootstrap_path.json") OR("${CMAKE_CURRENT_SOURCE_DIR}/CMakeLists.txt" IS_NEWER_THAN "${CMAKE_CURRENT_SOURCE_DIR}/deps/.bootstrap_path.json"))
            TPythonRun("TMake//python//TLoader.py" result)
            if(NOT (${result} EQUAL 0))
                TLogError("Base" "Run Bootstrap.py failed")
            endif()
        endif()
    endif()
endfunction()

TLog("Monkey" "Monkey Maker! I'm Monkey!")