import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}

    def buildGraph(self, durata):
        durata = durata * 60 * 1000
        allAlbums = DAO.getAllAlbum()
        for a in allAlbums:
            if a.Durata > durata:
                self._grafo.add_node(a)
                self._idMap[a.AlbumId] = a
        archi = DAO.getAllEdges(self._idMap)
        self._grafo.add_edges_from(archi)

    def getConnessaDetails(self, album):
        connessa = nx.node_connected_component(self._grafo, album)
        durataTot = 0
        for a in connessa:
            durataTot += a.Durata
        return len(connessa), durataTot/(60*1000)

    def get_set_album(self, album, dTot):
        dTot = dTot * 60 * 1000
        connessa = nx.node_connected_component(self._grafo, album)
        self._bestSol = 0
        self._bestSet = set()
        parziale = set()
        parziale.add(album)
        self._ricorsione(connessa, parziale, dTot)
        return self._bestSet

    def _ricorsione(self, connessa, parziale, dTot):
        durata_parziale = self._durata(parziale)
        if durata_parziale > dTot:
            return
        if len(parziale) > self._bestSol:
            self._bestSet = copy.deepcopy(parziale)
            self._bestSol = len(parziale)
        for v in connessa:
            if v not in parziale:
                parziale.add(v)
                self._ricorsione(connessa, parziale, dTot)
                parziale.remove(v)

    def _durata(self, parziale):
        tot = 0
        for a in parziale:
            tot += a.Durata
        return tot

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getNodes(self):
        nodi = list(self._grafo.nodes)
        nodi.sort(key=lambda x: x.Title)
        return nodi
