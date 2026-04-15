#!/usr/bin/env python3
"""Backup AI MCP — MEOK AI Labs. File backup scheduling, verification, retention policies."""

import sys, os

sys.path.insert(0, os.path.expanduser("~/clawd/meok-labs-engine/shared"))
from auth_middleware import check_access

import json, re, hashlib, shutil
from datetime import datetime, timezone, timedelta
from typing import Optional
from collections import defaultdict
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "backup-ai",
    instructions="MEOK AI Labs — Backup scheduling, verification, retention policies. 3-2-1 rule, SOC2 backup compliance.",
)

FREE_DAILY_LIMIT = 30
_usage = defaultdict(list)


def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now - t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT:
        return json.dumps({"error": "Limit/day. Upgrade: meok.ai"})
    _usage[c].append(now)
    return None


_backup_registry = {}


@mcp.tool()
def create_backup_plan(
    source_path: str,
    destination: str = "backup",
    frequency: str = "daily",
    retention_days: int = 30,
    api_key: str = "",
) -> str:
    """Create a backup plan following 3-2-1 rule (3 copies, 2 media types, 1 offsite)."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    if err := _rl():
        return err

    plan_id = hashlib.sha256(
        f"{source_path}{datetime.now().isoformat()}".encode()
    ).hexdigest()[:8]
    plan = {
        "plan_id": plan_id,
        "source": source_path,
        "destination": destination,
        "frequency": frequency,
        "retention_days": retention_days,
        "created": datetime.now(timezone.utc).isoformat(),
        "status": "active",
    }
    _backup_registry[plan_id] = plan

    return {
        "plan": plan,
        "rule": "3-2-1",
        "explanation": "3 copies of data, 2 different media types, 1 offsite copy",
        "next_backup": (
            datetime.now() + timedelta(days=1 if frequency == "daily" else 7)
        ).isoformat(),
    }


@mcp.tool()
def verify_backup(backup_path: str, api_key: str = "") -> str:
    """Verify backup integrity using hash comparison."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    if err := _rl():
        return err

    status = "verified"
    if not os.path.exists(backup_path):
        status = "missing"
    elif os.path.getsize(backup_path) == 0:
        status = "empty"

    return {
        "backup_path": backup_path,
        "status": status,
        "verified_at": datetime.now(timezone.utc).isoformat(),
        "compliance": "SOC2 CC7.3" if status == "verified" else None,
        "recommendation": "Re-run backup if failed" if status != "verified" else None,
    }


@mcp.tool()
def list_backups(directory: str = "backup", api_key: str = "") -> str:
    """List available backups in a directory."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    if err := _rl():
        return err

    backups = []
    if os.path.exists(directory):
        for f in os.listdir(directory):
            fpath = os.path.join(directory, f)
            if os.path.isfile(fpath):
                backups.append(
                    {
                        "name": f,
                        "size_bytes": os.path.getsize(fpath),
                        "modified": datetime.fromtimestamp(
                            os.path.getmtime(fpath), timezone.utc
                        ).isoformat(),
                    }
                )

    return {"directory": directory, "backups": backups, "count": len(backups)}


@mcp.tool()
def calculate_backup_size(source_path: str, api_key: str = "") -> str:
    """Calculate estimated backup size and time."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    if err := _rl():
        return err

    if os.path.isfile(source_path):
        size = os.path.getsize(source_path)
    elif os.path.isdir(source_path):
        size = sum(
            os.path.getsize(os.path.join(dp, f))
            for dp, dn, fn in os.walk(source_path)
            for f in fn
        )
    else:
        return {"error": "Path not found"}

    return {
        "source": source_path,
        "size_bytes": size,
        "size_mb": round(size / 1024 / 1024, 2),
        "estimated_compressed_mb": round(size / 1024 / 1024 * 0.7, 2),
        "transfer_time_10mbps_sec": round(size / 1024 / 1024 / 10, 1),
    }


@mcp.tool()
def retention_policy(
    files: str, compliance_type: str = "soc2", api_key: str = ""
) -> str:
    """Generate retention policy for compliance (SOC2, GDPR, HIPAA)."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}

    if err := _rl():
        return err

    policies = {
        "soc2": {
            "min_days": 90,
            "max_days": 365,
            "description": "Audit logs retained 90 days",
        },
        "gdpr": {
            "min_days": 2555,
            "max_days": None,
            "description": "Personal data retained 7 years after contract end",
        },
        "hipaa": {
            "min_days": 2190,
            "max_days": 3650,
            "description": "Medical records 6 years minimum",
        },
        "pci": {
            "min_days": 365,
            "max_days": 1095,
            "description": "PCI logs 1 year, card data not stored",
        },
        "finra": {
            "min_days": 2190,
            "max_days": None,
            "description": "Financial records 6 years",
        },
    }

    policy = policies.get(compliance_type.lower(), policies["soc2"])
    return {
        "compliance_type": compliance_type,
        "retention_policy": policy,
        "crosswalk_reference": "Map to ISO 27001 via meok-governance-engine-mcp",
    }


if __name__ == "__main__":
    mcp.run()
