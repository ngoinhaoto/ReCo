import sys


def get_base_prefix_compat():
    """Get base prefix, or None if unset"""

    return (
        getattr(sys, "base_prefix", None)
        or getattr(sys, "real_prefix", None)
        or sys.prefix
    )

