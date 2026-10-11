# Copilot instructions for `fastapi-profilesvc`

## Project shape
- This repo is a minimal FastAPI service, not a multi-service application. The app entry point is `main.py`, and the ASGI app object is created as `app = FastAPI()`.
- The current service surface is intentionally small: `GET /` in `main.py` returns `{"message": "Hello, World!"}`. Treat this as the baseline pattern for new route handlers and response payloads.
- There are no separate domain modules, repositories, or service layers yet. Prefer adding small, direct route functions in `main.py` unless a feature clearly demands package-level organization.

## Runtime and dependency conventions
- `pyproject.toml` is the source of truth for dependencies and Python version. The project targets Python `>=3.15` and currently depends on `fastapi[standard]>=0.143.0`.
- Use `uv` for project operations (`uv sync`, `uv run ...`) rather than ad hoc global Python commands. The workspace already includes `.venv`, and the repo is set up for a managed environment.
- Keep changes to dependency management in `pyproject.toml`; avoid introducing packages without updating the project metadata.

## Coding patterns to follow
- Follow the existing FastAPI style: lightweight function-based endpoints, plain dict/JSON responses, and no custom framework wrappers.
- When adding features, keep the shape simple and explicit: define route handlers near related logic, and prefer straightforward FastAPI request/response handling over abstraction layers.
- There is no current auth, persistence, or background worker layer. If a new feature needs those capabilities, add them intentionally and keep the app bootstrap readable.

## Workflow expectations
- Validate startup behavior with a minimal smoke check after changing app setup or routes, e.g. `uv run python -m compileall .` or an import-based check that the app object loads.
- There are no formal project tests at the moment; do not assume a test suite exists. If you add tests, keep them lightweight and project-scoped.
- For runtime changes, prefer using the project environment and route-level verification over broad refactors.

## Examples to model
- Keep new routes consistent with the pattern in `main.py`: a small function, a FastAPI decorator, and a JSON response object.
- Preserve the repo’s minimal architecture: root-level app entry, no hidden service orchestration, and no injection framework unless the project clearly grows beyond this starter template.
