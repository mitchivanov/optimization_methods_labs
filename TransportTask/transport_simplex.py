import numpy as np

from north_west_angle_method import north_west_angle_method
from output import print_bfs, print_cycle


def get_us_and_vs(bfs, costs):
    # выделим память под потенциалы
    us = [None] * len(costs)
    vs = [None] * len(costs[0])

    # первый потенциал u равен 0
    us[0] = 0

    # копируем допустимое базисное решение
    bfs_copy = bfs.copy()

    # пройдемся по базисному решению
    while len(bfs_copy) > 0:
        # index соответствует номеру элемента в базисном решении
        # bv соответствует индексам и значению в таблице
        for index, bv in enumerate(bfs_copy):
            # запомним индексы
            i, j = bv[0]
            # если потенцалам по данным индексам пустые, то ничего не делаем
            if us[i] is None and vs[j] is None: continue

            # запомним значение в таблице стоимостей
            cost = costs[i][j]
            # если не вычислили uᵢ
            if us[i] is None:
                # uᵢ = cᵢⱼ - vⱼ
                us[i] = cost - vs[j]
            # в обратном случае можем найти vⱼ
            else:
                # vⱼ = uᵢ - cᵢⱼ
                vs[j] = cost - us[i]
            bfs_copy.pop(index)
            break
    # возвращаем потенциалы поставищка и потребителя
    return us, vs


def get_ws(bfs, costs, us, vs):
    # вычислим параметр для свободных переменных
    ws = []
    # пройдемся по всем ячейкам стоимости
    for i, row in enumerate(costs):
        for j, cost in enumerate(row):
            # вычислим параметр wᵢⱼ для каждой неосновной переменной
            # wᵢⱼ, где индексы не входят в базовое допустимое решение
            non_basic = all([p[0] != i or p[1] != j for p, v in bfs])
            if non_basic:
                # wᵢⱼ = uᵢ + vⱼ - ciⱼ
                ws.append(((i, j), us[i] + vs[j] - cost))
    # возвращаем список хранящий индексы и значения параметра wᵢⱼ
    return ws


def can_be_improved(ws):
    for p, v in ws:
        # если хоть какое-то wᵢⱼ больше нуля, значит решение не оптимально и его можно улучшить
        if v > 0:
            return True
    return False


def get_entering_variable_position(ws):
    ws_copy = ws.copy()
    # отсортируем наши параметры wᵢⱼ по возрастанию значения
    ws_copy.sort(key=lambda w: w[1])
    # вернем максимальный по значению wᵢⱼ
    return ws_copy[-1][0]


def get_possible_next_nodes(cycle, not_visited):
    # возвращает возможные следующие узлы для данного цикла
    last_node = cycle[-1]
    # возможные узлы в строке (если их ещё не посещали и они стоят в той же строке, что и последний узел)
    nodes_in_row = [n for n in not_visited if n[0] == last_node[0]]
    # возможные узлы в колонках (если их ещё не посещали и они стоят в той же колонке, что и последний узел)
    nodes_in_column = [n for n in not_visited if n[1] == last_node[1]]


    if len(cycle) < 2: # если в цикле один узел добавляем оба в возможные направления пересчета
        return nodes_in_row + nodes_in_column
    else:
        prev_node = cycle[-2]
        row_move = prev_node[0] == last_node[0]
        # если мы уже двигались по строке
        if row_move:
            # то возвращаем возможные направления по колонке
            return nodes_in_column
        # если нет, то двигаемся по строке
        return nodes_in_row


def get_cycle(bv_positions, ev_position):
    def inner(cycle):
        if len(cycle) > 3:
            # если у цикла длина больше 3х, то проверяем, можем ли закрыть

            # если остается только одно возможное направление, то закрываем цикл
            can_be_closed = len(get_possible_next_nodes(cycle, [ev_position])) == 1
            if can_be_closed:
                # возвращаем цикл
                return cycle

        # выбираем все непосещенные ячейки из допустимого базисного решения
        not_visited = list(set(bv_positions) - set(cycle))
        # среди непосещенных найдем новое направление для продолжения цикла
        possible_next_nodes = get_possible_next_nodes(cycle, not_visited)

        # обход в глубину
        # строим цикл для каждого возможного нового направления
        for next_node in possible_next_nodes:
            # новый цикл созданный рекурсивно
            new_cycle = inner(cycle + [next_node])
            if new_cycle:
                return new_cycle

    return inner([ev_position])


def cycle_pivoting(bfs, cycle):
    # берем четные ячейки из цикла
    even_cells = cycle[0::2]
    # берем нечетные ячейки из цикла
    odd_cells = cycle[1::2]

    # найдем наименьшую нечетную ячейку, которая будет исключена из базиса
    get_bv = lambda pos: next(v for p, v in bfs if p == pos)
    leaving_position = sorted(odd_cells, key=get_bv)[0]
    leaving_value = get_bv(leaving_position)

    new_bfs = []
    # проходимся по всему базисному решению, кроме исключенной ячейки
    for p, v in [bv for bv in bfs if bv[0] != leaving_position] + [(cycle[0], 0)]:
        if p in even_cells:
            v += leaving_value
        elif p in odd_cells:
            v -= leaving_value
        # создаем новый базис на основе предыдущего,
        # без исключенной ячейки + параметр wᵢⱼ - начало цикла
        new_bfs.append((p, v))

    return new_bfs


def transportation_simplex_method(supply, demand, costs):

    def inner(bfs):

        # Выводим информацию о текущем базисном решении
        print("Текущее базисное решение:")
        print_bfs(bfs, len(costs), len(costs[0]))

        # вычислим потенциалы потребителя и поставщика для основных переменных -
        # путем ввода новых переменных u и v по соотнощениям:
        # u₁ = 0, uᵢ + vⱼ = cᵢⱼ
        us, vs = get_us_and_vs(bfs, costs)

        # Дополнительный вывод для иллюстрации
        print("Потенциалы потребителя (u):", us)
        print("Потенциалы поставщика (v):", vs)

        # для свободных переменных введем параметр w:
        # wᵢⱼ = uᵢ + vⱼ - cᵢⱼ
        ws = get_ws(bfs, costs, us, vs)

        # Выводим информацию о параметрах свободных переменных
        print("Параметры свободных переменных (w):", ws)

        # проверка на оптимальность
        # если wᵢⱼ ≤ 0, то базисное решение оптимально
        if can_be_improved(ws):
            # найдем ячейку, для которой будет максимально значение wᵢⱼ = uᵢ + vⱼ - cᵢⱼ
            ev_position = get_entering_variable_position(ws)

            # найдем цикл для заданного списка
            # с позициями основных переменных и позицией входящей переменной
            cycle = get_cycle([p for p, v in bfs], ev_position)
            print("Допустимое базисное решение:")
            print_bfs(bfs, len(costs), len(costs[0]))
            print("Цикл:")
            print_cycle(ev_position, cycle, bfs, len(costs), len(costs[0]))

            # рекурсивно улучшаем наше решение
            return inner(cycle_pivoting(bfs, cycle))

        print("Оптимальное решение:")
        print_bfs(bfs, len(costs), len(costs[0]))
        return bfs

    # находим начальное базисное решение методом северо-западного угла
    basic_feasible_sol = north_west_angle_method(supply, demand)
    print("Базис, полученный методом северо-западного угла:")
    print_bfs(basic_feasible_sol, len(costs), len(costs[0]))

    # решаем задачу методом потенциалов
    basic_variables = inner(basic_feasible_sol)

    solution = np.zeros((len(costs), len(costs[0])))
    for (i, j), v in basic_variables:
        solution[i][j] = v

    return solution