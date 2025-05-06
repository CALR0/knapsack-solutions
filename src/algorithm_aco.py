import numpy as np
import matplotlib.pyplot as plt
import time
import os
from collections import Counter
import pandas as pd

current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, "data", "Mochila_capacidad_maxima_4kg.xlsx")
data = pd.read_excel(file_path)

items_tup = [(int(data.iloc[i, 0]), float(data.iloc[i, 1]), int(data.iloc[i, 2]), int(data.iloc[i, 3])) for i in range(len(data))]
start_time = time.time()
items = np.array(items_tup)

max_weight = 4.0  # in kg

# Configurable Parameters
num_ants = 30
num_iterations = 100
initial_pheromone = 0.6     
evaporation = 0.4         
alpha = 1.5        
beta = 0.5

# Initialize pheromones
pheromones = np.ones(len(items)) * initial_pheromone
best_global_value = 0
best_global_solution = []
best_values_per_iteration = []

# Function to select item for the current ant
def select_item(current_weight, selected):
    available_weights = items[:, 1] <= (max_weight - current_weight)
    available_quantities = np.array([items[i, 3] - selected.count(i) for i in range(len(items))]) > 0
    heuristic_value = items[:, 2] ** beta
    probabilities = (pheromones ** alpha) * heuristic_value * available_weights * available_quantities
    if probabilities.sum() == 0:
        return None
    probabilities /= probabilities.sum()
    return np.random.choice(range(len(items)), p=probabilities)

# Main loop
for iteration in range(num_iterations):
    best_value_iteration = 0
    best_solution_iteration = []
    for ant in range(num_ants):
        current_solution = []
        selected_items = []
        current_value = 0
        current_weight = 0
        while True:
            item = select_item(current_weight, selected_items)
            if item is None or current_weight + items[item, 1] > max_weight:
                break
            current_solution.append(item)
            selected_items.append(item)
            current_value += items[item, 2]
            current_weight += items[item, 1]

        if current_value > best_value_iteration:
            best_value_iteration = current_value
            best_solution_iteration = current_solution

    if best_value_iteration > best_global_value:
        best_global_value = best_value_iteration
        best_global_solution = best_solution_iteration

    best_values_per_iteration.append(best_value_iteration)

    for item in range(len(items)):
        pheromones[item] = (1 - evaporation) * pheromones[item] + \
                           sum([items[item, 2] for s in best_solution_iteration if s == item]) / \
                           (best_value_iteration if best_value_iteration > 0 else 1)

finish_time = time.time()
duration = finish_time - start_time
best_solution_index = best_values_per_iteration.index(best_global_value)

# Count quantity of each selected item
solution_counter = Counter(best_global_solution)
full_solution = [solution_counter.get(i, 0) for i in range(len(items))]

# Function to save results to Excel with sequential ID
def save_results_to_excel(best_value, elapsed_time, best_iteration, best_weight, best_solution):
    output_file = 'results_aco.xlsx'
    
    if os.path.isfile(output_file):
        try:
            existing = pd.read_excel(output_file)
            run_id = existing['Run'].max() + 1
        except:
            existing = pd.DataFrame()
            run_id = 1
    else:
        existing = pd.DataFrame()
        run_id = 1

    new_record = pd.DataFrame({
        'Run': [run_id],
        'Best Value': [best_value],
        'Time (s)': [elapsed_time],
        'Iteration': [best_iteration],
        'Weight (kg)': [best_weight],
        'Best Solution': [str(best_solution)]
    })

    results = pd.concat([existing, new_record], ignore_index=True)
    results.to_excel(output_file, index=False)

# Output results
print("Ant Colony Optimization Algorithm")
print(f"Execution time (s): {duration:.4f}")
print(f"Best solution found at iteration: {best_solution_index}")
print(f"Best Global Solution (Selected Quantity per Item): {full_solution}")
print(f"Best Global Value: {best_global_value}")
print(f"Total Weight (kg): {sum(items[s, 1] for s in best_global_solution):.3f}")

# Save to Excel
save_results_to_excel(best_global_value, duration, best_solution_index + 1,
                      sum(items[s, 1] for s in best_global_solution), full_solution)

# Plot convergence
plt.plot(best_values_per_iteration, label='Best Value per Iteration')
plt.title('Convergence of ACO Algorithm')
plt.xlabel('Iteration')
plt.ylabel('Best Value')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()