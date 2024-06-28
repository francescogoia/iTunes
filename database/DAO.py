from database.DB_connect import DBConnect
from model.album import Album


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllAlbum():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        select a.AlbumId , a.Title , a.ArtistId , sum(t.Milliseconds) as Durata
        from album a , track t 
        where a.AlbumId = t.AlbumId 
        group  by a.AlbumId 
        """
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(Album(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(idMap):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        select distinctrow  t1.AlbumId as a1, t2.AlbumId as a2
        from playlisttrack p1, playlisttrack p2 , track t1, track t2
        where p1.TrackId = t1.TrackId and p2.TrackId = t2.TrackId
            and p1.PlaylistId = p2.PlaylistId and t2.AlbumId > t1.AlbumId"""
        cursor.execute(query)
        result = []
        for row in cursor:
            if row["a1"] in idMap and row["a2"] in idMap:
                result.append((idMap[row["a1"]], idMap[row["a2"]]))
        cursor.close()
        conn.close()
        return result
