# test_mcp_tools.py

import asyncio
from agents.mcp_config import mongodb_mcp_toolset
from utils.logger import get_logger
      
logger = get_logger(__name__) 
async def main():
    toolset = mongodb_mcp_toolset(read_only=True)

    tools = await toolset.get_tools()

    logger.info(f"Loaded {len(tools)} tools")

    for t in tools:
        logger.info("-", t.name)

asyncio.run(main())