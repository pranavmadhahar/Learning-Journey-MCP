import asyncio
import json
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage


load_dotenv()

# MCP servers the client will connect to.
# stdio = launch each MCP server as a local subprocess.
SERVERS = {
    "math": {
        "transport": "stdio",
        "command": "/home/pranav/Learning/mcp/myenv/bin/uv",
        "args": [
            "run",
            "fastmcp",
            "run",
            "src/math_mcp_server/main.py"
        ],
        "cwd": "/home/pranav/Learning/mcp/math-mcp-server"
    },
    "expense-tracker": {
        "transport": "stdio",
        "command": "/home/pranav/Learning/mcp/myenv/bin/uv",
        "args": [
            "run",
            "fastmcp",
            "run",
            "src/expense_tracker_mcp_server/main.py"
        ],
        "cwd": "/home/pranav/Learning/mcp/expense-tracker-mcp-server"
    }
}

async def main():
    # Create MCP client using the server configuration
    client = MultiServerMCPClient(SERVERS)

    # Discover tools exposed by all configured MCP servers.
    tools = await client.get_tools()

    # Convert the tool list into a dictionary: 
    # # tool name -> actual tool object. 
    # # Makes it easy to find the tool requested by the LLM.
    named_tools = {}

    for tool in tools:
        named_tools[tool.name] = tool

    print(named_tools.keys())

    # Create the LLM and make it aware of the MCP tools.
    llm = ChatOpenAI(model_name="gpt-4", temperature=0)
    llm_with_tools = llm.bind_tools(tools)


    # User's request. 
    # The LLM decides whether a tool is required and which one to call.
    prompt = "Solve the following math problem: 2 + 5"
    # prompt = "What is the capital of Belgium?"
    # prompt = "add Rs 200 for cab ride to airport last wednesday"
    response = await llm_with_tools.ainvoke(prompt)

    # If the LLM did not request any tools,
    # return its normal response.
    if not getattr(response, "tool_calls", None):
        print("\nLLM Reply:", response.content)
        return

    # Store the results of all requested tool calls.
    tool_messages = []

    # Process every tool call requested by the LLM.
    for t in response.tool_calls:
        selected_tool = t["name"]
        selected_tool_args = t["args"]
        selected_tool_id = t["id"]

        # Find the actual MCP tool and execute it.
        result = await named_tools[selected_tool].ainvoke(selected_tool_args)

        # Convert the tool result into a ToolMessage.
        # The ToolMessage tells the LLM what the tool returned.
        tool_messages.append(ToolMessage(
            tool_call_id = selected_tool_id,
            content=json.dumps(result)
        ))

    # Send the original prompt, the LLM's tool-call message,
    # and all tool results back to the LLM.
    # *tool_messages unpacks the list into individual messages.
    final_response = await llm_with_tools.ainvoke([prompt, response, *tool_messages])

    # Print the LLM's final natural-language response.
    print("Final Response:", final_response.content)



if __name__ == "__main__":
    # Start the asyncio event loop and run main().
    asyncio.run(main())

