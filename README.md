# Task List MCP Server
## Overview

This is a simple MCP Server demonstration. It deploys a Task List server onto google infrastructure. There is not external state for the application. It stores task list state inside a local json file that is updated and returned from MCP tool queries.

See the [documentation](documentation/) directory for more information


## Development
### Local Development

```bash
cd TaskListMCPServer/
uv virtualenv
source .venv/bin/activate
uv sync
# Source the env file
uv run --env-file dev.env -- fastmcp run main.py --host 0.0.0.0 --transport streamable-http --port 8080
# python your_script.py
# source .env
# fastmcp run main.py --host 0.0.0.0 --transport streamable-http --port 8080
```
