cmake_minimum_required(VERSION 3.12)


# this module is for wrap the message(...) 
# just because some wrong message sometimes is too 
# difficult to find in Cmake log 


set(SHOW_LOG TRUE CACHE BOOL "")

message("Import TLog module")

macro(TLog module text)
    if(${SHOW_LOG})
        string(TIMESTAMP cur_time "%H:%M:%S")
        message("[TMAKE][${module}][INFO][${cur_time}]:${text}")
    endif()
endmacro(TLog text)

macro(TLogError module message)
    if(${SHOW_LOG})
        EMPTY_LINE()
        string(TIMESTAMP cur_time "%H:%M:%S")
        message(FATAL_ERROR "[TMAKE][${module}][INFO][${cur_time}]:${text}")
        EMPTY_LINE()
    endif()
endmacro()

#only print a new Line 
macro(EMPTY_LINE)
    if(${SHOW_LOG})
        message("")
    endif()
endmacro()