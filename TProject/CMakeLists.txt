cmake_minimum_required(VERSION 3.17)

SET_MODULE(TProject)

macro(SETUP_GROUPS src_files)
    foreach(FILE ${src_files})
        get_filename_component(PARENT_DIR "${FILE}" PATH)

        set(GROUP "${PARENT_DIR}")
        string(REPLACE "/" "\\" GROUP "${GROUP}")

        source_group("${GROUP}" FILES "${FILE}")
    endforeach()
endmacro()

macro(SET_OUTPUT_NAMES prj_name)
    set_target_properties(${prj_name} PROPERTIES OUTPUT_NAME_DEBUG ${prj_name}_Debug)
    set_target_properties(${prj_name} PROPERTIES OUTPUT_NAME_RELEASE ${prj_name}_Release)
    set_target_properties(${prj_name} PROPERTIES OUTPUT_NAME_RELWITHDEBINFO ${prj_name}_ReleaseDebInfo)

    # On Linux/macOS the binaries go to <root>/bin folder
    if(UNIX)
        set_target_properties(${prj_name} PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/bin")
    endif()
endmacro()

# build a auto build project, which will auto include all source from src&include directories
macro(TProjectBuild prj_name)
    set(FOLDER_NAME ${prj_name})
    set(PROJECT_NAME ${prj_name})
    project(${PROJECT_NAME} CXX)

    file(GLOB_RECURSE SRC_FILES LIST_DIRECTORIES false RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} src/*.c??)
    file(GLOB_RECURSE HEADER_FILES LIST_DIRECTORIES false RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} include/*.h??)

    include_directories(src)
    include_directories(include)

    if(${TBUILD_STATIC} AND ${TBUILD_SHARED})
        TLog_("TBUILD_STATIC and TBUILD_SHARED should not be both true")
    endif()

    if(${TBUILD_STATIC})
        TLog_("${PROJECT_NAME} compile as static lib")
        add_library(${PROJECT_NAME} STATIC ${SRC_FILES} ${HEADER_FILES})
    elseif(${TBUILD_SHARED})
        TLog_("${PROJECT_NAME} compile as shared lib")
        add_library(${PROJECT_NAME} SHARED ${SRC_FILES} ${HEADER_FILES})
    else()
        TLog_("${PROJECT_NAME} compile as executeable")
        add_executable(${PROJECT_NAME} ${SRC_FILES} ${HEADER_FILES})
    endif()

    if(MSVC)
        add_definitions(-D_CONSOLE)
    endif()

    SETUP_GROUPS("${SRC_FILES}")
    SETUP_GROUPS("${HEADER_FILES}")

    SET_OUTPUT_NAMES(${PROJECT_NAME})
    set_property(TARGET ${PROJECT_NAME} PROPERTY FOLDER ${FOLDER_NAME})

    set_property(TARGET ${PROJECT_NAME} PROPERTY CXX_STANDARD ${CXXVERSION})
    set_property(TARGET ${PROJECT_NAME} PROPERTY CXX_STANDARD_REQUIRED ON)

    if(MSVC)
        set_property(TARGET ${PROJECT_NAME} PROPERTY VS_DEBUGGER_WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}")
    endif()
endmacro()

# set project compile as executeable
macro(TBUILD_EXE prjname)
    TProjectBuild(${prjname})
endmacro(TBUILD_EXE)

# set project compile as static lib
macro(TBUILD_LIB prjname)
    set(TBUILD_STATIC TRUE)
    set(TBUILD_SHARED FALSE)
    TProjectBuild(${prjname})
endmacro(TBUILD_LIB prjname)

# set project compile as shared lib
macro(TBUILD_SHARED prjname)
    set(TBUILD_STATIC FALSE)
    set(TBUILD_SHARED TRUE)
    TProjectBuild(${prjname})
endmacro(TBUILD_SHARED prjname)

# add all sub directories in parent_dir
# @parent_dir: root directory
macro(TADD_SUBDIRECTORY parent_dir)
    file(GLOB_RECURSE DIR_LIST LIST_DIRECTORIES true RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} ${parent_dir})

    foreach(SUB_DIR ${DIR_LIST})
        include_directories(${SUB_DIR})
    endforeach(SUB_DIR ${DIR_LIST})
endmacro()