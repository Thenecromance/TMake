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
    
endmacro(SET_MODULE text)

macro(UN_SET)
    unset(${LogModule})
endmacro(UN_SET)
