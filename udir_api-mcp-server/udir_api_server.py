#!/usr/bin/env python3
"""Simple Udir Curriculum API MCP Server - Fetch and search KL06/LK20 public curriculum data."""

import os
import sys
import logging
from datetime import datetime, timezone
import httpx
from mcp.server.fastmcp import FastMCP

# Logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("udir_api-server")

# Initialize MCP server (NO prompt parameter)
mcp = FastMCP("udir_api")

# Configuration
# BASE_URL should be derived from the API documentation; allow override via env var
BASE_URL = os.environ.get("UDIR_API_BASE_URL", "https://data.udir.no/kl06/v201906").strip()

# === Utility ===
def _join_url(base, path):
    """Join base URL with path."""
    if not base:
        return ""
    if path.startswith("/"):
        return base.rstrip("/") + path
    return base.rstrip("/") + "/" + path

def _fmt_table(items):
    """Very small formatter to show key fields."""
    if not items:
        return "No items."
    lines = []
    count = 0
    for it in items:
        if count >= 10:
            lines.append(f"... and {len(items) - 10} more items")
            break
        if isinstance(it, dict):
            # Show key identifiers and title
            kode = it.get("kode", "")
            tittel = ""
            if "tittel" in it:
                if isinstance(it["tittel"], dict):
                    tittel = it["tittel"].get("default", it["tittel"].get("nb", ""))
                else:
                    tittel = str(it["tittel"])
            grep_type = it.get("grep-type", "").split("/")[-1] if it.get("grep-type") else ""
            lines.append(f"  {kode}: {tittel} ({grep_type})")
        else:
            lines.append(str(it))
        count += 1
    return "\n".join(lines)

# === Tools ===

