#!/usr/bin/env python3
import json
import time
import uuid

# Read existing jobs
with open('/Users/chimpman/.openclaw/cron/jobs.json', 'r') as f:
    data = json.load(f)

# Create new Sinestro job entry
sinestro_job = {
    "id": str(uuid.uuid4()).lower(),
    "agentId": "sinestro",
    "name": "Sinestro Daily Strategy",
    "enabled": True,
    "createdAtMs": int(time.time() * 1000),
    "updatedAtMs": int(time.time() * 1000),
    "schedule": {
        "kind": "cron",
        "expr": "0 7 * * *"
    },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "payload": {
        "kind": "agentTurn",
        "message": "You are Sinestro. Execute your daily strategic analysis: 1) Review all agent workspace status (Grodd, Cheetah, Riddler, Brainiac, Toyman, Grundy), 2) Identify any bottlenecks or risks in the system, 3) Propose strategic improvements or optimizations, 4) Check for any overdue tasks or missed deliverables, 5) Report your findings with actionable recommendations. Deliver your strategic assessment with precision and authority.",
        "model": "nvidia-nim/moonshotai/kimi-k2.5"
    },
    "delivery": {
        "mode": "announce",
        "channel": "last",
        "to": "1474823021440012521"
    },
    "state": {
        "nextRunAtMs": None,
        "lastRunAtMs": None,
        "lastRunStatus": None,
        "lastStatus": None,
        "lastDurationMs": None,
        "lastDeliveryStatus": None,
        "consecutiveErrors": 0,
        "lastDelivered": None
    }
}

# Check if Sinestro job already exists
existing = [j for j in data['jobs'] if j.get('agentId') == 'sinestro' and 'Sinestro Daily Strategy' in j.get('name', '')]
if existing:
    print("Sinestro cron job already exists:", existing[0]['id'])
    exit(0)

# Add to jobs list
data['jobs'].append(sinestro_job)

# Write back
with open('/Users/chimpman/.openclaw/cron/jobs.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"✓ Added Sinestro cron job (ID: {sinestro_job['id']})")
print(f"  Schedule: 7:00 AM PST daily (0 7 * * *)")
print(f"  Total jobs: {len(data['jobs'])}")
