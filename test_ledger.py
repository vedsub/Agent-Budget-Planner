from ledger import reserve

# The concrete case from Stage 2
limit = 100
spent = 20
holds = {"A": 30}

print(f"Initial State -> Limit: {limit}, Spent: {spent}, Holds: {holds}\n")

# 1. Test insufficient capacity
try:
    print("Attempting to reserve 60 for request 'B'...")
    new_holds = reserve(limit, spent, holds, request_id="B", amount=60)
except ValueError as e:
    print(f"Failed as expected: {e}\n")

# 2. Test duplicate ID
try:
    print("Attempting to reserve 1 for existing request 'A'...")
    new_holds = reserve(limit, spent, holds, request_id="A", amount=1)
except ValueError as e:
    print(f"Failed as expected: {e}\n")

# 3. Test successful reservation
print("Attempting to reserve 40 for request 'C'...")
new_holds = reserve(limit, spent, holds, request_id="C", amount=40)
print(f"Success! New Holds dictionary: {new_holds}")



# test_ledger.py (append this to the bottom of the file)
from ledger import settle

print("\n--- Stage 3: Settlement Tests ---")

spent = 20
holds = {"A": 70}
closed_requests = set()

print(f"Initial State -> Spent: {spent}, Holds: {holds}, Closed: {closed_requests}\n")

# 1. Test missing receipt
try:
    print("Attempting settlement with missing receipt...")
    new_state = settle(spent, holds, closed_requests, "A", actual_cost=0, receipt_missing=True)
except ValueError as e:
    print(f"Failed as expected: {e}")
    print(f"State preserved -> Holds: {holds}\n")

# 2. Test over-ceiling violation
try:
    print("Attempting to settle 71 units on a 70 unit hold...")
    new_state = settle(spent, holds, closed_requests, "A", actual_cost=71)
except ValueError as e:
    print(f"Failed as expected: {e}\n")

# 3. Test successful settlement (20 units actual)
print("Attempting successful settlement of 20 units...")
spent, holds, closed_requests = settle(spent, holds, closed_requests, "A", actual_cost=20)
print(f"Success! State Transitioned -> Spent: {spent}, Holds: {holds}, Closed: {closed_requests}\n")

# 4. Test duplicate receipt
try:
    print("Attempting to submit receipt for 'A' again...")
    new_state = settle(spent, holds, closed_requests, "A", actual_cost=20)
except ValueError as e:
    print(f"Failed as expected: {e}\n")