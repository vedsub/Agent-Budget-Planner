# scheduler.py

def schedule(limit: int, deadline: int, jobs: list[dict]) -> list[dict]:
    """
    Deterministically replays an ordered queue of jobs against time and budget limits.
    Returns a trace of completed and rejected events.
    """
    
    # 0. Strict validation
    if type(limit) is bool or type(deadline) is bool:
        raise TypeError("Limits cannot be booleans.")
    if limit < 0 or deadline < 0:
        raise ValueError("Budget limit and deadline must be non-negative integers.")
        
    spent = 0
    elapsed = 0
    events = []
    
    # 1. Read the ordered queue
    for job in jobs:
        job_id = job.get("id")
        cost = job.get("cost", 0)
        duration = job.get("duration", 0)
        
        # 2. Check Deadline Gate
        if elapsed + duration > deadline:
            events.append({
                "job_id": job_id,
                "status": "rejected",
                "reason": "deadline"
            })
            continue # Job dropped, do not advance time or budget
            
        # 3. Check Budget Gate
        if spent + cost > limit:
            events.append({
                "job_id": job_id,
                "status": "rejected",
                "reason": "budget"
            })
            continue # Job dropped, do not advance time or budget
            
        # 4. Reserve capacity and complete (Simulator mode)
        spent += cost
        elapsed += duration
        events.append({
            "job_id": job_id,
            "status": "completed"
        })
        
    return events