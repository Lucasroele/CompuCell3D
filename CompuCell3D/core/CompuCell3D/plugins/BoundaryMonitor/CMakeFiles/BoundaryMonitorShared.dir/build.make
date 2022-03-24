# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.19

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Disable VCS-based implicit rules.
% : %,v


# Disable VCS-based implicit rules.
% : RCS/%


# Disable VCS-based implicit rules.
% : RCS/%,v


# Disable VCS-based implicit rules.
% : SCCS/s.%


# Disable VCS-based implicit rules.
% : s.%


.SUFFIXES: .hpux_make_needs_suffix_list


# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /geode2/home/u060/mehtasau/Carbonate/miniconda3/envs/cc3denv/bin/cmake

# The command to remove a file.
RM = /geode2/home/u060/mehtasau/Carbonate/miniconda3/envs/cc3denv/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /N/u/mehtasau/Carbonate/CC3D_PY3_GIT/CompuCell3D/CompuCell3D

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /N/u/mehtasau/Carbonate/CC3D_PY3_GIT/CompuCell3D/CompuCell3D

# Include any dependencies generated for this target.
include core/CompuCell3D/plugins/BoundaryMonitor/CMakeFiles/BoundaryMonitorShared.dir/depend.make

# Include the progress variables for this target.
include core/CompuCell3D/plugins/BoundaryMonitor/CMakeFiles/BoundaryMonitorShared.dir/progress.make

# Include the compile flags for this target's objects.
include core/CompuCell3D/plugins/BoundaryMonitor/CMakeFiles/BoundaryMonitorShared.dir/flags.make

core/CompuCell3D/plugins/BoundaryMonitor/CMakeFiles/BoundaryMonitorShared.dir/BoundaryMonitorPlugin.cpp.o: core/CompuCell3D/plugins/BoundaryMonitor/CMakeFiles/BoundaryMonitorShared.dir/flags.make
core/CompuCell3D/plugins/BoundaryMonitor/CMakeFiles/BoundaryMonitorShared.dir/BoundaryMonitorPlugin.cpp.o: core/CompuCell3D/plugins/BoundaryMonitor/BoundaryMonitorPlugin.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/N/u/mehtasau/Carbonate/CC3D_PY3_GIT/CompuCell3D/CompuCell3D/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object core/CompuCell3D/plugins/BoundaryMonitor/CMakeFiles/BoundaryMonitorShared.dir/BoundaryMonitorPlugin.cpp.o"
	cd /N/u/mehtasau/Carbonate/CC3D_PY3_GIT/CompuCell3D/CompuCell3D/core/CompuCell3D/plugins/BoundaryMonitor && /N/soft/rhel7/gcc/6.3.0/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/BoundaryMonitorShared.dir/BoundaryMonitorPlugin.cpp.o -c /N/u/mehtasau/Carbonate/CC3D_PY3_GIT/CompuCell3D/CompuCell3D/core/CompuCell3D/plugins/BoundaryMonitor/BoundaryMonitorPlugin.cpp

core/CompuCell3D/plugins/BoundaryMonitor/CMakeFiles/BoundaryMonitorShared.dir/BoundaryMonitorPlugin.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/BoundaryMonitorShared.dir/BoundaryMonitorPlugin.cpp.i"
	cd /N/u/mehtasau/Carbonate/CC3D_PY3_GIT/CompuCell3D/CompuCell3D/core/CompuCell3D/plugins/BoundaryMonitor && /N/soft/rhel7/gcc/6.3.0/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /N/u/mehtasau/Carbonate/CC3D_PY3_GIT/CompuCell3D/CompuCell3D/core/CompuCell3D/plugins/BoundaryMonitor/BoundaryMonitorPlugin.cpp > CMakeFiles/BoundaryMonitorShared.dir/BoundaryMonitorPlugin.cpp.i

core/CompuCell3D/plugins/BoundaryMonitor/CMakeFiles/BoundaryMonitorShared.dir/BoundaryMonitorPlugin.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/BoundaryMonitorShared.dir/BoundaryMonitorPlugin.cpp.s"
	cd /N/u/mehtasau/Carbonate/CC3D_PY3_GIT/CompuCell3D/CompuCell3D/core/CompuCell3D/plugins/BoundaryMonitor && /N/soft/rhel7/gcc/6.3.0/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /N/u/mehtasau/Carbonate/CC3D_PY3_GIT/CompuCell3D/CompuCell3D/core/CompuCell3D/plugins/BoundaryMonitor/BoundaryMonitorPlugin.cpp -o CMakeFiles/BoundaryMonitorShared.dir/BoundaryMonitorPlugin.cpp.s

