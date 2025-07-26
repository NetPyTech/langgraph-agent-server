from pydantic_ai.mcp import MCPServerStdio

calculator_mcp = MCPServerStdio('python', ["MCP/calculator.py", 'stdio'])