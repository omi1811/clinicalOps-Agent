# agents/shared_mcp.py

from dotenv import load_dotenv
from utils.logger import get_logger
      
logger = get_logger(__name__)  

from agents.mcp_config import mongodb_mcp_toolset

load_dotenv()

# SINGLE shared MCP instance
shared_mcp_toolset = mongodb_mcp_toolset(
    read_only=False
)

logger.info("✅ Shared MongoDB MCP Toolset initialized")