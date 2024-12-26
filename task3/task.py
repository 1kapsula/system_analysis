import json
import math

class GraphProcessor:
    def __init__(self):
        self.graph_structure = {}
        self.neighbor_map = {}
        self.child_structure = {}
        self.visited_nodes = []
        self.all_nodes = set()
        self.root_node = ""

    # Функция для построения списка соседей
    def get_neighbors(self, neighbors):
        for i in range(len(neighbors)):
            self.neighbor_map[neighbors[i]] = [
                neighbors[j] for j in range(len(neighbors)) if i != j
            ]

    # Рекурсивная функция обхода графа и создания карты дочерних узлов(DFS)
    def dfs_graph(self, structure, node):
        self.visited_nodes.append(node)
        self.get_neighbors(structure[node])
        descendants = []
        for child in structure[node]:
            descendants.append(child)
            if child not in self.visited_nodes:
                child_descendants = self.dfs_graph(structure, child)
                self.child_structure[child] = child_descendants
                descendants.extend(child_descendants)
        return descendants

    # конвертация JSON в структуру графа
    def convert_json_to_graph(self, json_data):
        current_nodes = []
        for parent, children in json_data.items():
            if self.root_node == "":
                self.root_node = parent
            current_nodes.append(parent)
            child_nodes = self.convert_json_to_graph(children)
            self.graph_structure[parent] = child_nodes
        self.all_nodes.update(current_nodes)
        return current_nodes

    # функция для вычисления значений r1 - r5
    def calculate_r(self, target_node, r_type):
        if r_type == 1:
            # r1: непосредственное управление
            return len(self.graph_structure[target_node]) if target_node in self.graph_structure else 0
        elif r_type == 2:
            # r2: непосредственное подчинение
            return int(any(target_node in descendants for descendants in self.graph_structure.values()))
        elif r_type == 3:
            # r3: опосредованное управление
            return len(self.child_structure[target_node]) - len(self.graph_structure[target_node]) if target_node in self.child_structure and target_node in self.graph_structure else 0
        elif r_type == 4:
            # r4: опосредованное подчинение
            parent_count = sum(1 for descendants in self.child_structure.values() if target_node in descendants)
            return max(0, parent_count - 1)
        elif r_type == 5:
            # r5: соподчинение на одном уровне
            return len(self.neighbor_map[target_node]) if target_node in self.neighbor_map else 0
        return 0
    # функция для расчета энтропии
    def calculate_entropy(self, extensional_lengths):
        H = 0.0
        n = len(extensional_lengths)
        for i in range(n):
            for j in range(len(extensional_lengths[i])):
                if extensional_lengths[i][j] != 0:
                    p = extensional_lengths[i][j] / (n - 1)
                    H -= p * math.log2(p)
        return round(H, 1)
    
    def execute(self, input_data: str):
        # Загружаем JSON в виде словаря и преобразуем в структуру графа
        parsed_tree = json.loads(input_data)
        self.convert_json_to_graph(parsed_tree)
        
        # Обход графа для формирования child_structure и neighbor_map
        self.child_structure[self.root_node] = self.dfs_graph(self.graph_structure, self.root_node)
        self.neighbor_map[self.root_node] = []
        
        extensional_lengths = []
        for node in sorted(self.all_nodes, key=lambda x: int(x)):
            node_characteristics = [self.calculate_r(node, r) for r in range(1, 6)]
            extensional_lengths.append(node_characteristics)
            print(f"{node}: {node_characteristics}")

        # Расчет энтропии для графа на основе матрицы экстенсиональных длин
        entropy = self.calculate_entropy(extensional_lengths)
        print(f"Энтропия графа: {entropy}")

def main(input_json: str):
    processor = GraphProcessor()
    processor.execute(input_json)

if __name__ == "__main__":
    example_tree = """{
        "1": {
            "2": {
            },
            "3": {
                "4": {},
                "5": {}
            }
        }
    }"""
    main(example_tree)
    