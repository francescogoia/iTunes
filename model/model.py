import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}

    def buildGraph(self, durata):
        durata_milliSec = 60*1000*durata         # duarata in millisecondi
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
        totMinutes = totD / (1000*60)
        return len(conn), totMinutes

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getNodes(self):
        return list(self._grafo.nodes)
