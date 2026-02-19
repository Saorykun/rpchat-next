"""Prompts module.

IMPORTANT: During migration, copy legacy `rpchat/prompts.py` here *verbatim*.
For now, we provide a thin re-export shim so prompts remain unchanged while
you move architecture around.

Once you are ready, replace this file with the copied legacy content and remove the shim.
"""

from __future__ import annotations

# Bridge import: keep prompts exactly as legacy while refactoring architecture.
from rpchat.prompts import *  # noqa: F401,F403
