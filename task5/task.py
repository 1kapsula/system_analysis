import json

def build_index_map(ranking):
    index_map = {}
    position = 0
    for group in ranking:
        if isinstance(group, list):
            for elem in group:
                index_map[elem] = position
        else:
            index_map[group] = position
        position += 1
    return index_map

def process_matrices(matrix_a, matrix_b, transpose=False):
    size = len(matrix_a)
    result_matrix = [[0] * size for _ in range(size)]
    
    if transpose:
        matrix_a = [[matrix_a[j][i] for j in range(size)] for i in range(size)]
        matrix_b = [[matrix_b[j][i] for j in range(size)] for i in range(size)]
        
    for i in range(size):
        for j in range(size):
            result_matrix[i][j] = matrix_a[i][j] * matrix_b[i][j]
    return result_matrix

def build_relation_matrix(index_map):
    size = len(index_map)
    relation_matrix = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if index_map.get(i + 1, size) >= index_map.get(j + 1, size):
                relation_matrix[i][j] = 1
    return relation_matrix

def main(ranking_a: str, ranking_b: str) -> str:
    rank_a = json.loads(ranking_a)
    rank_b = json.loads(ranking_b)

    # Построение матриц отношений для каждой из ранжировок
    matrix_a = build_relation_matrix(build_index_map(rank_a))
    matrix_b = build_relation_matrix(build_index_map(rank_b))

    # Перемножение матриц и транспонированных матриц
    conflict_matrix = process_matrices(matrix_a, matrix_b)
    transposed_conflict_matrix = process_matrices(matrix_a, matrix_b, transpose=True)

    # Определение ядра противоречий
    conflict_core = []
    for i in range(len(conflict_matrix)):
        for j in range(i + 1, len(conflict_matrix[0])):
            if conflict_matrix[i][j] + transposed_conflict_matrix[i][j] == 0:
                conflict_core.append([i + 1, j + 1])

    return json.dumps(conflict_core)

if __name__ == "__main__":
    # Примеры входных данных
    ranking_json_a = "[1,[2,3],4,[5,6,7],8,9,10]"
    ranking_json_b = "[[1,2],[3,4,5],6,7,9,[8,10]]"
    # Вызов функции main и печать результата
    print(main(ranking_json_a, ranking_json_b))
