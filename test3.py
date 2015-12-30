import igraph as ig
import pandas as pd
import numpy as np
import multiprocessing as mp
import time
from Data import Data
from DataHandler import DataHandler
import csv


def get_csv(path):
        """
        recuperation du csv
        a modifier selon la methode choisie pour recuperer les donnees
        :param path: Path of the CSV
        :return: None
        """
        row_table = np.genfromtxt(path, delimiter=';')

        return row_table

if __name__ == '__main__':

    t = time.time()

    with open("C:\Users\Administrateur\Documents\PRODUITS_VISITES.csv", 'rb') as f:
        reader = csv.reader(f, delimiter=";")
        edges = list(reader)

    # collect the set of vertex names and then sort them into a list
    vertices = set()
    for line in edges:
        vertices.update(line)
    vertices = sorted(vertices)

    # create an empty graph
    g = ig.Graph(directed=False)

    # add vertices to the graph
    g.add_vertices(vertices)

    # add edges to the graph
    g.add_edges(edges)

    # set the weight of every edge to 1
    g.es["weight"] = 1

    # collapse multiple edges and sum their weights
    g.simplify(combine_edges={"weight": "sum"})

    ig.plot(g)

    print time.time() - t



