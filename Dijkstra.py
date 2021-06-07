import numpy as np


# import pandas as pd


# class Dijkstra calculate the shortest route between 2 points
class Dijkstra:

    def __init__(self, vertices=None, edges=None):
        """
        :param vertices: list of Location of each point
        :param edges:list of Connections between the points
        """
        self.__vertices = vertices
        self.__edged = edges

    def build_adj_matrix(self):
        # matrix size by point amount
        n_points = len(self.__vertices)
        matrix = np.zeros((n_points, n_points))
        for edg in self.__edged:
            # get points from index in edge list
            start = self.__vertices[edg[0]]
            end = self.__vertices[edg[1]]
            # add value of dist
            distance = ((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2) ** 0.5
            # store distance in matrix
            i = edg[0]
            j = edg[1]
            matrix[i, j] = distance
            matrix[j, i] = distance
        return matrix

    def find_shortest_route(self, start, end, matrix):
        """
        :param start: The point at the start of the route
        :param end: The point at the end of the route
        :param matrix: adj_matrix - the distance between each 2 adjacent points
        :return: Neighbors_points = []
        # Neighbors_points = []
        # i_black list [] = marker all the points we have already tested
        # di [] = a list which gives the distance of each point from the start point
        # pi [] = a list which gives for each point,Through which point you will get to the starting point,
        at the shortest way
        """

        beginning = start
        n_points = len(self.__vertices)
        i_black_list = np.zeros(n_points)

        # Initially all values​will be defined as infinity
        di = np.ones(n_points) * np.inf
        # Of course the distance of the point by itself is zero
        di[start] = 0

        # Initially all values​will be defined as -1
        pi = np.ones(n_points) * (-1)

        # A black list that starts at the starting point and goes through all the points to find the minimum way from
        # each point to the starting point The list starts with zeros, and each one passed through is worth 1 
        while i_black_list[start] == 0:
            i_black_list[start] = 1
            Neighbors_points = [0]
            Neighbors_points[0] = start
            Neighbors_points = []
            for h in range(len(matrix)):
                if matrix[start][h] != 0:
                    Neighbors_points.append(h)

            # For every neighbor, check to see if his route from the current step is shorter than it was before
            for j in range(len(Neighbors_points)):
                if di[start] + matrix[start][Neighbors_points[j]] < di[Neighbors_points[j]]:
                    di[Neighbors_points[j]] = matrix[start][Neighbors_points[j]] + di[start]

                    pi[Neighbors_points[j]] = start
                # else:
                #     if Neighbors_points[j]!= pi[Neighbors_points[j]]:
                #         di[Neighbors_points] = di[Neighbors_points] + matrix[start][Neighbors_points[j]]
            # Check what the next step will be - that is, what is the minimum in the set of di
            num_min = 1000000
            index_num_min = -1
            for dis in range(len(di)):
                if di[dis] < num_min and i_black_list[dis] == 0:
                    # That is to make sure you do not use a step that was already in place
                    num_min = di[dis]
                    index_num_min = dis
            start = index_num_min

        # Return the set of points that make up the route
        path_points = [end]
        while pi[end] != beginning:
            path_points.append(pi[end])
            end = int(pi[end])
        path_points.append(beginning)
        return path_points


if __name__ == '__main__':
    edges2 = [[9, 8], [9, 0], [9, 5], [0, 7], [7, 5], [7, 6], [5, 4], [6, 1], [3, 10], [1, 4], [1, 10], [3, 2], [10, 4],
              [2, 1], [8, 5]]
    vertices2 = [[199478.0635, 747506.5066],
                 [179101.272, 665999.3409],
                 [147999.8535, 601115.3471],
                 [179637.5034, 573231.3168],
                 [219854.8549, 634897.9224],
                 [230622.3805, 681983.3251],
                 [188012.1502, 692086.7818],
                 [198115.6068, 707241.9668],
                 [250829.2938, 765007.382],
                 [210415.4671, 768741.2682],
                 [211135.8875, 605855.9755]
                 ]
