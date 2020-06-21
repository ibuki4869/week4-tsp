import pandas as pd
import numpy as np
import sys
import time


def calculate_total_distance(order, distance_matrix):
    """Calculate total distance traveled for given visit order"""
    idx_from = np.array(order)
    idx_to = np.array(order[1:] + [order[0]])
    distance_arr = distance_matrix[idx_from, idx_to]

    return np.sum(distance_arr)


def calculate_2opt_exchange_cost(visit_order, i, j, distance_matrix):
    """Calculate the difference of cost by applying given 2-opt exchange"""
    n_cities = len(visit_order)
    a, b = visit_order[i], visit_order[(i + 1) % n_cities]
    c, d = visit_order[j], visit_order[(j + 1) % n_cities]

    cost_before = distance_matrix[a, b] + distance_matrix[c, d]
    cost_after = distance_matrix[a, c] + distance_matrix[b, d]
    return cost_after - cost_before


def apply_2opt_exchange(visit_order, i, j):
    """Apply 2-opt exhanging on visit order"""

    tmp = visit_order[i + 1: j + 1]
    tmp.reverse()
    visit_order[i + 1: j + 1] = tmp

    return visit_order


def improve_with_2opt(visit_order, distance_matrix):
    """Check all 2-opt neighbors and improve the visit order"""
    n_cities = len(visit_order)
    cost_diff_best = 0.0
    i_best, j_best = None, None

    for i in range(0, n_cities - 2):
        if i > 513:
            break
        for j in range(i + 2, n_cities):
            if j > 513:
                break
            if i == 0 and j == n_cities - 1:
                continue

            cost_diff = calculate_2opt_exchange_cost(
                visit_order, i, j, distance_matrix)

            if cost_diff < cost_diff_best:
                cost_diff_best = cost_diff
                i_best, j_best = i, j

    if cost_diff_best < 0.0:
        visit_order_new = apply_2opt_exchange(visit_order, i_best, j_best)
        return visit_order_new
    else:
        return None


def local_search(visit_order, distance_matrix, improve_func):
    """Main procedure of local search"""
    cost_total = calculate_total_distance(visit_order, distance_matrix)
    i = 0
    while True:
        improved = improve_func(visit_order, distance_matrix)
        if not improved:
            break
        if i > 1000:
            break
        i += 1

        visit_order = improved

    return visit_order


def solve(df_dist):
    N = len(df_dist)

    dist = df_dist.values.tolist()

    current_city = 0
    unvisited_cities = set(range(1, N))
    solution = [current_city]

    def distance_from_current_city(to):
        return dist[current_city][to]

    while unvisited_cities:
        next_city = min(unvisited_cities, key=distance_from_current_city)
        unvisited_cities.remove(next_city)
        solution.append(next_city)
        current_city = next_city
    return solution


def multi_start(N_START, infile, outfile):
    df = pd.read_csv(infile)
    df_x = pd.DataFrame()
    df_y = pd.DataFrame()
    df_x = df_x.append([df['x']]*len(df), ignore_index=True)
    df_y = df_y.append([df['y']]*len(df), ignore_index=True)
    df_xt = df_x.T
    df_yt = df_y.T
    df_dist = (df_x-df_xt)**2+(df_y-df_yt)**2
    df_dist = np.sqrt(df_dist)
    distance_matrix = df_dist.values
    N = len(df)
    order_best = None
    score_best = sys.float_info.max
    order_random = solve(df_dist)
    for i in range(N_START):
        order_improved = local_search(
            order_random, distance_matrix, improve_with_2opt)
        score = calculate_total_distance(order_improved, distance_matrix)

        if score < score_best:
            score_best = score
            order_best = order_improved
        if i > N:
            order_random = list(np.random.permutation(N))

    with open(outfile, 'w') as f:
        f.write('index'+'\n')
        for ans in order_best:
            f.write(str(ans)+'\n')


if __name__ == '__main__':
    start = time.time()
    print('0')
    multi_start(200, 'input_0.csv', 'solution_yours_0.csv')
    print('1')
    multi_start(200, 'input_1.csv', 'solution_yours_1.csv')
    print('2')
    multi_start(200, 'input_2.csv', 'solution_yours_2.csv')
    print('3')
    multi_start(200, 'input_3.csv', 'solution_yours_3.csv')
    print('4')
    multi_start(200, 'input_4.csv', 'solution_yours_4.csv')
    print('5')
    multi_start(200, 'input_5.csv', 'solution_yours_5.csv')
    print('6')
    multi_start(200, 'input_6.csv', 'solution_yours_6.csv')
    elapsed_time = time.time() - start
    print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
