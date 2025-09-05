# Task List MCP Server
## Overview

This is a simple MCP Server demonstration. It deploys a Task List server onto google infrastructure. There is not external state for the application. It stores task list state inside a local json file that is updated and returned from MCP tool queries.

See the [documentation](documentation/) directory for more information


## Development
### Local Development

```bash
uv virtualenv
source .venv/bin/activate
uv sync
fastmcp run TaskListMCPServer/main.py --host 0.0.0.0 --transport streamable-http --port 8080
```
