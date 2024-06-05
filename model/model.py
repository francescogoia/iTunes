import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._bestScore = None
        self._bestSet = None
        self._grafo = nx.Graph()
        self._idMap = {}

    def get_set_album(self, a1, dTot):
        self._bestSet = None
        self._bestScore = 0
        connessa = nx.node_connected_component(self._grafo, a1)
        parziale = set()
        parziale.add(a1)
        connessa.remove(a1)
        self._ricorsione(parziale, connessa, dTot)

        return self._bestSet

    def _ricorsione(self, parziale, connessa, dTot):
        # verificare se parziale è una sol ammissibile
        if self.durataTot(parziale) > dTot:
            return
        # verificare se parziale è migliore del best
        if len(parziale) > self._bestScore:
            self._bestSet = len(parziale)
            self._bestSet = copy.deepcopy(parziale)

        # ciclo su nodi aggiungibili --> ricorsione
        for c in connessa:
            if c not in parziale:

                parziale.add(c)
                self._ricorsione(parziale, connessa, dTot)
                parziale.remove(c)

    def durataTot(self, listOfNodes):
        dTot = 0
        for n in listOfNodes:
            dTot += n.totD
        return dTot / (60*1000)

    def buildGraph(self, durata):
        durata_milliSec = 60 * 1000 * durata  # duarata in millisecondi
        self._grafo.clear()
        self._grafo.add_nodes_from(DAO.getAlbums(durata_milliSec))
        self._idMap = {a.AlbumId: a for a in list(self._grafo.nodes)}
        edges = DAO.getEdges(self._idMap)
        self._grafo.add_edges_from(edges)

    def getConnessaDetails(self, v0):
        conn = nx.node_connected_component(self._grafo, v0)
        totD = 0
        for album in conn:
            totD += album.totD
        totMinutes = totD / (1000 * 60)
        return len(conn), totMinutes

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getNodes(self):
        return list(self._grafo.nodes)

    def getNodeI(self, i):
        return list(self._grafo.nodes)[i]
