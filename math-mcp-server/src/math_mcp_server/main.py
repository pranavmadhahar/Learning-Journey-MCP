from __future__ import annotations
# Allows postponed evaluation of type annotations

from fastmcp import FastMCP


# Create the MCP server
mcp = FastMCP("math-mcp-server")


def _as_number(x):
    # Helper function: convert input into a number
    # Accepts int, float, or numeric strings
    if isinstance(x, (int, float)):
        return x

    if isinstance(x, str):
        # Remove whitespace and convert string to float
        return float(x.strip())

    # Reject unsupported input types
    raise TypeError(
        f"Expected int, float, or numeric string, got {type(x).__name__}"
    )


@mcp.tool()
async def add(x, y):
    """Add two numbers."""
    # Convert inputs to numbers before performing the operation
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


@mcp.tool()
async def modulus(x, y):
    """Calculate the remainder of two numbers."""
    # % returns the remainder after division
    return _as_number(x) % _as_number(y)


@mcp.tool()
async def square_root(x):
    """Calculate the square root of a number."""
    # ** 0.5 means raise the number to the power 0.5
    # which is equivalent to taking its square root
    return _as_number(x) ** 0.5


@mcp.tool()
async def square(x):
    """Calculate the square of a number."""
    return _as_number(x) ** 2

@mcp.tool()
async def cube(x):
    """Calculate the cube of a number."""
    return _as_number(x) ** 3

