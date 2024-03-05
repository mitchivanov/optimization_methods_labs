def print_transportation_problem(supply, demand, costs):
    """
    Выводит на экран данные транспортной задачи.

    :param supply: Список предложений от поставщиков.
    :param demand: Список спроса от потребителей.
    :param costs: Матрица стоимостей перевозок.
    """
    print("Предложение:")
    print(supply)
    print("Спрос:")
    print(demand)
    print("Стоимость перевозок:")
    for row in costs:
        print(row)
    print()


def print_cycle(start_pos, cycle, bfs, len_col, len_row):
    """
    Выводит информацию о цикле в таблице.

    :param start_pos: Начальная позиция цикла.
    :param cycle: Список координат цикла.
    :param bfs: Список базисных переменных.
    :param len_col: Количество столбцов в таблице.
    :param len_row: Количество строк в таблице.
    """
    cycle_table = [['0' for j in range(len_row)] for i in range(len_col)]
    ctr = 1
    cycle_table[start_pos[0]][start_pos[1]] = "*_0"

    for (i, j), v in bfs:
        if (i, j) in cycle:
            cycle_table[i][j] = f"{v}_{ctr}"
            if ctr == 1:
                ctr = len(cycle) - 1
            else:
                ctr -= 1

    for row in cycle_table:
        print(row)
    print()


def print_bfs(bfs, len_col, len_row):
    """
    Выводит информацию о базисных переменных в таблице.

    :param bfs: Список базисных переменных.
    :param len_col: Количество столбцов в таблице.
    :param len_row: Количество строк в таблице.
    """
    bfs_table = [['0' for j in range(len_row)] for i in range(len_col)]

    for (i, j), v in bfs:
        bfs_table[i][j] = f"{v}_b"

    for row in bfs_table:
        print(row)


def print_solution(costs, solution):
    """
    Выводит информацию о найденном оптимальном решении.

    :param costs: Матрица стоимостей перевозок.
    :param solution: Матрица оптимального решения.
    :return: Итоговая минимальная стоимость.
    """
    print()
    total_cost = 0

    for i, row in enumerate(costs):
        for j, cost in enumerate(row):
            if solution[i][j] != 0:
                print(f"Из {i + 1}-го склада нужно доставить в {j + 1}-й магазин "
                      f"{solution[i][j]} ед. товара, стоимость: {cost * solution[i][j]}")
                total_cost += cost * solution[i][j]

    print(f"Итого, минимальные затраты составят: {total_cost}")
    return total_cost
