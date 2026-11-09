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
  
# ledger.py (append this below the reserve function)

def settle(
    spent: int,
    holds: dict[str, int],
    closed_requests: set[str],
    request_id: str,
    actual_cost: int,
    receipt_missing: bool = False
) -> tuple[int, dict[str, int], set[str]]:
    """
    Settles a reservation, converting actual usage to spent and releasing the remainder.
    Returns (new_spent, new_holds, new_closed_requests).
    """
    # 0. Strict type validation
    if type(spent) is bool or type(actual_cost) is bool:
        raise TypeError("Numerical values cannot be booleans.")
    if spent < 0 or actual_cost < 0:
        raise ValueError("Spent and actual cost must be non-negative integers.")
    if type(receipt_missing) is not bool:
        raise TypeError("receipt_missing must be a boolean.")

    # 1. Reject duplicate receipts
    if request_id in closed_requests:
        raise ValueError(f"Duplicate receipt rejected. Request '{request_id}' is already settled.")

    # 2. Handle missing receipts
    if receipt_missing:
        raise ValueError(f"Receipt missing for '{request_id}'. Hold preserved for reconciliation.")

    # 3. Locate reservation
    if request_id not in holds:
        raise ValueError(f"No active hold found for request '{request_id}'.")

    reserved_amount = holds[request_id]

    # 4. Validate receipt against the ceiling
    if actual_cost > reserved_amount:
        raise ValueError(
            f"Accounting violation: Actual cost ({actual_cost}) exceeds "
            f"reserved ceiling ({reserved_amount}). Ledger unchanged."
        )

    # 5. Commit settlement (Partition the hold)
    new_spent = spent + actual_cost
    
    new_holds = holds.copy()
    del new_holds[request_id]
    
    new_closed = closed_requests.copy()
    new_closed.add(request_id)

    return new_spent, new_holds, new_closed