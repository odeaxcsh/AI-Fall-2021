cmake_minimum_required(VERSION 3.10)

project(ProblemSolver)

file(GLOB SOURCES "Game/*.cpp")
add_library(GAMELIB SHARED ${SOURCES})

add_executable(${PROJECT_NAME} App/main.cpp)

include_directories(${PROJECT_SOURCE_DIR})

target_link_libraries(${PROJECT_NAME} GAMELIB)
