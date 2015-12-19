#!/usr/bin/env python

from distutils.spawn import find_executable
import os
import subprocess
import sys

DOWNLOAD_DIRECTORY = "ExternalDownloads"

class Dependency(object):

    def __init__(self, dep_name, dep_url, dep_location):
        self.name = dep_name
        self.url = dep_url
        self.location = dep_location


def clone(git, url, location):
    try:
        subprocess.call([git, 'clone', url, location])
    except AttributeError as error:    
        print error
        
def main(argv):
    git_path = find_executable('git')
    
    dependencies = [Dependency('llvm', 'http://llvm.org/git/llvm.git',
                               'llvm'), Dependency('clang',
                                                   'http://llvm.org/git/clang.git',
                                                   'clang')]
    

    for dependency in dependencies:
        clone(git_path, dependency.url,
              os.path.join(DOWNLOAD_DIRECTORY, dependency.location))
        
    
if __name__ == "__main__":
    sys.exit(main(sys.argv))
