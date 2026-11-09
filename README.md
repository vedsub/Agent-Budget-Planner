# Agent Budget Planner

This project implements a financial controller and deterministic admission simulator for autonomous Large Language Model (LLM) agents. It provides a robust state machine to manage token budgets and execution deadlines, ensuring agents do not overdraw funds or breach time limits during asynchronous API operations.

This was built as a standalone exploration of financial invariants, atomic state transitions, and deterministic system simulations.

## The Core Problem

When LLM agents run in autonomous loops, they consume unpredictable amounts of compute. If an agent fires multiple concurrent requests, standard budget checks fail because the actual cost isn't known until the generation finishes. This project solves that by implementing a **reservation and settlement ledger** using strict integer arithmetic to prevent floating-point drift.

## Key Concepts & Architecture

The project is structured across four core modules, each addressing a specific distributed systems or accounting challenge.

### 1. Integer-Based Cost Estimation (`estimator.py`)

Floating-point arithmetic introduces microscopic rounding errors which are unacceptable in financial systems.

* **Design Decision:** All token rates and costs are calculated as exact integers using a granular base unit (teaching units).
* **Ceiling Calculation:** Because LLM outputs are unpredictable, the estimator calculates the absolute worst-case scenario (Input Tokens × Input Rate + Output Ceiling × Output Rate) before a request is authorised.

### 2. Atomic Budget Reservation (`ledger.py` - `reserve`)

Checking a budget and deducting from it must happen simultaneously to prevent race conditions where concurrent requests double-spend the same available funds.

* **Holds vs. Spent:** The ledger maintains two separate pools: `spent` (finalised receipts) and `holds` (reserved ceilings for in-flight requests).
* **Idempotency:** The state machine explicitly rejects duplicate request IDs to prevent double-charging on network retries.
* **Immutability:** If a reservation fails, the function rejects the mutation entirely, preserving the exact prior state.

### 3. Receipt Settlement & Reconciliation (`ledger.py` - `settle`)

When a request completes, it almost always costs less than the reserved ceiling.

* **Partitioning the Hold:** The system splits the hold, moving the actual cost into the `spent` ledger and releasing the unused remainder back into the available pool.
* **Accounting Invariants:** If an API returns an actual cost higher than the reserved ceiling, the system halts and throws a violation rather than silently pushing the account into a negative balance.
* **Phantom Liabilities:** If a receipt goes missing (e.g., the callback crashes), the system retains the hold. Releasing it would falsely inflate the available budget, hiding an unknown liability.

### 4. Deterministic Admission Simulation (`scheduler.py`)

A simulator that evaluates a queue of expected jobs against strict time and budget limits without making live API calls.

* **Sequential Gating:** Every job must pass a Deadline Gate and a Budget Gate.
* **Event Trace:** It outputs a JSON-friendly trace logging exact reasons for rejection (e.g., `rejected for budget`) or a `completed` status, allowing developers to audit the admission decisions.
* **Synchronous Limitations:** It highlights a key software boundary: a monotonic deadline gate can prevent the *next* job from dispatching, but it cannot interrupt a synchronous callback that is already running.

## Scope and Limitations

* **Single-Process State Machine:** This is an in-memory implementation demonstrating the invariants. If deployed as a live microservice, the `reserve` transition requires an external lock (e.g., PostgreSQL `SELECT ... FOR UPDATE` or a Redis transaction).
* **Arbitrary Units:** The current implementation uses integer "teaching units." In production, this maps directly to micro-cents or a provider's fractional token billing rates.

## Directory Structure

```text
Agent-Budget-Planner/
├── cli.py                 # Command-line driver handling file I/O
├── estimator.py           # Core logic for integer cost estimation
├── ledger.py              # State machine for reservations and settlements
├── scheduler.py           # Deterministic queue replay simulator
├── test_ledger.py         # Concrete test cases for state transitions
├── test_scheduler.py      # Concrete test cases for the admission gates
└── samples/
    └── input.json         # Sample payload for CLI execution

```

## How to Run

**1. Run the CLI Estimator:**

```bash
python3 cli.py samples/input.json --mode execute --output budget.json

```

**2. Test the Ledger (Reservations & Settlements):**

```bash
python3 test_ledger.py

```

**3. Test the Scheduler Trace:**

```bash
python3 test_scheduler.py

```