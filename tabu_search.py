"""
This implementation for tabu search is modified from:
https://www.techconductor.com/algorithms/python/Search/Tabu_Search.php

Reference:
https://www.researchgate.net/publication/242527226_Tabu_Search_A_Tutorial
"""
import copy
import math


def distance(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)


def generate_neighbours(points):
    """This function geenrates a 2D distance matrix between all points

    Parameters
    ----------
    points : type
        Description of parameter `points`.

    Returns
    -------
    type
        Description of returned object.

    """
    dict_of_neighbours = {}

    for i in range(len(points)):
        for j in range(i+1, len(points)):
            if i not in dict_of_neighbours:
                _list = list()
                _list.append([j, distance(points[i], points[j])])
                dict_of_neighbours[i] = _list
            else:
                dict_of_neighbours[i].append([j, distance(points[i], points[j])])
            if j not in dict_of_neighbours:
                _list = list()
                _list.append([i, distance(points[j], points[i])])
                dict_of_neighbours[j] = _list
            else:
                dict_of_neighbours[j].append([i, distance(points[j], points[i])])
    return dict_of_neighbours


def generate_first_solution(nodes, dict_of_neighbours):
    start_node = nodes[0]
    end_node = start_node

    first_solution = []

    visiting = start_node

    distance_of_first_solution = 0
    while visiting not in first_solution:
        minim = 1000000
        for k in dict_of_neighbours[visiting]:
            if k[1] < minim and k[0] not in first_solution:
                minim = k[1]
                best_node = k[0]

        first_solution.append(visiting)
        distance_of_first_solution = distance_of_first_solution + minim
        visiting = best_node

    first_solution.append(end_node)
    position = 0
    for k in dict_of_neighbours[first_solution[-2]]:
        if k[0] == start_node:
            break
        position += 1

    distance_of_first_solution = distance_of_first_solution + dict_of_neighbours[first_solution[-2]][position][1] - minim
    return first_solution, distance_of_first_solution


def find_neighborhood(solution, dict_of_neighbours):
    neighborhood_of_solution = []
    for n in solution[1:-1]:
        idx1 = solution.index(n)
        for kn in solution[1:-1]:
            idx2 = solution.index(kn)
            if n == kn:
                continue

            _tmp = copy.deepcopy(solution)
            _tmp[idx1] = kn
            _tmp[idx2] = n

            distance = 0
            for k in _tmp[:-1]:
                next_node = _tmp[_tmp.index(k) + 1]
                for i in dict_of_neighbours[k]:
                    if i[0] == next_node:
                        # print("{0} -> {1}: {2}".format(k, next_node, i[1]))
                        distance = distance + i[1]
            _tmp.append(distance)
            if _tmp not in neighborhood_of_solution:
                neighborhood_of_solution.append(_tmp)

    indexOfLastItemInTheList = len(neighborhood_of_solution[0]) - 1

    neighborhood_of_solution.sort(key=lambda x: x[indexOfLastItemInTheList])
    return neighborhood_of_solution


def tabu_search(first_solution, distance_of_first_solution, dict_of_neighbours, iters, size):
    count = 1
    solution = first_solution
    tabu_list = list()
    best_cost = distance_of_first_solution
    best_solution_ever = solution
    while count <= iters:
        neighborhood = find_neighborhood(solution, dict_of_neighbours)
        index_of_best_solution = 0
        best_solution = neighborhood[index_of_best_solution]
        best_cost_index = len(best_solution) - 1
        found = False
        while found is False:
            i = 0
            while i < len(best_solution):

                if best_solution[i] != solution[i]:
                    first_exchange_node = best_solution[i]
                    second_exchange_node = solution[i]
                    break
                i = i + 1

            if [first_exchange_node, second_exchange_node] not in tabu_list and [second_exchange_node,
                                                                                 first_exchange_node] not in tabu_list:
                tabu_list.append([first_exchange_node, second_exchange_node])
                found = True
                solution = best_solution[:-1]
                cost = neighborhood[index_of_best_solution][best_cost_index]
                if cost < best_cost:
                    best_cost = cost
                    best_solution_ever = solution
            elif index_of_best_solution < len(neighborhood):
                best_solution = neighborhood[index_of_best_solution]
                index_of_best_solution = index_of_best_solution + 1
            # else:
            #     break

        while len(tabu_list) > size:
            tabu_list.pop(0)

        count = count + 1
        print(best_cost)
    best_solution_ever.pop(-1)
    return best_solution_ever, best_cost
