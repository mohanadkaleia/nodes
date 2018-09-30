#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
import sys
import copy
import argparse
import tabu_search as ts
from genetic_algorithm import City, TourManager, Tour, Population, GA


Point = namedtuple("Point", ['x', 'y'])


def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))


    # build a trivial solution
    # visit the nodes in the order they appear in the file
    # nodes = range(0, nodeCount)
    # iter = 70
    # size = 3
    # dict_of_neighbours = ts.generate_neighbours(points)
    # first_solution, distance_of_first_solution = ts.generate_first_solution(nodes, dict_of_neighbours)
    # solution, cost = ts.tabu_search(first_solution,
    #                                 distance_of_first_solution,
    #                                 dict_of_neighbours,
    #                                 iter,
    #                                 size,
    #                                 n_opt=1)
    pop_size = 1000
    tourmanager = TourManager()
    for index, point in enumerate(points):
        city = City(point[0], point[1], index)
        tourmanager.addCity(city)

    pop = Population(tourmanager, pop_size, True)
    print ("Initial distance: " + str(pop.getFittest().getDistance()))

    ga = GA(tourmanager)
    pop = ga.evolvePopulation(pop)
    for i in range(0, 1000):
        pop = ga.evolvePopulation(pop)

    # Print final results
    print ("Finished")
    print ("Final distance: " + str(pop.getFittest().getDistance()))
    print ("Solution:")
    print (pop.getFittest())

    solution = []
    for city in pop.getFittest():
        solution.append(city.index)

    # calculate the length of the tour
    obj = length(points[solution[-1]], points[solution[0]])
    for i in range(0, nodeCount-1):
        obj += length(points[solution[i]], points[solution[i+1]])

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')
