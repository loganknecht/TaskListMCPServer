# weather.Dockerfile
FROM python:3.12-slim

# ------------------------------------------------------------------------------
# Install UV
# ------------------------------------------------------------------------------
# From Docs Here: https://docs.astral.sh/uv/guides/integration/docker/
# But instead just do this: https://stackoverflow.com/a/79228154
# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Copy Server Code Over
# ------------------------------------------------------------------------------
COPY ./TaskListMCPServer /opt/TaskListMCPServer/TaskListMCPServer

WORKDIR /opt/TaskListMCPServer/TaskListMCPServer

# ------------------------------------------------------------------------------
# Install Dependencies
# ------------------------------------------------------------------------------
# From Docs Here
# https://github.com/astral-sh/uv-docker-example/blob/main/Dockerfile
# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy
# Ensure installed tools can be executed out of the box
ENV UV_TOOL_BIN_DIR=/usr/local/bin
# Install the project's dependencies using the lockfile and settings
RUN uv sync --locked --no-dev

RUN uv virtualenv
# Place executables in the environment at the front of the path
ENV PATH="/opt/TaskListMCPServer/TaskListMCPServer/.venv/bin:$PATH"
# ------------------------------------------------------------------------------

# Run your weather.py script directly
CMD ["fastmcp", "run", "task_list_mcp_server.py", \
        "--host", "0.0.0.0", \
        "--transport", "streamable-http", \
        "--port", "8080"]