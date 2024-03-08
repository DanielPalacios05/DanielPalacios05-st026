import json
import os
import time
import grpc
from concurrent import futures
import peers_pb2_grpc
import peers_pb2
import messaging_pb2 as pb2
import messaging_pb2_grpc as pb2_grpc
from linkedPeers import LinkedPeers
from linkedPeer import LinkedPeer
import pika
import messaging



def peer_info_callback(body):

    incoming_message = json.loads(body)


    # Extract the peer and files information from the incoming message
    peer_info = incoming_message['peerPublicContact']
    files_info = incoming_message['files']

    # Create a gRPC channel to the peer
    host = os.getenv("PEERS_HOST", "localhost")
    channel = grpc.insecure_channel(f"{host}:50051")


    # Create a stub (client) for the Peers service
    stub = peers_pb2_grpc.PeersStub(channel)

    # Create a AddPeerWithFilesRequest
    request = peers_pb2.AddPeerWithFilesRequest()
    request.peer.host = peer_info['ip']
    request.peer.port = peer_info['port']

    # Add the files to the request
    for file_info in files_info:
        file = request.files.add()
        file.filepath = file_info['filepath']
        file.filename = file_info['filename']

    # Make the RPC call
    response = stub.AddPeerWithFiles(request)

    # Print the response
    return response.filesUploaded

class FetchingServicer(pb2_grpc.FetchingServicer):

        
    def initFetch(self, request, context):

        linked_peers : LinkedPeers = LinkedPeers()

        initiating_peer = request.initiatingPeer
        linkedPeers = request.linkedPeers

        # Convert the initiatingPeer and linkedPeers to LinkedPeer instances and add them to linked_peers

        for peer in linkedPeers:
            peer_instance = LinkedPeer(peer.ip, peer.port,[])
            linked_peers.add_peer(peer_instance)

        # Call broadcast_fetch with the initiating_peer_instance
        linked_peers.broadcast_fetch(initiating_peer,20)
        
        
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=messaging.HOST))

        channel = connection.channel()

        peersFetched = 0
        filesFetched = 0

        while True:
            method_frame, header_frame, body = channel.basic_get('peer_info')
            if method_frame:
                filesFetched += peer_info_callback(body)
                peersFetched += 1
            else:
                print('No more messages in queue')
                break


        




        # Implement your logic here
        # For now, let's return a dummy response
        return pb2.FetchResponse(peersFetched=peersFetched, filesFetched=filesFetched)
    


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_FetchingServicer_to_server(FetchingServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("RPC server started on port 50051")
    server.wait_for_termination()

def init_rpc_server():
    serve()