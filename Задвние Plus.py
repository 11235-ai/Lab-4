class Item:
    def __init__(self, name, code, weight, value):
        self.name = name
        self.code = code
        self.weight = weight
        self.value = value


def knapsack(items, required, capacity):
    required_size = sum(item.weight for item in required)
    required_score = sum(item.value for item in required)
    available_capacity = capacity - required_size

    items = [item for item in items if item not in required]
    items = sorted(items, key=lambda x: x.value / x.weight, reverse=True)

    def Election_procc(i, weight, value):
        if weight > available_capacity:
            return 0

        node_value = value
        total_weight = weight
        j = i

        while j < len(items) and total_weight + items[j].weight <= available_capacity:
            node_value += items[j].value
            total_weight += items[j].weight
            j += 1

        if j < len(items):
            node_value += (available_capacity - total_weight) * (items[j].value / items[j].weight)

        return node_value

    def branch_bound(i, weight, value):
        nonlocal max_value, best_combination, unique_combinations

        if weight <= available_capacity and value > max_value:
            max_value = value
            best_combination = current_combination[:]
            unique_combinations.add(tuple(sorted(current_combination, key=lambda x: x.code)))

        if i == len(items):
            return

        if Election_procc(i, weight, value) > max_value:
            branch_bound(i + 1, weight, value)

        if weight + items[i].weight <= available_capacity:
            current_combination.append(items[i])
            branch_bound(i + 1, weight + items[i].weight, value + items[i].value)
            current_combination.pop()

    max_value = required_score
    best_combination = []
    current_combination = []
    unique_combinations = set()

    branch_bound(0, 0, 0)

    final_items = required + best_combination
    return final_items, max_value, unique_combinations


def display_inventory(items, row_capacity=4, exact_slots=None):
    grouped_result = []
    current_row = []
    current_row_weight = 0

    for item in items:
        for _ in range(item.weight):
            if current_row_weight + 1 > row_capacity:
                grouped_result.append(current_row)
                current_row = []
                current_row_weight = 0
            current_row.append(f'[{item.code}]')
            current_row_weight += 1

    if current_row:
        grouped_result.append(current_row)

    if exact_slots and sum(len(row) for row in grouped_result) != exact_slots:
        return None

    return grouped_result

if __name__ == '__main__':
    items = [
        Item("Винтовка", 'r', 3, 25), Item("Пистолет", "p", 2, 15),
        Item("Боекомплект", "a", 2, 15), Item("Аптечка", 'm', 2, 20), 
        Item("Ингалятор", "i", 1, 5), Item("Нож", "k", 1, 15),
        Item("Топор", "x", 3, 20), Item("Оберег", "t", 1, 25),
        Item("Фляжка", "f", 1, 15), Item("Антидот", "d", 1, 10),
        Item("Еда", "s", 2, 20), Item("Арбалет", "c", 2, 20)
    ]

    required = [Item("Антидот", "d", 1, 10)]
    inventory_size = 8
    initial_survival_points = 10
    total_score = sum(item.value for item in items)
    final_items, max_score, unique_combinations = knapsack(items, required, inventory_size)

    print("Комбинации:")
    for combo in unique_combinations:
        selected_items = required + list(combo)

        combo_score = sum(item.value for item in selected_items)
        unused_items = [item for item in items if item not in selected_items]
        unused_score = sum(item.value for item in unused_items)
        adjusted_score = combo_score - unused_score + initial_survival_points

        if adjusted_score > 0:
            formatted_result = display_inventory(selected_items, row_capacity=4, exact_slots=8)
            if formatted_result:
                for row in formatted_result:
                    print(", ".join(row))
                print(f"Общие очки выживания: {combo_score}")
                print(f"Итоговые очки выживания: {adjusted_score}\n")

  
    print("Комбинации с 7 ящиками:")
    for combo in unique_combinations:
        selected_items = required + list(combo)

        total_weight = sum(item.weight for item in selected_items)
        if total_weight == 7:
            combo_score = sum(item.value for item in selected_items)
            unused_items = [item for item in items if item not in selected_items]
            unused_score = sum(item.value for item in unused_items)
            adjusted_score = combo_score - unused_score + initial_survival_points

            if adjusted_score > 0:
                formatted_result = display_inventory(selected_items, row_capacity=4, exact_slots=7)
                if formatted_result:
                    for row in formatted_result:
                        print(", ".join(row))
                    print(f"Общие очки выживания: {combo_score}")
                    print(f"Итоговые очки выживания: {adjusted_score}\n")
            else:
                    print("Не существует комбинаций с 7 ящиками, которые имеют положительную скорректированную оценку.")
