cmake_minimum_required(VERSION 3.17)

# set the Default version for all subproject
set(CXXVERSION 17)

# using a easy way to include the other CMakeLists.txt
macro(TINCLUDE file)
    include(${CMAKE_CURRENT_SOURCE_DIR}/${file}/CMakeLists.txt)
endmacro(TINCLUDE file)

TINCLUDE(TMacro)
TINCLUDE(TLog) # Logs
TINCLUDE(TProject) # more easy way to build Project and subproject
TINCLUDE(TPython) # execute python script project
TINCLUDE(TConfigFile)
# ignore the CRT_SECURE_WARNING for WIN32
macro(IGNORE_CRT_WARNING)
    if(WIN32)
        add_definitions(-D_CRT_SECURE_NO_WARNINGS)
        LOG_INFO("BaseModule" "Ignoring the CRT SECURE WARNING")
    endif()
endmacro()

# set CXX VERSION for all sub project
macro(SET_CXX_VERSION ver)
    LOG_INFO("BaseModule" "Set CXX Version ${ver}")
    set(CXXVERSION ${ver})
endmacro()

# # # ##############################
# project(ConfigFileTest)
# TConfigFileStart(config)
# TConfigFileSet(Author "Thenecromance")
# TConfigFileSet(Major 1)
# TConfigFileSet(Minor 1)
# TConfigFileSetNone(Test)
# # TConfigFileAuto()
# TConfigFileWrite()
# # TConfigFileDebug()

# # # ##############################

# # ##############################
# # Python Test Case
# TPythonSupport(bSupport)
# if(${bSupport})
# TPythonRun("${CMAKE_CURRENT_SOURCE_DIR}\\Test\\HelloWorld.py" result )
# endif()
# message(${CMAKE_CURRENT_SOURCE_DIR})
# # ##############################

