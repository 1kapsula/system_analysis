import math

def calculate_state_frequencies():
    sum_states = {}
    product_states = {}
    combined_states = {}
    
    for i in range(1, 7):
        for j in range(1, 7):
            sum_val = i + j
            product_val = i * j
            combined_key = f"{sum_val}-{product_val}"

            sum_states[sum_val] = sum_states.get(sum_val, 0) + 1
            product_states[product_val] = product_states.get(product_val, 0) + 1
            combined_states[combined_key] = combined_states.get(combined_key, 0) + 1
    
    return sum_states, product_states, combined_states


def calculate_entropy(states):
    entropy = 0.0
    total_count = sum(states.values())
    for count in states.values():
        probability = count / total_count
        entropy -= probability * math.log2(probability)
    return entropy


def calculate_entropy_metrics():
    sum_states, product_states, combined_states = calculate_state_frequencies()
    
    entropy_combined = calculate_entropy(combined_states)
    entropy_sum = calculate_entropy(sum_states)
    entropy_product = calculate_entropy(product_states)
    conditional_entropy = entropy_combined - entropy_sum
    mutual_information = entropy_product - conditional_entropy

    return [
        round(entropy_combined, 2),
        round(entropy_sum, 2),
        round(entropy_product, 2),
        round(conditional_entropy, 2),
        round(mutual_information, 2)
    ]

def main():
    print(calculate_entropy_metrics())

if __name__ == "__main__":
    main()