core/CompuCell3D/plugins/BoundaryMonitor/CMakeFiles/BoundaryMonitorShared.dir/BoundaryMonitorPluginProxy.cpp.o: core/CompuCell3D/plugins/BoundaryMonitor/CMakeFiles/BoundaryMonitorShared.dir/flags.make
core/CompuCell3D/plugins/BoundaryMonitor/CMakeFiles/BoundaryMonitorShared.dir/BoundaryMonitorPluginProxy.cpp.o: core/CompuCell3D/plugins/BoundaryMonitor/BoundaryMonitorPluginProxy.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/N/u/mehtasau/Carbonate/CC3D_PY3_GIT/CompuCell3D/CompuCell3D/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object core/CompuCell3D/plugins/BoundaryMonitor/CMakeFiles/BoundaryMonitorShared.dir/BoundaryMonitorPluginProxy.cpp.o"
	cd /N/u/mehtasau/Carbonate/CC3D_PY3_GIT/CompuCell3D/CompuCell3D/core/CompuCell3D/plugins/BoundaryMonitor && /N/soft/rhel7/gcc/6.3.0/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/BoundaryMonitorShared.dir/BoundaryMonitorPluginProxy.cpp.o -c /N/u/mehtasau/Carbonate/CC3D_PY3_GIT/CompuCell3D/CompuCell3D/core/CompuCell3D/plugins/BoundaryMonitor/BoundaryMonitorPluginProxy.cpp

core/CompuCell3D/plugins/BoundaryMonitor/CMakeFiles/BoundaryMonitorShared.dir/BoundaryMonitorPluginProxy.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/BoundaryMonitorShared.dir/BoundaryMonitorPluginProxy.cpp.i"
	cd /N/u/mehtasau/Carbonate/CC3D_PY3_GIT/CompuCell3D/CompuCell3D/core/CompuCell3D/plugins/BoundaryMonitor && /N/soft/rhel7/gcc/6.3.0/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /N/u/mehtasau/Carbonate/CC3D_PY3_GIT/CompuCell3D/CompuCell3D/core/CompuCell3D/plugins/BoundaryMonitor/BoundaryMonitorPluginProxy.cpp > CMakeFiles/BoundaryMonitorShared.dir/BoundaryMonitorPluginProxy.cpp.i

core/CompuCell3D/plugins/BoundaryMonitor/CMakeFiles/BoundaryMonitorShared.dir/BoundaryMonitorPluginProxy.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/BoundaryMonitorShared.dir/BoundaryMonitorPluginProxy.cpp.s"
	cd /N/u/mehtasau/Carbonate/CC3D_PY3_GIT/CompuCell3D/CompuCell3D/core/CompuCell3D/plugins/BoundaryMonitor && /N/soft/rhel7/gcc/6.3.0/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /N/u/mehtasau/Carbonate/CC3D_PY3_GIT/CompuCell3D/CompuCell3D/core/CompuCell3D/plugins/BoundaryMonitor/BoundaryMonitorPluginProxy.cpp -o CMakeFiles/BoundaryMonitorShared.dir/BoundaryMonitorPluginProxy.cpp.s

# Object files for target BoundaryMonitorShared
BoundaryMonitorShared_OBJECTS = \
"CMakeFiles/BoundaryMonitorShared.dir/BoundaryMonitorPlugin.cpp.o" \
"CMakeFiles/BoundaryMonitorShared.dir/BoundaryMonitorPluginProxy.cpp.o"

# External object files for target BoundaryMonitorShared
BoundaryMonitorShared_EXTERNAL_OBJECTS =

