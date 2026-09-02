from __future__ import annotations
from fastmcp import FastMCP

mcp = FastMCP("math-mcp-server")

def _as_number(x):
    # accepts int, float, or numeric strings; raise errors otherwise
    if isinstance(x, (int, float)):
        return x
    if isinstance(x, str):
        return float(x.strip())
    raise typeError(f"Expected int, float, or numeric string, got {type(x).__name__}")

@mcp.tool()
async def add(x, y):
    """Add two numbers."""
    return _as_number(x) + _as_number(y)

@mcp.tool()
async def subtract(x, y):
    """Subtract two numbers."""
    return _as_number(x) - _as_number(y)

@mcp.tool()
async def multiply(x, y):
    """Multiply two numbers."""
    return _as_number(x) * _as_number(y)

@mcp.tool()
async def divide(x, y):
    """Divide two numbers."""
    return _as_number(x) / _as_number(y)


  

            

