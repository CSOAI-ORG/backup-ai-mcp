<div align="center">

# Backup Ai MCP

**MCP server for backup ai mcp operations**

[![PyPI](https://img.shields.io/pypi/v/meok-backup-ai-mcp)](https://pypi.org/project/meok-backup-ai-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Backup Ai MCP provides AI-powered tools via the Model Context Protocol (MCP).

## Tools

| Tool | Description |
|------|-------------|
| `create_backup_plan` | Create a backup plan following 3-2-1 rule (3 copies, 2 media types, 1 offsite). |
| `verify_backup` | Verify backup integrity using hash comparison. |
| `list_backups` | List available backups in a directory. |
| `calculate_backup_size` | Calculate estimated backup size and time. |
| `retention_policy` | Generate retention policy for compliance (SOC2, GDPR, HIPAA). |

## Installation

```bash
pip install meok-backup-ai-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "backup-ai-mcp": {
      "command": "python",
      "args": ["-m", "meok_backup_ai_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 5 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
