"""Test suite initialisation for the Ottoneu GM Operating System.

This package makes the project code importable by appending the repository
root to ``sys.path``.  Without this adjustment the ``backend`` package
would not be discoverable when running pytest directly.  Tests live in
this package so that pytest can discover them when running ``make test``.
"""

import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)