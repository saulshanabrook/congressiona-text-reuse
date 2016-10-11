# assuming this is run by pytest: http://doc.pytest.org/en/latest/
# e.g.
# py.test tests/unittests.py
# or
# py.test -s tests/unittests.py

import sys,os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import pytest
from shingling import make_windows

def test_windows():
    
    windows = [o for o in make_windows(range(4), 2)]
    print windows
    assert windows[0] == [0, 1]
    assert windows[1] == [2, 3]
    assert len(windows) == 2
