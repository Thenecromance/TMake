cmake_minimum_required(VERSION 3.17)
SET_MODULE("TLog")

# this module is for wrap the message(...)
# just because some wrong message sometimes is too
# difficult to find in Cmake log
set(SHOW_LOG TRUE CACHE BOOL "")

function(TLog module text)
    if(${SHOW_LOG})
        string(TIMESTAMP cur_time "%H:%M:%S")
        message("[TMAKE][${module}][INFO][${cur_time}]:${text}")
    endif()
endfunction()

function(TLogError module message)
    if(${SHOW_LOG})
        string(TIMESTAMP cur_time "%H:%M:%S")
        message(WARNING "\n[TMAKE][${module}][ERROR][${cur_time}]:${text}")
    endif()
endfunction()

UN_SET()