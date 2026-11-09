def estimate(input_tokens: int, output_ceiling: int, input_rate: int, output_rate: int) -> int:
    """
    Estimates the worst-case cost of an LLM request in integer teaching units.
    """
    operands = {
        "input_tokens": input_tokens,
        "output_ceiling": output_ceiling,
        "input_rate": input_rate,
        "output_rate": output_rate
    }
    
    # 1. Validate operands
    for name, value in operands.items():
        if isinstance(value, bool):
            raise TypeError(f"{name} cannot be a boolean.")
        if not isinstance(value, int):
            raise TypeError(f"{name} must be an integer.")
        if value < 0:
            raise ValueError(f"{name} must be a non-negative integer.")

    # 2. Price the prompt
    prompt_cost = input_tokens * input_rate
    
    # 3. Price the output ceiling
    ceiling_cost = output_ceiling * output_rate
    
    # 4. Add the estimate
    return prompt_cost + ceiling_cost