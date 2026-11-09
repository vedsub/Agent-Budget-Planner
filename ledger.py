# ledger.py

def reserve(
    limit: int, 
    spent: int, 
    holds: dict[str, int], 
    request_id: str, 
    amount: int
) -> dict[str, int]:
    """
    Attempts to reserve budget for a new request.
    Returns a newly allocated holds dictionary if successful.
    Raises ValueError if capacity is insufficient or the request_id exists.
    """
    
    # Validation (preventing booleans and negatives)
    if type(limit) is bool or type(spent) is bool or type(amount) is bool:
        raise TypeError("Numerical values cannot be booleans.")
    if limit < 0 or spent < 0 or amount < 0:
        raise ValueError("Limit, spent, and amount must be non-negative integers.")
    if not request_id:
        raise ValueError("request_id cannot be empty.")

    # 1. Check request identity FIRST (reject duplicate IDs)
    if request_id in holds:
        raise ValueError(f"Duplicate request ID rejected: {request_id}")

    # 2. Read the ledger
    current_reserved = sum(holds.values())
    available = limit - spent - current_reserved

    # 3. Reject without mutation if capacity is insufficient
    if amount > available:
        raise ValueError(
            f"Insufficient capacity. Available: {available} units, "
            f"Requested: {amount} units."
        )

    # 4. Admission and reservation in one transition
    # We copy the dictionary so we don't mutate the caller's state unexpectedly.
    new_holds = holds.copy()
    new_holds[request_id] = amount

    return new_holds