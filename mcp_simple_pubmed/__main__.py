"""
Main module entry point for mcp-simple-pubmed.
"""
# NOTE: This is a temporary entry point for the FastMCP migration.
# It points to the new server implementation.
from .server_fastmcp import main

if __name__ == "__main__":
    main()