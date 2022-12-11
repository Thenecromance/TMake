# TMake
CMake macros 
## 0x00 TConfigFile 
This part codes is only working for operate config.h.in and config.h
-----------
Macro List 
| MarcoName | ArgsName | Explain|
|--------------------|------------|------------|
|TConfigFileStart |config_name | set the config where I want to put those auto generated macros|
|TConfigFileSet | key value | add macros define|
|TConfigFileSetNone| key | set macro without value |
|TConfigFileWrite| None | write to the config file |
|TConfigFileRelease | None | release all the vars from the cache|
|TConfigFileAuto |None | output all key:value for direct copy to the xxxx.h.in|
|TAPPEND | string | a lazy guy do the bugged lazy thing|
 
 ## 0x01 TLog
 to make message more simple and easy to use 
 ---------
 Macro List 
| MarcoName | ArgsName | Explain|
|--------------------|------------|------------|
|SHOW_LOG |SHOW_LOG | if this value set FALSE TLog won't output any thing|
|TLog |module msg | **module**  means which I called  **msg** Log Messages |
|TLogError | module msg | **module**  means which I called  **msg** Log Messages |


## 0x02 TProject
for build Project and subproject etc
---------
 Macro List 
| MarcoName | ArgsName | Explain|
|--------------------|------------|------------|
|SETUP_GROUPS|src_files |merge each src in one group|
|SET_OUTPUT_NAMES | prj_name| auto generate the configuration |
|TProjectBuild |prj_name| create a project which name is **prj_name**|
|TBUILD_EXE |prj_name | create a executeable project|
|TBUILD_LIB|prj_name | create a static lib project |
|TBUILD_SHARED| prj_name| create a shared lib project |

## 0x03 TPython
run python script from CMakeLists.txt to replace some operations in CMakeLists.txt *download git,resources etc*
---------
 Macro List 
| MarcoName | ArgsName | Explain|
|--------------------|------------|------------|
|SET_PYTHON| None | set the Python command for different OS|
|TPythonSupport| None | Check OS support Python or not |
|TPythonRun |python result | **python** run command, or file **result** return the script value to check is working right or not | 

## 0x04 TMacro 
some tiny marcos in here 
---------
 Macro List 
| MarcoName | ArgsName | Explain|
|--------------------|------------|------------|
|return_|res value| this macro is mainly to replace the `return()` which is support by CMake |
|SET_MODULE| Module | I just don't want to use `TLog(Module msg)` after call the macro, in CMakeList can use `TLog_(msg)` as I want |
|UN_SET | None | Unload Module Name |

## 0x05 TMake 
some tiny marcos in here 
---------
 Macro List 
| MarcoName | ArgsName | Explain|
|--------------------|------------|------------|
|IGNORE_CRT_WARNING| None | Ignore CRT_SECURE_WARNING for windows|
|SET_CXX_VERSION |CXXVERSION | to setup all subproject CXX VERSION as the same one |
