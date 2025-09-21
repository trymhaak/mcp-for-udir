# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains an MCP (Model Context Protocol) server for accessing Norwegian curriculum data from Utdanningsdirektoratet (Udir). The project provides Claude Desktop with tools to fetch and search KL06/LK20 public curriculum data.

## Architecture

The repository is structured as a single MCP server implementation:

- `udir_api-mcp-server/` - Main MCP server directory containing:
  - `udir_api_server.py` - FastMCP-based server implementation with three main tools
  - `CLAUDE.md` - Detailed server documentation and usage guide
  - `Dockerfile` - Python 3.11 slim container setup
  - `requirements.txt` - Python dependencies (mcp[cli], httpx)
  - `readme.txt` - API documentation and tool descriptions

## Development Commands

### Docker Build and Run
```bash
cd udir_api-mcp-server
docker build -t udir_api-mcp-server .
docker run -p 8000:8000 udir_api-mcp-server
```

### Local Development
```bash
cd udir_api-mcp-server
pip install -r requirements.txt
python udir_api_server.py
```

### Environment Configuration
```bash
export UDIR_API_BASE_URL="https://data.udir.no/kl06/v201906"
```

## MCP Server Tools

The server provides three tools for curriculum data access:

1. **fetch_resource** - Fetch lists from specific API endpoints with pagination
2. **get_by_id** - Retrieve detailed information for specific resource codes
3. **search_resources** - Keyword search across multiple curriculum resource types

## Key Implementation Constraints

The MCP server follows specific compatibility constraints:
- No @mcp.prompt() decorators
- No prompt parameter to FastMCP()
- No typing module type hints (Optional/Union/List)
- Default to empty strings for all parameters
- Single-line docstrings only
- Always return strings from tools
- Graceful error handling with user-friendly messages

## Integration

This server is designed for Docker MCP Gateway integration. See `udir_api-mcp-server/CLAUDE.md` for complete Docker MCP Gateway catalog configuration and Claude Desktop usage examples.

## Data Sources

- Norwegian curriculum API (Grep database)
- LK06 (legacy curriculum 2006-2020) and LK20 (current curriculum from 2020)
- Public API with no authentication required
- Current API version: v201906