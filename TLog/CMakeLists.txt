cmake_minimum_required(VERSION 3.17)




# this module is for wrap the message(...)
# just because some wrong message sometimes is too
# difficult to find in Cmake log
set(SHOW_LOG TRUE CACHE BOOL "")

function(TLog module msg)
    if(${SHOW_LOG})
        string(TIMESTAMP cur_time "%H:%M:%S")
        message("[Monkey][${module}][INFO][${cur_time}]:${msg}")
    endif()
endfunction()

function(TLogError module msg)
    if(${SHOW_LOG})
        string(TIMESTAMP cur_time "%H:%M:%S")
        message(WARNING "\n[Monkey][${module}][ERROR][${cur_time}]:${msg}")
    endif()
endfunction()
