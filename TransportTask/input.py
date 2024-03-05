def read_input_data(filename: str):
    """
    Считывание входных данных из файла.

    :param filename: Имя файла с входными данными.
    :return: Кортеж с данными транспортной задачи.
    """
    try:
        with open(filename, 'r') as fp:
            # Считываем предложения
            supply_list = list(map(int, fp.readline().split()))
            # Считываем спрос
            demand_list = list(map(int, fp.readline().split()))

            # Считываем матрицу стоимостей перевозок
            costs_matrix = [list(map(int, line.split())) for line in fp if not (line.startswith('N') or line.startswith('Y'))]

            # Инициализируем штрафы для избытка спроса и предложения
            penalties_for_more_demand = [0] * len(demand_list)
            penalties_for_more_supply = [0] * len(supply_list)

            # Проверяем наличие штрафов и считываем их, если они есть
            if fp.readline().strip() == "Y":
                penalties_for_more_demand = list(map(int, fp.readline().split()))
                penalties_for_more_supply = list(map(int, fp.readline().split()))

        return supply_list, demand_list, costs_matrix, penalties_for_more_demand, penalties_for_more_supply

    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return [], [], [], [], []
