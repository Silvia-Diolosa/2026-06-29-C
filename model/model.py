import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self.idMap = {}
        self._bestPath = []
        self._bestScore = 0



    def buildGraph(self):
        self._graph.clear()
        self.idMap.clear()

        nodes = DAO.getAllNodes()
        for node in nodes:
            self.idMap[node.ArtistId] = node
        self._graph.add_nodes_from(nodes)

        info = DAO.getArtistInfo()
        for i in info:
            artista = self.idMap[i[0]]
            numBrani = i[1]
            numPlaylist = i[2]
            artista.numBrani = numBrani
            artista.numPlaylist = numPlaylist

        edges = DAO.getAllEdges()
        for edge in edges:
            u = self.idMap[edge[0]]
            v = self.idMap[edge[1]]
            self._graph.add_edge(u, v, weight=edge[2])


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getNodes(self):
        return list(self._graph.nodes)
    def getEdges(self):
        return list(self._graph.edges(data=True))
    def getNumNodi(self):
        return len(self._graph.nodes)
    def getNumEdges(self):
        return len(self._graph.edges)


    def getInfo1(self):
        lista = []
        for node in self._graph.nodes:
            grado = self._graph.degree(node)
            lista.append((node, grado))

        lista.sort(key=lambda x: x[1], reverse=True)

        return lista[0]


    def getInfo2(self):
        lista = []
        for node in self._graph.nodes:
            somma = 0
            for edge in self._graph.edges(node, data=True):
                somma += edge[2]["weight"]
            lista.append((node, somma))
        lista.sort(key=lambda x: x[1], reverse=True)
        return lista[0]


    def getInfo3(self):
        lista = []
        for edge in self.getEdges():
            if edge[0].Name <= edge[1].Name:
                lista.append((edge[0], edge[1], edge[2]["weight"]))
            else:
                lista.append((edge[1], edge[0], edge[2]["weight"]))

        lista.sort(key=lambda x: (-x[2], x[0].Name, x[1].Name))

        return lista[0:10]



    def getBestPath(self, partenza, n):
        self._bestPath = []
        self._bestScore = 0
        parziale = [partenza]

        self.ricorsione(parziale, n)

        return self._bestPath, self._bestScore


    def ricorsione(self, parziale, n):
        if len(parziale) == n:
            score = self._calcolaScore(parziale)
            if score > self._bestScore:
                self._bestScore = score
                self._bestPath = copy.deepcopy(parziale)
            return

        # caso ricorsivo
        for nodo in parziale:
            for vicino in self._graph.neighbors(nodo):
                if vicino not in parziale and self.condizione(parziale, vicino):
                    parziale.append(vicino)
                    self.ricorsione(parziale, n)
                    parziale.pop()


    def _calcolaScore(self, parziale):
        score = 0
        for nodo in parziale:
            score += nodo.numBrani
        return score

    def condizione(self, parziale, nodo):
        for vicino in self._graph.neighbors(nodo):  # per ogni vicino del nodo che vogliamo aggiungere
            if vicino in parziale:  # se questo vicino è in parziale
                peso = self._graph[nodo][vicino]["weight"]  # l'arco che fanno non può pesare 1
                if peso == 1:
                    return False

        return True


