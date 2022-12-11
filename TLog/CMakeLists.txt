cmake_minimum_required(VERSION 3.17)

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
        string(TIMESTAMP cur_time "%H:%M:%S")
        message(WARNING "\n[TMAKE][${module}][ERROR][${cur_time}]:${text}")
    endif()
endmacro()
