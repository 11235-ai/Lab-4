class Item:
    def __init__(self, name, code, weight, value):
        self.name = name
        self.code = code
        self.weight = weight
        self.value = value


def knapsack(items, required, capacity):

    required_size = sum(item.weight for item in required)
    required_score = sum(item.value for item in required)
    capacity = capacity - required_size

    items = [item for item in items if item not in required]
    items = sorted(items, key=lambda x: x.value / x.weight, reverse=True)

    def Election_procc(i, weight, value):
        if weight > capacity:
            return 0

        node_value = value
        t_weight = weight
        j = i

        while j < len(items) and t_weight + items[j].weight <= capacity:
            node_value += items[j].value
            t_weight += items[j].weight
            j += 1

        if j < len(items):
            node_value += (capacity - t_weight) * (items[j].value / items[j].weight)

        return node_value

    def branch_bound(i, weight, value):
        nonlocal max_value, best_combination

        if weight <= capacity and value > max_value:
            max_value = value
            best_combination = current_combination[:]

        if i == len(items):
            return

        if Election_procc(i, weight, value) > max_value:
            branch_bound(i + 1, weight, value)

        if weight + items[i].weight <= capacity:
            current_combination.append(items[i])
            branch_bound(i + 1, weight + items[i].weight, value + items[i].value)
            current_combination.pop()

    max_value = required_score
    best_combination = []
    current_combination = []

    branch_bound(0, 0, 0)

    final_items = required + best_combination
    return final_items, max_value


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

    initial_survival_points = 10  # 10 очков выживания Тома

    final_items, max_score = knapsack(items, required, inventory_size)

    selected_items = set(final_items)
    unused_items = [item for item in items if item not in selected_items]
    unused_score = sum(item.value for item in unused_items)

    grouped_result = []
    current_row = []
    current_row_weight = 0

    for item in final_items:
        for _ in range(item.weight):
            if current_row_weight + 1 > 4:
                grouped_result.append(current_row)
                current_row = []
                current_row_weight = 0
            current_row.append(f'[{item.code}]')
            current_row_weight += 1

    if current_row:
        grouped_result.append(current_row)

    for row in grouped_result:
        print(", ".join(row))

    print()
    final_score = max(max_score - unused_score, 0) + initial_survival_points
    print(f"Общие очки выживания: {max_score}")
    print(f"Итоговые очки выживания: {final_score}")
