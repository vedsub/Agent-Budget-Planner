# test_scheduler.py
from scheduler import schedule
import json

print("--- Stage 4: Scheduler Trace ---")

limit = 100
deadline = 100

jobs = [
    {"id": "A", "cost": 60, "duration": 40},
    {"id": "B", "cost": 50, "duration": 30},
    {"id": "C", "cost": 30, "duration": 80},
    {"id": "D", "cost": 20, "duration": 20}
]

print(f"Initial Budget: {limit} units | Deadline: {deadline} ms\n")

trace = schedule(limit=limit, deadline=deadline, jobs=jobs)

# Pretty print the trace array just like a JSON output
print(json.dumps(trace, indent=2))