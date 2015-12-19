#!/usr/bin/env python

import errno
import os
import shutil
import subprocess
import sys

from distutils.spawn import find_executable
from utilities import log_error

START_DIRECTORY = os.path.abspath(os.path.curdir)
DOWNLOAD_DIRECTORY = os.path.join(START_DIRECTORY, "ExternalDownloads")
SOURCE_DIRECTORY = os.path.join(START_DIRECTORY, "Sources")
WORKSPACE = os.path.join(START_DIRECTORY, "Workspace")
BUILD_DIRECTORY = os.path.join(WORKSPACE, "Build")

TOOL_DEPENDENCIES = ['clang', 'cmake']

DEPENDENCY_DIRECTORY_MAP = [('llvm', 'llvm'),
                            ('clang', 'llvm/tools/clang')]
SOURCE_DIRECTORY_MAP = [('Sources', 'test-check')]

def check_tools():
    tool_paths = []
    for dependency in TOOL_DEPENDENCIES:
        tool_paths.append((dependency, find_executable(dependency)))
        if tool_paths[-1][1] is None:
            log_error("Missing tool: " + dependency)
            return None

    return tool_paths


def check_dependencies():
    if not os.path.isdir(DOWNLOAD_DIRECTORY):
        log_error("External Download directory does not exist")
        return 1

    for dependency in DEPENDENCY_DIRECTORY_MAP:
        path = os.path.join(DOWNLOAD_DIRECTORY, dependency[0])
        if not os.path.isdir(path):
            log_error(dependency[0] + " could not be found")
            return 1
        else:
            print "Found " + dependency[0] + ":"
            print path


def organise_source():
    sources_path = DOWNLOAD_DIRECTORY
    for source in DEPENDENCY_DIRECTORY_MAP:
        try:
            source_path = os.path.join(sources_path, source[0])
            destination_path = os.path.join(WORKSPACE, source[1])
            print "Copying " + source[0] + " to: " + destination_path
            shutil.copytree(source_path, destination_path)
        except OSError, os_error:
            if os_error.errno == errno.EEXIST:
                pass


def configure():
    if os.path.isdir(BUILD_DIRECTORY) == False:
        os.mkdir(BUILD_DIRECTORY)
    
    os.chdir(BUILD_DIRECTORY)

    # To build LLVM you need to point to the directory
    workspace_sources_path = os.path.join(WORKSPACE, 'llvm')
    cmake_command = ['cmake', '-GNinja', workspace_sources_path,
                     '-DLLVM_EXTERNAL_CLANG_TOOLS_EXTRA_SOURCE_DIR='
                     + SOURCE_DIRECTORY]
    print "Running command: " + " ".join(cmake_command)
    subprocess.call(cmake_command)


def build():
    os.chdir(BUILD_DIRECTORY)
    cmake_command = ['ninja', 'test-check']
    print "Running command: " + " ".join(cmake_command)
    subprocess.call(cmake_command)


def main(argv):
    tool_paths = check_tools()

    if tool_paths is None:
        log_error("Could not find any required tools")
        return 1

    print "Tool Paths"
    print "----------"
    for tool in tool_paths:
        print tool[0] + ': ' + tool[1]

    check_dependencies()
    organise_source()
    configure()
    build()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
