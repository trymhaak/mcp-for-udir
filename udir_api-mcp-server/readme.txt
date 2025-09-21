Udir Curriculum API – Fetch & Search
=====================================

OVERVIEW
--------
MCP server that fetches and keyword-searches KL06/LK20 public curriculum data from Utdanningsdirektoratet (Norwegian Directorate for Education and Training). This server provides access to Norwegian curriculum plans, subject codes, competence goals, and other educational resources through a simple REST API interface.

DESCRIPTION
-----------
This MCP server interfaces with the public Grep database containing all curriculum plans in the Norwegian Knowledge Promotion curriculum (Kunnskapsløftet). It includes both the old LK06 curriculum plans and the new LK20 curriculum plans that came with the curriculum renewal (fagfornyelsen).

The server provides three main tools for accessing curriculum data:
- fetch_resource: Generic GET requests with optional query parameters, pagination
- get_by_id: Direct lookup of specific resources by their codes/IDs  
- search_resources: Keyword search across multiple curriculum resource types

TOOLS
-----
1. fetch_resource
   - Purpose: Fetch lists of resources from specific endpoints
   - Parameters: 
     * endpoint (required): API endpoint like /laereplaner-lk20, /fagkoder, /kompetansemaal-lk20
     * query (optional): Search terms or raw query parameters
     * limit (optional): Number of results to return (default: 20)
     * offset (optional): Pagination offset (default: 0)
   - Example: "Fetch LK20 curriculum plans: call fetch_resource with endpoint=laereplaner-lk20 and limit=50"

2. get_by_id  
   - Purpose: Get detailed information about a specific resource
   - Parameters:
     * endpoint (required): Resource type like laereplaner-lk20, fagkoder
     * id (required): Specific resource code like NOR01-06, NOR1204
   - Example: "Get Norwegian curriculum plan: call get_by_id with endpoint=laereplaner-lk20 and id=NOR01-06"

3. search_resources
   - Purpose: Keyword search across curriculum resources
   - Parameters:
     * q (required): Search query/keywords
     * limit (optional): Number of results (default: 20)
     * offset (optional): Pagination offset (default: 0)
     * endpoint (optional): Specific endpoint to search, otherwise searches across common types
   - Example: "Search for mathematics: call search_resources with q=matematikk"

AUTHENTICATION
--------------
None required. This is a public API provided by the Norwegian Directorate for Education and Training.

ENVIRONMENT VARIABLES
--------------------
UDIR_API_BASE_URL (optional): Base URL for the Udir API
- Default: https://data.udir.no/kl06/v201906
- When not set, you can pass absolute URLs directly to the endpoint parameter

AVAILABLE RESOURCE TYPES
------------------------
Key curriculum resource types available through the API:

LK20 (Current curriculum, effective from 2020):
- laereplaner-lk20: Curriculum plans
- kompetansemaal-lk20: Competence goals
- kompetansemaalsett-lk20: Competence goal sets
- kjerneelementer-lk20: Core elements
- grunnleggende-ferdigheter-lk20: Basic skills
- tverrfaglige-temaer-lk20: Cross-curricular themes

LK06 (Previous curriculum, 2006-2020):
- laereplaner: Curriculum plans
- kompetansemaal: Competence goals  
- kompetansemaalsett: Competence goal sets
- hovedomraader: Main areas

Administrative data:
- fagkoder: Subject codes
- opplaeringsfag: Educational subjects
- utdanningsprogram: Educational programs
- programomraader: Program areas
- aarstrinn: Year levels

USAGE EXAMPLES
--------------
1. List all LK20 curriculum plans:
   fetch_resource(endpoint="laereplaner-lk20", limit="100")

2. Get specific Norwegian curriculum plan:
   get_by_id(endpoint="laereplaner-lk20", id="NOR01-06")

3. Search for mathematics-related content:
   search_resources(q="matematikk", limit="30")

4. List subject codes:
   fetch_resource(endpoint="fagkoder", limit="50")

5. Get specific subject code details:
   get_by_id(endpoint="fagkoder", id="NOR1204")

6. Search competence goals:
   search_resources(q="lesing", endpoint="kompetansemaal-lk20")

DATA FORMAT
-----------
All responses are in JSON format. Each resource typically contains:
- id: UUID identifier
- kode: Human-readable code
- uri: Permanent URI identifier  
- url-data: API URL for full data
- tittel: Title (often multilingual object)
- grep-type: Resource type URI
- status: Current status
- sist-endret: Last modified date

ERROR HANDLING
--------------
The server provides user-friendly error messages for:
- Missing required parameters
- Invalid API endpoints
- Network connectivity issues
- API rate limiting or server errors
- Invalid data formats

LICENSING
---------
Data is provided under the Norwegian License for Open Government Data (NLOD).
See: https://www.udir.no/om-udir/data/vilkar-for-bruk/

CONTACT & SUPPORT
-----------------
For questions about the curriculum data or API:
- Email: teknisk.grep@udir.no
- Slack: Open channel available (see GitHub wiki)
- Documentation: https://github.com/Utdanningsdirektoratet/KL06-LK20-public/wiki

VERSION INFORMATION
-------------------
Current API version: v201906
This version includes both LK06 and LK20 curriculum content.

The server uses the latest stable API endpoint but can be configured to use other versions by setting the UDIR_API_BASE_URL environment variable.
