"""workflow-tools — backend-agnostic orchestration tools.

Bundles ``workflow_tools.py`` + ``workflow_adapters/`` (base / dsl /
inline / mc). Provides 4 tools that wrap multiple backends:

    workflow_run / workflow_status / workflow_cancel / workflow_list_templates

Backend selection per-call via the ``backend`` argument or the
``HERMES_WORKFLOW_BACKEND`` env var. Default fallback is ``inline``
(zero-config). The ``mc`` adapter delegates to the nnnet/hermes-plugin-
mc-tools plugin when present (gracefully degraded if not).

Replaces in-fork ``tools/workflow_tools.py`` + ``tools/workflow_adapters/``
+ the ``workflow_*`` block in ``TOOLSETS['kanban']['tools']``.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


_TOOL_NAMES = (
    "workflow_run", "workflow_status", "workflow_cancel",
    "workflow_list_templates",
)


def register(ctx: Any) -> None:
    """Entry point — load workflow_tools (which self-registers handlers
    + triggers workflow_adapters auto-registration) and extend
    TOOLSETS['kanban']['tools'] with the workflow_* names.
    """
    try:
        from . import workflow_tools  # noqa: F401
    except Exception as exc:
        logger.error("workflow-tools: failed to load workflow_tools module: %s", exc)
        return

    try:
        import toolsets

        kanban_ts = toolsets.TOOLSETS.get("kanban") or {}
        kanban_tools = kanban_ts.get("tools")
        if isinstance(kanban_tools, list):
            added = 0
            for name in _TOOL_NAMES:
                if name not in kanban_tools:
                    kanban_tools.append(name)
                    added += 1
            logger.info(
                "workflow-tools: registered %d tools (%d added to TOOLSETS['kanban'])",
                len(_TOOL_NAMES), added,
            )
        else:
            logger.warning(
                "workflow-tools: TOOLSETS['kanban']['tools'] not a list"
            )
    except Exception as exc:
        logger.warning(
            "workflow-tools: tools registered but TOOLSETS['kanban'] extension "
            "failed (%s)", exc,
        )
