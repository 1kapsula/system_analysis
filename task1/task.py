import json

# Функция для получения всех потомков вершины
def get_descendants(node):
    descendants = []
    for child, subchildren in node.items():
        descendants.append(child)
        descendants.extend(get_descendants(subchildren))
    return descendants

# Функция для обхода графа и получения братьев и потомков
def get_siblings_and_descendants(node, parent=None):
    siblings_and_descendants = {}
    
    for key, children in node.items():
        # Получаем список братьев
        siblings = [sibling for sibling in node if sibling != key]
        
        # Получаем список потомков
        descendants = get_descendants(children)
        
        # Сохраняем данные для текущей вершины
        siblings_and_descendants[key] = {
            "siblings": siblings,
            "descendants": descendants
        }
        
        # Рекурсивно обрабатываем детей
        siblings_and_descendants.update(get_siblings_and_descendants(children, key))
    
    return siblings_and_descendants

def main(input_json: str):
    # Загружаем JSON в виде словаря
    tree = json.loads(input_json)

    # Получаем результат
    result = get_siblings_and_descendants(tree)

    for key, value in result.items():
        print(f"Вершина {key}:")
        print(f"  Братья: {value['siblings']}")
        print(f"  Потомки: {value['descendants']}")

if __name__ == "__main__":
    example_str = """{
        "1": {
            "2": {
                "3": {
                    "5": {},
                    "6": {}
                },
                "4": {
                    "7": {},
                    "8": {}
                }
            }
        }
    }"""
    main(example_str)