"""Repository-wide Python startup tweaks.

This module is imported automatically by Python when it is on `sys.path`.
We use it to suppress noisy ADK experimental warnings without changing the
actual runtime behavior of MongoDB MCP or the selected Gemini model.
"""

from __future__ import annotations

import warnings


warnings.filterwarnings(
    "ignore",
    message=r".*FeatureName\.(PLUGGABLE_AUTH|BASE_AUTHENTICATED_TOOL|JSON_SCHEMA_FOR_FUNC_DECL|_MCP_GRACEFUL_ERROR_HANDLING).*",
    category=UserWarning,
)
