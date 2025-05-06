import random
import math
import time
import matplotlib.pyplot as plt
import pandas as pd
import os

backpack_capacity = 4.0  # en kg
run_number = 1

# Configurable Parameters
initial_temperature = 500
cooling_factor = 0.9998
total_iterations = 30000
final_temperature = 0.0001

current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, "data", "Mochila_capacidad_maxima_4kg.xlsx")
df = pd.read_excel(file_path)

items = []
for _, row in df.iterrows():
    items.append({
        'id': row['Id'],
        'value': row['Valor'],
        'weight': row['Peso_kg'],  # se mantiene en kg
        'available_quantity': int(row['Cantidad'])
    })

class KnapsackProblem:
    def __init__(self, items, capacity):
        self.items = items 
        self.capacity = capacity

    def total_value(self, solution):
        return sum(self.items[i]["value"] * solution[i] for i in range(len(self.items)))

    def total_weight(self, solution):
        return sum(self.items[i]["weight"] * solution[i] for i in range(len(self.items)))

    def generate_initial_solution(self):
        solution = [0] * len(self.items)
        total_weight = 0
        while total_weight <= self.capacity:
            i = random.randint(0, len(self.items) - 1)
            if (total_weight + self.items[i]["weight"] <= self.capacity) and (solution[i] < self.items[i]["available_quantity"]):
                solution[i] += 1
                total_weight += self.items[i]["weight"]
            else:
                break
        return solution

    def neighbor_solution(self, current_solution):
        neighbor = current_solution.copy()
        for i in range(len(neighbor)):
            if random.random() < 0.1:
                max_quantity = int(self.items[i]["available_quantity"])
                neighbor[i] = random.randint(0, max_quantity)
        return neighbor

    def acceptance(self, delta_value, temperature):
        if delta_value >= 0:
            return 1.0
        elif temperature == 0:
            return 0.0
        else:
            return math.exp(delta_value / temperature)

    def cooling(self, initial_temp, alpha, iteration, total_iterations, final_temp):
        new_temp = initial_temp * (1.0 - iteration / total_iterations) ** alpha
        return max(new_temp, final_temp)

    def solve(self, initial_temperature, cooling_factor, total_iterations, final_temperature):
        best_solution = self.generate_initial_solution()
        best_value = self.total_value(best_solution)
        best_weight = self.total_weight(best_solution)
        best_iteration = 0

        current_solution = best_solution.copy()
        current_value = best_value
        current_weight = best_weight

        start_time = time.time()
        optimal_values = []

        for i in range(total_iterations):
            neighbor = self.neighbor_solution(current_solution)
            neighbor_value = self.total_value(neighbor)
            neighbor_weight = self.total_weight(neighbor)

            if neighbor_weight <= self.capacity:
                delta = neighbor_value - current_value
                if self.acceptance(delta, initial_temperature) > random.random():
                    current_solution = neighbor
                    current_value = neighbor_value
                    current_weight = neighbor_weight
                    if current_value > best_value:
                        best_solution = current_solution
                        best_value = current_value
                        best_weight = current_weight
                        best_iteration = i

            initial_temperature = self.cooling(initial_temperature, cooling_factor, i, total_iterations, final_temperature)
            optimal_values.append(best_value)

        total_time = time.time() - start_time
        return best_solution, best_value, best_weight, total_time, optimal_values, best_iteration

def save_results_to_excel(run_number, value, time, iteration, weight, solution):
    file = 'results_sa.xlsx'
    if os.path.isfile(file):
        results = pd.read_excel(file)
        last_run = results['Run'].max() if 'Run' in results.columns else 0
        run_number = last_run + 1
    else:
        results = pd.DataFrame(columns=['Run', 'Best Value', 'Time (s)', 'Iteration', 'Weight (kg)', 'Best Solution'])

    new_record = pd.DataFrame([{
        'Run': run_number,
        'Best Value': value,
        'Time (s)': time,
        'Iteration': iteration,
        'Weight (kg)': weight,
        'Best Solution': str(solution)
    }])

    results = pd.concat([results, new_record], ignore_index=True)
    results.to_excel(file, index=False)

# Running the algorithm
problem = KnapsackProblem(items, backpack_capacity)
solution, value, weight, time, history, iteration = problem.solve(initial_temperature, cooling_factor, total_iterations, final_temperature)

# Printing results
print(f"Best solution found at iteration: {iteration}")
print(f"Execution time (s): {time:.4f}")
print("Optimal solution:", solution)
print("Optimal value:", value)
print(f"Total weight: {weight:.2f} kg")

# Save to Excel
save_results_to_excel(run_number, value, time, iteration, weight, solution)

# Plot convergence
plt.plot(history)
plt.xlabel('Iteration')
plt.ylabel('Optimal value')
plt.title('Simulated Annealing Convergence')
plt.grid(True)
plt.show()
