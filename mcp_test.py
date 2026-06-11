from agents.mcp_config import mongodb_mcp_toolset
from utils.logger import get_logger
      
logger = get_logger(__name__)  

toolset = mongodb_mcp_toolset(read_only=True)

logger.info(toolset)