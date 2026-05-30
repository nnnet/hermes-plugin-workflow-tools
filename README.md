# hermes-plugin-workflow-tools

External Hermes plugin — backend-agnostic workflow orchestration.

## About

Four `workflow_*` tools that wrap multiple execution backends behind a
single uniform interface. Lets a chief or main:manager hand a workflow
template to the system without committing to a specific backend.

| Tool | Purpose |
|---|---|
| `workflow_run` | Start a workflow run (returns run_id) |
| `workflow_status` | Read run state (state/current_node/history/result/error) |
| `workflow_cancel` | Stop a running workflow |
| `workflow_list_templates` | List available templates for a backend |

## Backends

| Adapter | Status | Notes |
|---|---|---|
| `inline` | mandatory | Zero-config in-process DSL runner; default fallback |
| `mc` | optional | HTTP bridge to nnnet/hermes-plugin-mc-tools; auto-loads if mc-tools is enabled |
| (future) | — | `langgraph`, `temporal`, etc — adapter contract is in `workflow_adapters/base.py` |

Backend selection per-call:
```python
workflow_run(template="x", backend="mc")     # force MC
workflow_run(template="x")                   # use HERMES_WORKFLOW_BACKEND or fallback to inline
```

## Activate

```yaml
# config.yaml
plugins:
  enabled:
    - workflow-tools
```

For MC backend, also enable `mc-tools`:
```yaml
plugins:
  enabled:
    - mc-tools
    - workflow-tools
```

## Mounting

```yaml
# docker-compose.hermes-core.yml
volumes:
  - ./sources/hermes-external-plugins/workflow-tools:/opt/data/plugins/workflow-tools:ro
```

## Layout

```
hermes-plugin-workflow-tools/
├── __init__.py                # register(ctx)
├── plugin.yaml
├── workflow_tools.py          # 4 workflow_* tool handlers + schemas
└── workflow_adapters/
    ├── __init__.py            # public surface re-exports
    ├── base.py                # WorkflowAdapter protocol + registry + autoregister
    ├── dsl.py                 # workflow DSL parsing
    ├── inline.py              # in-process backend
    └── mc.py                  # Mission Control backend (lazy mc_tools import)
```
