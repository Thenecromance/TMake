cmake_minimum_required(VERSION 3.12)

##############################################
# using marco to pass the value from the function or marco
###############################################
macro(return_ res value)
    set(${result} ${RetVal} PARENT_SCOPE)
endmacro(return_ res value)

