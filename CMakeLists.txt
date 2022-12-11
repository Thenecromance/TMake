cmake_minimum_required(VERSION 3.12)

set(CXXVERSION 17)

macro(TINCLUDE file)
    include(./TMake/${file}/CMakeLists.txt)
endmacro(TINCLUDE file)

TINCLUDE(TMacro)
TINCLUDE(TLog) # Logs
TINCLUDE(TProject) # more easy way to build Project and subproject
TINCLUDE(TPython) # execute python script project

# ignore the CRT_SECURE_WARNING for WIN32
macro(IGNORE_CRT_WARNING)
    if(WIN32)
        add_definitions(-D_CRT_SECURE_NO_WARNINGS)
        LOG_INFO("BaseModule" "Ignoring the CRT SECURE WARNING")
    endif()
endmacro(IGNORE_CRT_WARNING)

# set CXX VERSION for all sub project
macro(SET_CXX_VERSION ver)
    LOG_INFO("BaseModule" "Set CXX Version ${ver}")
    set(CXXVERSION ${ver})
endmacro(SET_CXX_VERSION ver)
