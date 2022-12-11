cmake_minimum_required(VERSION 3.17)
SET_MODULE(TConfigFile)

# start to configureation files
macro(TConfigFileStart config_name)
    TLog_("Start")

    set(configName ${config_name}.h CACHE STRING "")
endmacro()

# set the arg define with value
macro(TConfigFileSet key value)
    set(${key} "${value}")
    list(APPEND _configLists ${key})
    TLog_("Append ${key} :${value}")
endmacro()

# set the arg in define just like #define key
macro(TConfigFileSetNone key)
    option(${key} "keys without value" ON)
    list(APPEND _configLists ${key})
endmacro(TConfigFileSetNone key)

# write all the configureation to the ${configName}.h.in
macro(TConfigFileWrite)
    TLog_("start to write the ${configName}")
    configure_file(${configName}.in ${configName} @ONLY)
    TConfigFileRelease()
endmacro()

# relase all stuff about the ConfigFile
macro(TConfigFileRelease)
    TLog_("Released the vars")

    foreach(Key IN LISTS _configLists)
        unset(${Key})
    endforeach()

    unset(_configLists) # release the List which saved each params
    unset(configName) # release config
endmacro()

macro(TConfigFileAuto)
    foreach(Key IN LISTS _configLists)
        if(DEFINED ${Key})
            string(APPEND config_in "#cmakedefine ${Key} \"@${Key}@\"\n")
        else()
            string(APPEND config_in "#cmakedefine ${Key}\n")
        endif()
    endforeach()

    TLog_("you can write the ${config_name}.h.in just like below:\n${config_in}")
endmacro()

macro(TAPPEND key)
    list(APPEND _configLists ${key}) # just I'm too lazy....
endmacro(TAPPEND key)

UN_SET()

# only for debug
# macro(TConfigFileDebug)
# foreach(Key IN LISTS _configLists)
# TLog_("Debug ${Key}")
# endforeach()
# endmacro(TConfigFileDebug)
