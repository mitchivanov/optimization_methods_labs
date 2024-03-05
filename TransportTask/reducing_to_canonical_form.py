def reduce_to_canonical_form(M: int, N: int, supply: list, demand: list, costs: list):
    """
    Приведение транспортной задачи к каноническому виду.

    :param M: Количество предложений (поставщиков).
    :param N: Количество спроса (потребителей).
    :param supply: Список предложений от поставщиков.
    :param demand: Список спроса от потребителей.
    :param costs: Матрица стоимостей перевозок.
    :return: Кортеж минимальной задачи, матрицы и вектора ограничений.
    """

    min_task = []

    for i in range(M):
        for j in range(N):
            min_task.append(int(costs[i][j]))

    b_vector = [supply[i] if i < M else demand[i - M] for i in range(M + N)]
    A_matrix = [[0 for _ in range(M * N)] for _ in range(M + N)]

    # Заполняем строки-ограничения на поставку
    for i in range(M):
        for j in range(N):
            A_matrix[i][i * N + j] = 1

    # Заполняем строки-ограничения на прием
    for i in range(N):
        for j in range(M):
            A_matrix[M + i][i + j * N] = 1

    return min_task, A_matrix, b_vector
