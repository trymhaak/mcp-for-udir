# mcp-for-udir

MCP server for Norwegian curriculum data (LK06/LK20) from [Utdanningsdirektoratet](https://www.udir.no/) (the Norwegian Directorate for Education and Training).

It exposes the public [Grep database](https://data.udir.no/) to any MCP client (Claude Desktop, Claude Code, and others): every curriculum plan, subject code, and competence goal in the Norwegian Knowledge Promotion curriculum, both the old LK06 plans and the current LK20 plans from fagfornyelsen.

No API key needed. The Udir API is fully public.

## Tools

| Tool | What it does |
|---|---|
| `fetch_resource` | Fetch lists from an endpoint (`/laereplaner-lk20`, `/fagkoder`, `/kompetansemaal-lk20`, ...) with optional query and pagination |
| `get_by_id` | Direct lookup of a specific resource by code, e.g. curriculum plan `NOR01-06` or subject code `NOR1204` |
| `search_resources` | Keyword search across curriculum resource types, e.g. `matematikk` |

Example prompts once connected:

- "Get the Norwegian curriculum plan NOR01-06"
- "Search competence goals for programmering"
- "List all LK20 curriculum plans"

## Quickstart

### Local

```bash
cd udir_api-mcp-server
pip install -r requirements.txt
python udir_api_server.py
```

### Docker

```bash
cd udir_api-mcp-server
docker build -t udir-mcp .
docker run -p 8000:8000 udir-mcp
```

### Configuration

Optional environment variable:

```bash
export UDIR_API_BASE_URL="https://data.udir.no/kl06/v201906"   # default
```

## Resource types

Key endpoints available through the API:

- **LK20 (current, from 2020):** `laereplaner-lk20` (curriculum plans), `kompetansemaal-lk20` (competence goals)
- **LK06 (legacy):** `laereplaner`, `kompetansemaal`
- **Shared:** `fagkoder` (subject codes)

See `udir_api-mcp-server/readme.txt` for the full endpoint list and parameter details.

## Stack

Python, [FastMCP](https://github.com/modelcontextprotocol/python-sdk), httpx. Single-file server in `udir_api-mcp-server/udir_api_server.py`.

## License

MIT. See [LICENSE](LICENSE).
