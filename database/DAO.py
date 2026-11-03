from database.DB_connect import DBConnect
from model.artist import Artist


class DAO():

    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct c.Country
                from customer c
                where c.Country is not null
                order by c.Country
                """

        cursor.execute(query)

        for row in cursor:
            results.append(row["Country"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT a.*
FROM artist a, album ab, track t
WHERE a.ArtistId = ab.ArtistId
AND ab.AlbumId = t.AlbumId
ORDER BY a.Name"""

        cursor.execute(query)

        for row in cursor:
            results.append(Artist(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT t1.ArtistId as id1, t2.ArtistId as id2, COUNT(*) as peso
FROM
(SELECT DISTINCT a.ArtistId, p.PlaylistId
FROM artist a, album ab, track t, playlisttrack p
WHERE a.ArtistId = ab.ArtistId
AND ab.AlbumId = t.AlbumId
AND t.TrackId = p.TrackId) t1, 
(SELECT DISTINCT a.ArtistId, p.PlaylistId
FROM artist a, album ab, track t, playlisttrack p
WHERE a.ArtistId = ab.ArtistId
AND ab.AlbumId = t.AlbumId
AND t.TrackId = p.TrackId) t2
WHERE t1.ArtistId < t2.ArtistId
AND t1.PlaylistId = t2.PlaylistId
GROUP BY t1.ArtistId, t2.ArtistId
"""

        cursor.execute(query)

        for row in cursor:
            results.append((row["id1"], row["id2"], row["peso"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getArtistInfo():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT a.ArtistId as id , COUNT(DISTINCT t.TrackId) as numBrani, COUNT(DISTINCT p.PlaylistId) as numPlaylist
FROM artist a, album ab, track t, playlisttrack p
WHERE a.ArtistId = ab.ArtistId
AND ab.AlbumId = t.AlbumId
AND t.TrackId = p.TrackId
GROUP BY a.ArtistId
    """

        cursor.execute(query)

        for row in cursor:
            results.append((row["id"], row["numBrani"], row["numPlaylist"]))

        cursor.close()
        conn.close()
        return results



