cmake_minimum_required(VERSION 3.17)

# #############################################
# using marco to pass the value from the function or marco
# ##############################################
macro(return_ res value)
    set(${result} ${RetVal} PARENT_SCOPE)
endmacro(return_ res value)

macro(SET_MODULE text)
    set(LogModule ${text})
    message("Import ${LogModule} module")

    macro(TLog_ msg)
        TLog(${LogModule} ${msg})
    endmacro()

    macro(TLogError_ msg)
        TLog(${LogModule} ${msg})
        TLogErro(${LogModule} ${msg})
    endmacro(TLogError_ msg)
endmacro(SET_MODULE text)

macro(UN_SET)
    unset(${LogModule})
endmacro(UN_SET)

# ignore the CRT_SECURE_WARNING for WIN32
macro(IGNORE_CRT_WARNING)
    if(WIN32)
        add_definitions(-D_CRT_SECURE_NO_WARNINGS)
        TLog("BaseModule" "Ignoring the CRT SECURE WARNING")
    endif()
endmacro()

# set CXX VERSION for all sub project
macro(SET_CXX_VERSION ver)
    TLog("BaseModule" "Set CXX Version ${ver}")
    set(CXXVERSION ${ver})
endmacro()
