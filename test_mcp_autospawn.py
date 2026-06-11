import asyncio
from google.adk.tools.mcp_tool import MCPToolset
from mcp import StdioServerParameters
import os
from dotenv import load_dotenv
from google.adk.tools.mcp_tool import MCPToolset
from google.adk.tools.mcp_tool import SseConnectionParams
from utils.logger import get_logger
      
logger = get_logger(__name__) 

load_dotenv()

async def test_mcp():
    logger.info("🔌 Testing ADK MCPToolset (auto-spawning MCP)...")
    
    toolset = MCPToolset(
    connection_params=SseConnectionParams(
        url="http://localhost:8000/sse"
    )
)
    
    try:
        logger.info("📡 ADK is auto-spawning MCP server...")
        tools = await toolset.get_tools()
        logger.info(f"✅ MCP connected! Found {len(tools)} tools:")
        for t in tools[:5]:
            logger.info(f"   - {t.name}")
        logger.info("\n🎉 MCP Toolset works perfectly! No manual server needed.")
    except Exception as e:
        logger.info(f"\n❌ MCP test failed: {e}")
    finally:
        await toolset.close()

asyncio.run(test_mcp())
