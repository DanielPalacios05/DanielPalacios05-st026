import sqlite3
from concurrent import futures
import grpc
import peers_pb2
import peers_pb2_grpc

# Create a SQLite database and a table for peers and linked peers
conn = sqlite3.connect('peers.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS peers
                     (host text, port integer, is_linked integer)''')

class Peers(peers_pb2_grpc.PeersServicer):
    def AddPeer(self, request, context):
        # Create a new SQLite connection for each request
        conn = sqlite3.connect('peers.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS peers
(host text, port integer, is_linked integer);
                  
                  CREATE TABLE IF NOT EXISTS files
(host text, port integer, filepath text, filename text);''')

        # Add the peer to the database
        c.execute("INSERT INTO peers VALUES (?,?,?)", (request.peer.host, request.peer.port, request.linkPeer))
        conn.commit()
        conn.close()
        return peers_pb2.PeerLinkResponse(added=True)
    
    def ListPeers(self, request, context):
        # Create a new SQLite connection for each request
        conn = sqlite3.connect('peers.db')
        c = conn.cursor()

        # Query all peers from the database
        if request.linkedPeers:
            c.execute("SELECT * FROM peers WHERE is_linked = 1")
        else:
            c.execute("SELECT * FROM peers")
        peers = c.fetchall()

        # Convert the result to PeerListResponse
        response = peers_pb2.PeerListResponse()
        for peer in peers:
            peer_link_request = peers_pb2.PeerLinkRequest(peer=peers_pb2.Peer(host=peer[0], port=peer[1]), linkPeer=bool(peer[2]))
            response.peerEntry.append(peer_link_request)


        conn.close()
        return response
    

    def AddPeerWithFiles(self, request, context):
        # Create a new SQLite connection for each request
        conn = sqlite3.connect('peers.db')
        c = conn.cursor()

        # Check if the peer already exists
        c.execute("SELECT * FROM peers WHERE host = ? AND port = ?", (request.peer.host, request.peer.port))
        result = c.fetchone()

        if result is None:
            # If the peer does not exist, add the peer to the database
            c.execute("INSERT INTO peers VALUES (?,?,?)", (request.peer.host, request.peer.port, True))
        else:
            # If the peer exists, delete all existing files associated with the peer
            c.execute("DELETE FROM files WHERE host = ? AND port = ?", (request.peer.host, request.peer.port))

        # Add the files to the database
        for file in request.files:
            c.execute("INSERT INTO files VALUES (?,?,?,?)", (request.peer.host, request.peer.port, file.filepath, file.filename))

        conn.commit()
        conn.close()

        return peers_pb2.AddPeerWithFilesResponse(filesUploaded=len(request.files))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    peers_pb2_grpc.add_PeersServicer_to_server(Peers(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
