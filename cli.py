import argparse
import json
from estimator import estimate

def main():
    parser = argparse.ArgumentParser(description="Agent Budget Planner CLI")
    parser.add_argument("input_file", help="Path to input JSON")
    parser.add_argument("--mode", required=True, choices=["execute"], help="Run mode")
    parser.add_argument("--output", required=True, help="Path to output JSON")
    
    args = parser.parse_args()

    # Read the input payload
    with open(args.input_file, 'r') as f:
        data = json.load(f)

    req = data.get("request", {})
    rates = data.get("rates", {})

    # Execute the core function
    try:
        total_cost = estimate(
            input_tokens=req.get("input_tokens", 0),
            output_ceiling=req.get("output_ceiling", 0),
            input_rate=rates.get("input_rate", 0),
            output_rate=rates.get("output_rate", 0)
        )
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")
        return

    # Write the result
    result = {"estimate": total_cost}
    with open(args.output, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"Estimate calculated: {total_cost} units.")

if __name__ == "__main__":
    main()