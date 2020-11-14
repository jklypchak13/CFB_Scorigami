"""
This file is designed to account for the fact that we have a src and test directory.
It's necessary to add the specified relative path to each test file so that our tests
can access the source code under test. When righting a test it's necessary to add the
line

from . import context

to ensure that the tests can access the source code. If you have questions about this file
please feel free to.
"""
import sys
sys.path.append('./src/')