core/CompuCell3D/plugins/BoundaryMonitor/libCC3DBoundaryMonitor.so: core/CompuCell3D/plugins/BoundaryMonitor/CMakeFiles/BoundaryMonitorShared.dir/BoundaryMonitorPlugin.cpp.o
core/CompuCell3D/plugins/BoundaryMonitor/libCC3DBoundaryMonitor.so: core/CompuCell3D/plugins/BoundaryMonitor/CMakeFiles/BoundaryMonitorShared.dir/BoundaryMonitorPluginProxy.cpp.o
core/CompuCell3D/plugins/BoundaryMonitor/libCC3DBoundaryMonitor.so: core/CompuCell3D/plugins/BoundaryMonitor/CMakeFiles/BoundaryMonitorShared.dir/build.make
core/CompuCell3D/plugins/BoundaryMonitor/libCC3DBoundaryMonitor.so: core/CompuCell3D/libCC3DCompuCellLib.so
core/CompuCell3D/plugins/BoundaryMonitor/libCC3DBoundaryMonitor.so: core/CompuCell3D/Potts3D/libCC3DPotts3D.so
core/CompuCell3D/plugins/BoundaryMonitor/libCC3DBoundaryMonitor.so: core/muParser/ExpressionEvaluator/libCC3DExpressionEvaluator.so
core/CompuCell3D/plugins/BoundaryMonitor/libCC3DBoundaryMonitor.so: core/muParser/libCC3DmuParser.so
core/CompuCell3D/plugins/BoundaryMonitor/libCC3DBoundaryMonitor.so: core/PublicUtilities/libCC3DPublicUtilities.so
core/CompuCell3D/plugins/BoundaryMonitor/libCC3DBoundaryMonitor.so: core/PublicUtilities/Units/libCC3DUnits.so
core/CompuCell3D/plugins/BoundaryMonitor/libCC3DBoundaryMonitor.so: core/CompuCell3D/Automaton/libCC3DAutomaton.so
core/CompuCell3D/plugins/BoundaryMonitor/libCC3DBoundaryMonitor.so: core/CompuCell3D/Boundary/libCC3DBoundary.so
core/CompuCell3D/plugins/BoundaryMonitor/libCC3DBoundaryMonitor.so: core/CompuCell3D/Field3D/libCC3DField3D.so
core/CompuCell3D/plugins/BoundaryMonitor/libCC3DBoundaryMonitor.so: core/XMLUtils/libCC3DXMLUtils.so
core/CompuCell3D/plugins/BoundaryMonitor/libCC3DBoundaryMonitor.so: core/BasicUtils/libCC3DBasicUtils.so
core/CompuCell3D/plugins/BoundaryMonitor/libCC3DBoundaryMonitor.so: core/CompuCell3D/plugins/BoundaryMonitor/CMakeFiles/BoundaryMonitorShared.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/N/u/mehtasau/Carbonate/CC3D_PY3_GIT/CompuCell3D/CompuCell3D/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Linking CXX shared library libCC3DBoundaryMonitor.so"
	cd /N/u/mehtasau/Carbonate/CC3D_PY3_GIT/CompuCell3D/CompuCell3D/core/CompuCell3D/plugins/BoundaryMonitor && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/BoundaryMonitorShared.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
core/CompuCell3D/plugins/BoundaryMonitor/CMakeFiles/BoundaryMonitorShared.dir/build: core/CompuCell3D/plugins/BoundaryMonitor/libCC3DBoundaryMonitor.so

.PHONY : core/CompuCell3D/plugins/BoundaryMonitor/CMakeFiles/BoundaryMonitorShared.dir/build

core/CompuCell3D/plugins/BoundaryMonitor/CMakeFiles/BoundaryMonitorShared.dir/clean:
	cd /N/u/mehtasau/Carbonate/CC3D_PY3_GIT/CompuCell3D/CompuCell3D/core/CompuCell3D/plugins/BoundaryMonitor && $(CMAKE_COMMAND) -P CMakeFiles/BoundaryMonitorShared.dir/cmake_clean.cmake
.PHONY : core/CompuCell3D/plugins/BoundaryMonitor/CMakeFiles/BoundaryMonitorShared.dir/clean

core/CompuCell3D/plugins/BoundaryMonitor/CMakeFiles/BoundaryMonitorShared.dir/depend:
	cd /N/u/mehtasau/Carbonate/CC3D_PY3_GIT/CompuCell3D/CompuCell3D && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /N/u/mehtasau/Carbonate/CC3D_PY3_GIT/CompuCell3D/CompuCell3D /N/u/mehtasau/Carbonate/CC3D_PY3_GIT/CompuCell3D/CompuCell3D/core/CompuCell3D/plugins/BoundaryMonitor /N/u/mehtasau/Carbonate/CC3D_PY3_GIT/CompuCell3D/CompuCell3D /N/u/mehtasau/Carbonate/CC3D_PY3_GIT/CompuCell3D/CompuCell3D/core/CompuCell3D/plugins/BoundaryMonitor /N/u/mehtasau/Carbonate/CC3D_PY3_GIT/CompuCell3D/CompuCell3D/core/CompuCell3D/plugins/BoundaryMonitor/CMakeFiles/BoundaryMonitorShared.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : core/CompuCell3D/plugins/BoundaryMonitor/CMakeFiles/BoundaryMonitorShared.dir/depend

