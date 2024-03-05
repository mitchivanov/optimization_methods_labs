from output import print_transportation_problem


def make_closed_tp(supply, demand, costs, penalties_for_more_demand, penalties_for_more_supply):
    """
    Приведение транспортной задачи к закрытому виду.

    :param supply: Вектор предложений.
    :param demand: Вектор спроса.
    :param costs: Матрица стоимости перевозок.
    :param penalties_for_more_demand: Штрафы за неудовлетворение спроса.
    :param penalties_for_more_supply: Штрафы за непокрытие предложения.
    :return: Кортеж с закрытым видом транспортной задачи.
    """

    print("Приведение задачи к закрытому виду...")

    # Общее предложение и спрос
    total_supply = sum(supply)
    total_demand = sum(demand)

    print("Всего предложения:")
    print(total_supply)
    print("Всего спроса:")
    print(total_demand)

    # Если спрос больше предложения, вводим штрафы за неудовлетворение спроса
    if total_supply < total_demand:
        print("Спрос больше предложения, закрытая задача будет иметь вид:")
        new_supply = supply + [total_demand - total_supply]
        new_costs = costs + [penalties_for_more_demand]
        print_problem(new_supply, demand, new_costs)
        return new_supply, demand, new_costs

    # Если предложение больше спроса, вводим штрафы за непокрытие предложения
    if total_supply > total_demand:
        print("Предложение больше спроса, закрытая задача будет иметь вид:")
        new_demand = demand + [total_supply - total_demand]
        new_costs = costs
        for i in range(len(new_costs)):
            new_costs[i].append(penalties_for_more_supply[i])

        print_problem(supply, new_demand, new_costs)
        return supply, new_demand, new_costs

    # Если спрос равен предложению, исходная задача имеет закрытый вид
    print("Спрос равен предложению, исходная задача имеет закрытый вид \n")
    return supply, demand, costs
