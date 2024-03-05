import numpy as np
from reducing_to_canonical_form import reduce_to_canonical_form
from reducing_to_closed_form import make_closed_tp
from input import read_input_data
from output import print_solution, print_transportation_problem
from transport_simplex import transportation_simplex_method

def main():
    # Считываем входные данные из файла
    supply, demand, costs, penalties_for_more_demand, penalties_for_more_supply = read_input_data("input.txt")

    if not supply or not demand or not costs:
        # Обработка случая ошибки при чтении данных
        print("Ошибка при считывании входных данных. Проверьте формат файла.")
        return

    print("Исходная транспортная задача:")
    print_transportation_problem(supply, demand, costs)

    # Приводим задачу в закрытую форму
    closed_supply, closed_demand, closed_costs = make_closed_tp(supply, demand, costs,
                                                                penalties_for_more_demand,
                                                                penalties_for_more_supply)

    # Решаем транспортную задачу методом симплекса
    solution = transportation_simplex_method(closed_supply, closed_demand, closed_costs)

    # Выводим результат
    print_solution(costs, solution)

if __name__ == "__main__":
    main()