@mcp.tool()
async def fetch_resource(endpoint: str = "", query: str = "", limit: str = "20", offset: str = "0") -> str:
    """Fetch resources from a given endpoint with optional query, limit, and offset."""
    if not endpoint.strip():
        return "❌ Error: 'endpoint' is required (e.g., /laereplaner-lk20, /fagkoder, /kompetansemaal-lk20)."
    
    url = ""
    try:
        # Prefer explicit BASE_URL if provided; otherwise allow direct absolute URLs passed via endpoint
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            url = endpoint
        else:
            if not BASE_URL:
                return "❌ Error: UDIR_API_BASE_URL is not set; provide a full absolute URL in 'endpoint' or set the env var."
            url = _join_url(BASE_URL, endpoint)

        params = {}
        if query.strip():
            # Expect query as raw "key=value&k2=v2" or a single search term 'q'
            if "=" in query:
                # Let the API handle the raw query string
                pass
            else:
                # If no key provided, map to 'q'
                params["q"] = query.strip()

        # Basic pagination coercion
        try:
            l = int(limit) if limit.strip() else 20
            o = int(offset) if offset.strip() else 0
            if l >= 0:
                params["limit"] = str(l)
            if o >= 0:
                params["offset"] = str(o)
        except Exception:
            return "❌ Error: 'limit' and 'offset' must be integers."

        # Build final URL (attach raw query if contains '=')
        final_url = url
        if query.strip() and "=" in query:
            sep = "&" if "?" in final_url else "?"
            final_url = final_url + sep + query.strip()

        async with httpx.AsyncClient() as client:
            resp = await client.get(final_url, params=params, timeout=20)
            resp.raise_for_status()
            try:
                data = resp.json()
            except Exception:
                text = resp.text
                return "✅ Success (non-JSON response):\n" + text

        # Format a concise preview
        preview = ""
        if isinstance(data, list):
            preview = _fmt_table(data)
        elif isinstance(data, dict):
            # If items/values list exists, preview it; else show dict keys
            if "items" in data and isinstance(data["items"], list):
                preview = _fmt_table(data["items"])
            else:
                # Show key information from the dict
                keys = list(data.keys())[:10]
                preview_dict = {k: data.get(k) for k in keys}
                preview = str(preview_dict)

        return f"✅ Success:\nURL: {final_url}\nTotal items: {len(data) if isinstance(data, list) else 'N/A'}\nPreview:\n{preview}"
        
    except httpx.HTTPStatusError as e:
        return f"❌ API Error: {e.response.status_code} at {url or endpoint}"
    except Exception as e:
        logger.error(f"fetch_resource error: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def get_by_id(endpoint: str = "", id: str = "") -> str:
    """Fetch a single resource by ID at the given endpoint."""
    if not endpoint.strip():
        return "❌ Error: 'endpoint' is required (e.g., laereplaner-lk20, fagkoder)."
    if not id.strip():
        return "❌ Error: 'id' is required (e.g., NOR01-06, NOR1204)."
    
    url = ""
    try:
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            base = endpoint.rstrip("/")
            url = base + "/" + id
        else:
            if not BASE_URL:
                return "❌ Error: UDIR_API_BASE_URL is not set; provide an absolute 'endpoint' or set the env var."
            base = _join_url(BASE_URL, endpoint).rstrip("/")
            url = base + "/" + id

        async with httpx.AsyncClient() as client:
            resp = await client.get(url, timeout=20)
            resp.raise_for_status()
            try:
                data = resp.json()
                
                # Format the response nicely
                result = "✅ Success:\n"
                if isinstance(data, dict):
                    # Show key fields first
                    if "kode" in data:
                        result += f"Kode: {data['kode']}\n"
                    if "tittel" in data:
                        tittel = data["tittel"]
                        if isinstance(tittel, dict):
                            tittel_text = tittel.get("default", tittel.get("nb", ""))
                        else:
                            tittel_text = str(tittel)
                        result += f"Tittel: {tittel_text}\n"
                    if "grep-type" in data:
                        result += f"Type: {data['grep-type'].split('/')[-1]}\n"
                    if "status" in data:
                        result += f"Status: {data['status']}\n"
                    result += f"\nFull data:\n{str(data)}"
                else:
                    result += str(data)
                
                return result
            except Exception:
                return "✅ Success (non-JSON response):\n" + resp.text
                
    except httpx.HTTPStatusError as e:
        return f"❌ API Error: {e.response.status_code} at {url or endpoint}"
    except Exception as e:
        logger.error(f"get_by_id error: {e}")
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def search_resources(q: str = "", limit: str = "20", offset: str = "0", endpoint: str = "") -> str:
    """Keyword search across resources - searches through available curriculum data."""
    if not q.strip():
        return "❌ Error: 'q' (search query) is required."
    
    # For Udir API, we can search across multiple endpoints or use a general approach
    # Since there's no dedicated search endpoint, we'll search common resource types
    search_endpoints = [
        "laereplaner-lk20",  # LK20 curriculum plans
        "laereplaner",       # LK06 curriculum plans
        "fagkoder",          # Subject codes
        "kompetansemaal-lk20", # Competence goals LK20
        "kompetansemaal"     # Competence goals LK06
    ]
    
    if endpoint.strip():
        # If specific endpoint provided, search only there
        search_endpoints = [endpoint.strip()]
    
    url = ""
    all_results = []
    
    try:
        # Search across endpoints (limited approach since API doesn't have unified search)
        for search_endpoint in search_endpoints:
            try:
                if search_endpoint.startswith("http://") or search_endpoint.startswith("https://"):
                    url = search_endpoint
                else:
                    if not BASE_URL:
                        continue
                    url = _join_url(BASE_URL, search_endpoint)

                params = {"q": q.strip()}
                try:
                    l = int(limit) if limit.strip() else 20
                    o = int(offset) if offset.strip() else 0
                    if l >= 0:
                        params["limit"] = str(min(l, 5))  # Limit per endpoint for combined search
                    if o >= 0:
                        params["offset"] = str(o)
                except Exception:
                    continue

                async with httpx.AsyncClient() as client:
                    resp = await client.get(url, params=params, timeout=10)
                    if resp.status_code == 200:
                        try:
                            data = resp.json()
                            if isinstance(data, list) and data:
                                # Filter results that contain the search term
                                filtered = []
                                for item in data:
                                    if isinstance(item, dict):
                                        # Search in title and other text fields
                                        item_text = ""
                                        if "tittel" in item:
                                            tittel = item["tittel"]
                                            if isinstance(tittel, dict):
                                                item_text += tittel.get("default", tittel.get("nb", ""))
                                            else:
                                                item_text += str(tittel)
                                        if "kode" in item:
                                            item_text += " " + str(item["kode"])
                                        
                                        if q.lower() in item_text.lower():
                                            item["_source_endpoint"] = search_endpoint
                                            filtered.append(item)
                                
                                all_results.extend(filtered[:5])  # Max 5 per endpoint
                        except Exception:
                            continue
                            
            except Exception:
                continue
        
        if not all_results:
            return f"❌ No results found for query: '{q}'"
        
        # Limit total results
        try:
            final_limit = int(limit) if limit.strip() else 20
            all_results = all_results[:final_limit]
        except Exception:
            all_results = all_results[:20]
        
        preview = _fmt_table(all_results)
        return f"✅ Search Results for '{q}':\nFound {len(all_results)} results\n\nPreview:\n{preview}"
        
    except Exception as e:
        logger.error(f"search_resources error: {e}")
        return f"❌ Error: {str(e)}"

# === Startup ===
if __name__ == "__main__":
    logger.info("Starting Udir Curriculum API MCP server...")
    try:
        logger.info(f"Using base URL: {BASE_URL}")
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)
