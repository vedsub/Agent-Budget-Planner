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