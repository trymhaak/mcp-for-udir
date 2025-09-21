Udir Curriculum API MCP Server - Claude Desktop Integration
============================================================

IMPLEMENTATION NOTES
--------------------
This MCP server was built following specific constraints for optimal compatibility:

✅ NO @mcp.prompt() decorators
✅ NO prompt parameter to FastMCP()  
✅ NO typing module type hints (no Optional/Union/List, etc.)
✅ NO complex parameter types — uses param: str = "" (never None)
✅ SINGLE-LINE DOCSTRINGS ONLY
✅ DEFAULT TO EMPTY STRINGS for all params
✅ ALWAYS return strings from tools
✅ ALWAYS use Docker (Python 3.11 slim base)
✅ ALWAYS log to stderr using provided logging setup
✅ ALWAYS handle errors gracefully with user-friendly messages

TOOL CATALOG
-----------
The server provides three main tools for Claude Desktop:

1. **fetch_resource**
   - Fetches resource lists from specific API endpoints
   - Supports pagination (limit, offset)
   - Handles both simple and complex query parameters
   - Returns formatted previews of curriculum data

2. **get_by_id**  
   - Retrieves detailed information for specific resources
   - Uses endpoint + resource code/ID pattern
   - Provides comprehensive data formatting
   - Essential for deep-diving into curriculum content

3. **search_resources**
   - Performs keyword searches across multiple resource types
   - Intelligent filtering based on search terms
   - Cross-endpoint search when no specific endpoint provided
   - Ideal for exploratory curriculum research

ENVIRONMENT CONFIGURATION
-------------------------
Set the base URL for optimal performance:

```bash
export UDIR_API_BASE_URL="https://data.udir.no/kl06/v201906"
```

If not set, the server defaults to this URL but you can override by passing absolute URLs to the endpoint parameter in tool calls.

CLAUDE DESKTOP USAGE EXAMPLES
-----------------------------

### Basic Curriculum Exploration
```
"Show me available Norwegian curriculum plans for LK20"
→ Tool: fetch_resource(endpoint="laereplaner-lk20", limit="20")
```

### Detailed Resource Lookup  
```
"Get details about the Norwegian language curriculum NOR01-06"
→ Tool: get_by_id(endpoint="laereplaner-lk20", id="NOR01-06")
```

### Educational Research
```
"Search for content related to mathematics across all curriculum types"
→ Tool: search_resources(q="matematikk", limit="30")
```

### Administrative Data Access
```
"List all available subject codes"
→ Tool: fetch_resource(endpoint="fagkoder", limit="100")
```

### Targeted Search
```
"Find competence goals related to reading in LK20"
→ Tool: search_resources(q="lesing", endpoint="kompetansemaal-lk20")
```

DOCKER MCP GATEWAY INTEGRATION
------------------------------
This server is designed to work seamlessly with the Docker MCP Gateway system.

### Catalog Entry Template
```yaml
version: 2
name: custom
displayName: Custom MCP Servers
registry:
  udir_api:
    description: "Fetch and keyword-search KL06/LK20 public curriculum data from Udir"
    title: "Udir Curriculum API"
    type: server
    dateAdded: "2025-09-21T00:00:00Z"
    image: udir_api-mcp-server:latest
    ref: ""
    readme: ""
    toolsUrl: ""
    source: ""
    upstream: ""
    icon: ""
    tools:
      - name: fetch_resource
      - name: get_by_id
      - name: search_resources
    metadata:
      category: integration
      tags:
        - utdanningsdirektoratet
        - curriculum
        - kl06
        - lk20
      license: MIT
      owner: local
```

### Registry Configuration
Add to ~/.docker/mcp/registry.yaml:
```yaml
registry:
  udir_api:
    ref: ""
```

COMMON USE CASES FOR CLAUDE
---------------------------

1. **Curriculum Analysis**
   - Compare LK06 vs LK20 curriculum changes
   - Analyze competence goal progressions across year levels
   - Research cross-curricular themes and connections

2. **Educational Planning**
   - Find relevant curriculum content for specific topics
   - Identify assessment criteria and learning objectives  
   - Explore subject code hierarchies and relationships

3. **Research & Documentation**
   - Generate reports on curriculum structure and content
   - Extract and summarize learning objectives
   - Create educational content aligned with national standards

4. **Administrative Tasks**
   - Verify correct subject codes for documentation
   - Look up official curriculum terminology
   - Access authoritative educational program structures

PERFORMANCE CONSIDERATIONS
--------------------------
- The API is public and doesn't require authentication
- Rate limiting may apply for excessive requests
- Search operations query multiple endpoints and may take longer
- Use specific endpoints when possible for faster responses
- Cache frequently accessed curriculum data when appropriate

ERROR SCENARIOS & HANDLING
--------------------------
The server gracefully handles common issues:

- **Invalid Endpoints**: Suggests correct endpoint formats
- **Missing Resources**: Clear error messages with helpful hints
- **Network Issues**: Timeout handling with retry suggestions
- **Malformed Queries**: Parameter validation and correction guidance
- **API Changes**: Robust error reporting for troubleshooting

MAINTENANCE & UPDATES
--------------------
- Monitor the official Udir GitHub wiki for API changes
- Check for new curriculum versions (current: v201906)
- Update UDIR_API_BASE_URL if the API version changes
- Rebuild Docker image after any server updates

INTEGRATION VERIFICATION
------------------------
After installation, verify the integration works:

1. Check Docker MCP Gateway lists the server:
   ```bash
   docker mcp server list
   ```

2. Test basic functionality through Claude Desktop:
   - Request a simple curriculum list
   - Search for a common educational term
   - Look up a specific resource by ID

3. Monitor logs for any configuration issues:
   ```bash
   docker logs [container-id]
   ```

TROUBLESHOOTING
--------------
Common issues and solutions:

- **Server not appearing**: Check catalog and registry YAML syntax
- **Tool calls failing**: Verify UDIR_API_BASE_URL environment variable
- **Empty responses**: Confirm API endpoint names match current version
- **Search not working**: Check query formatting and endpoint availability

CONTACT & SUPPORT
----------------
For technical issues with this MCP server implementation, refer to:
- MCP documentation for integration questions
- Udir API documentation for data-related questions
- GitHub issues for bug reports and feature requests
