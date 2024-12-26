import json
from typing import List, Dict, Tuple, Callable

STEP_SIZE = 0.01

class FuzzyRange:
    def __init__(self, start: float, end: float, start_core: bool, end_core: bool):
        self.start = start
        self.end = end
        self.start_core = start_core
        self.end_core = end_core

    def membership_function(self) -> Callable[[float], float]:
        if self.start_core and self.end_core:
            return lambda x: 1.0
        elif not self.start_core and not self.end_core:
            return lambda x: 0.0
        elif self.start_core:
            return lambda x: 1.0 - (x - self.start) / (self.end - self.start)
        else:
            return lambda x: (x - self.start) / (self.end - self.start)

class FuzzySet:
    def __init__(self, data: Dict):
        self.name = data['id']
        self.ranges = []
        for i in range(len(data['points']) - 1):
            self.ranges.append(FuzzyRange(
                start=data['points'][i][0],
                end=data['points'][i + 1][0],
                start_core=bool(data['points'][i][1]),
                end_core=bool(data['points'][i + 1][1]),
            ))

    def compute_membership(self, value: float) -> float:
        for fuzzy_range in self.ranges:
            if fuzzy_range.start <= value < fuzzy_range.end:
                return fuzzy_range.membership_function()(value)
        if value < self.ranges[0].start:
            return 1.0 if self.ranges[0].start_core else 0.0
        return 1.0 if self.ranges[-1].end_core else 0.0

class FuzzySystem:
    def __init__(self, regulator_data: str, temperature_data: str, mapping_data: str):
        self.regulators = self._parse_sets(json.loads(regulator_data))
        self.temperatures = self._parse_sets(json.loads(temperature_data))
        self.mapping = {pair[0]: pair[1] for pair in json.loads(mapping_data)}

    @staticmethod
    def _parse_sets(data: Dict) -> Dict[str, FuzzySet]:
        sets = {}
        for category in data.values():
            for item in category:
                fuzzy_set = FuzzySet(item)
                sets[fuzzy_set.name] = fuzzy_set
        return sets

    def calculate_output(self, current_temperature: float) -> float:
        temp_memberships = {
            temp_name: temp_set.compute_membership(current_temperature)
            for temp_name, temp_set in self.temperatures.items()
        }

        min_output, max_output = float('inf'), float('-inf')
        for reg_set in self.regulators.values():
            min_output = min(min_output, reg_set.ranges[0].start)
            max_output = max(max_output, reg_set.ranges[-1].end)

        best_output, highest_membership = min_output, 0.0
        current_value = min_output

        while current_value <= max_output:
            membership_values = []
            for temp_name, reg_name in self.mapping.items():
                temp_mu = temp_memberships[temp_name]
                reg_mu = self.regulators[reg_name].compute_membership(current_value)
                membership_values.append(min(temp_mu, reg_mu))

            max_membership = max(membership_values)
            if max_membership > highest_membership:
                highest_membership = max_membership
                best_output = current_value

            if highest_membership == 1.0:
                break

            current_value += STEP_SIZE

        return best_output

def main(regulator_json: str, temperature_json: str, mapping_json: str):
    fuzzy_system = FuzzySystem(regulator_json, temperature_json, mapping_json)

    print(f"Temperature: 19.0, Output: {round(fuzzy_system.calculate_output(19.0), 2)}")
    print(f"Temperature: 23.0, Output: {round(fuzzy_system.calculate_output(23.0), 2)}")
    print(f"Temperature: 10.0, Output: {round(fuzzy_system.calculate_output(10.0), 2)}")

if __name__ == "__main__":
    regulator_json = '''{
        "регуляторы": [
            {"id": "низкий", "points": [[0,0], [0,1], [5,1], [8,0]]},
            {"id": "средний", "points": [[5,0], [8,1], [13,1], [16,0]]},
            {"id": "высокий", "points": [[13,0], [18,1], [23,1], [26,0]]}
        ]
    }'''

    temperature_json = '''{
        "температуры": [
            {"id": "холодно", "points": [[0,1], [18,1], [22,0], [50,0]]},
            {"id": "комфортно", "points": [[18,0], [22,1], [24,1], [26,0]]},
            {"id": "жарко", "points": [[0,0], [24,0], [26,1], [50,1]]}
        ]
    }'''

    mapping_json = '''[
        ["холодно", "высокий"],
        ["комфортно", "средний"],
        ["жарко", "низкий"]
    ]'''

    main(regulator_json, temperature_json, mapping_json)
