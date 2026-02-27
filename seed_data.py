"""Compatibility wrapper for running demo seed scripts.

This module simply forwards to ``backend.app.seed_data`` so that the
``make seed`` target continues to work even when the seed logic lives in
the backend package.  Feel free to execute ``python -m backend.app.seed_data``
directly instead of using this wrapper.
"""

from backend.app.seed_data import seed_demo


if __name__ == "__main__":
    seed_demo()