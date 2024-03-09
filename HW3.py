import numpy as np

def read_graph(file_path):
    distances = []
    with open(file_path, 'r') as file:
        lines = file.readlines()[2:]  # 从第三行开始读取
        for line in lines:
            parts = line.strip().split()
            try:
                # 尝试将前两个值转换为整数，第三个值转换为浮点数
                i, j = map(int, parts[:2])
                dist = float(parts[2])
                distances.append((i, j, dist))
            except ValueError:
                # 如果转换失败，跳过这行数据
                continue

    # 假设节点是从0开始编号，直到最大索引
    max_node_index = max(max(i, j) for i, j, dist in distances)
    size = max_node_index + 1
    distance_matrix = np.zeros((size, size))

    for i, j, dist in distances:
        distance_matrix[i][j] = dist
        distance_matrix[j][i] = dist  # 无向图，所以需要设置两次

    return distance_matrix


def simulated_annealing(distance_matrix, initial_temp=10000, cooling_rate=0.99, stopping_temp=1):
    current_solution = np.random.permutation(range(len(distance_matrix)))
    current_cost = calculate_total_distance(current_solution, distance_matrix)
    best_solution = np.copy(current_solution)
    best_cost = current_cost
    temperature = initial_temp

    iteration_count = 0  # 新增：用于跟踪算法尝试的循环数量

    while temperature > stopping_temp:
        new_solution = np.copy(current_solution)
        i, j = np.random.randint(0, len(new_solution), size=2)
        new_solution[i], new_solution[j] = new_solution[j], new_solution[i]  # Swap two cities
        new_cost = calculate_total_distance(new_solution, distance_matrix)

        if new_cost < current_cost or np.random.rand() < np.exp((current_cost - new_cost) / temperature):
            current_solution = new_solution
            current_cost = new_cost

            if new_cost < best_cost:
                best_solution = np.copy(new_solution)
                best_cost = new_cost

        temperature *= cooling_rate
        iteration_count += 1  # 每次循环，计数器加1

    return best_solution, best_cost, iteration_count  # 返回最佳解、最佳成本和循环数量


# Calculate total distance
def calculate_total_distance(solution, distance_matrix):
    return sum(distance_matrix[solution[i - 1], solution[i]] for i in range(len(solution)))


# Example usage
file_path = '/Users/howard/Documents/PyCharmProjects/EEC289Q/HW1/pythonProject/1000_euclidianDistance.txt'  # Replace this with the actual file path
# file_path = '/Users/howard/Documents/PyCharmProjects/EEC289Q/HW1/pythonProject/1000_randomDistance.txt'  # Replace this with the actual file path
distance_matrix = read_graph(file_path)
best_solution, best_cost, iteration_count = simulated_annealing(distance_matrix)
# print("Best solution:", best_solution)

# 如果希望输出更加美观，可以这样做
formatted_solution = ' '.join(map(str, best_solution))
print("Formatted Best Solution Path:")
print(formatted_solution)

print("Best cost:", round(best_cost, 2))  # 四舍五入到小数点后两位

print("Iterations (cycles) evaluated: {:.2e}".format(iteration_count))

