# Backup AI MCP Server

> By [MEOK AI Labs](https://meok.ai) — Backup scheduling, verification, and retention policies with SOC2/GDPR/HIPAA compliance

## Installation

```bash
pip install backup-ai-mcp
```

## Usage

```bash
# Run standalone
python server.py

# Or via MCP
mcp install backup-ai-mcp
```

## Tools

### `create_backup_plan`
Create a backup plan following the 3-2-1 rule (3 copies, 2 media types, 1 offsite).

**Parameters:**
- `source_path` (str): Path to back up
- `destination` (str): Destination path (default 'backup')
- `frequency` (str): Backup frequency (default 'daily')
- `retention_days` (int): Retention period in days (default 30)

### `verify_backup`
Verify backup integrity using hash comparison. Checks SOC2 CC7.3 compliance.

**Parameters:**
- `backup_path` (str): Path to the backup file

### `list_backups`
List available backups in a directory with sizes and modification dates.

**Parameters:**
- `directory` (str): Directory to list (default 'backup')

### `calculate_backup_size`
Calculate estimated backup size, compressed size, and transfer time.

**Parameters:**
- `source_path` (str): Path to calculate

### `retention_policy`
Generate retention policy for compliance (SOC2, GDPR, HIPAA, PCI, FINRA).

**Parameters:**
- `files` (str): File description
- `compliance_type` (str): Compliance type — 'soc2', 'gdpr', 'hipaa', 'pci', 'finra'

## Authentication

Free tier: 30 calls/day. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## License

MIT — MEOK AI Labs
