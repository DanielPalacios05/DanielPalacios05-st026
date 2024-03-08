import os
import pika
import json
import grpc
import peers_pb2
import peers_pb2_grpc
import files_pb2
import files_pb2_grpc
from linkedPeers import LinkedPeers
import messaging
import time
"""QUEUES
time.sleep(30)er fetching request and start sending peer info 
the initiatingPeer peer_info queue
fetch_response : Receives a linking peer confirmation that it processed the call correctly

peer_info : Receives the peers info and for every peer in it it will handle it

Each of these 
"""

def fetch_request_callback(ch, method, properties, body):
    """Body structure:request = str({"initiatingPeer":
                           {"ip":initiating_peer.ip,
                            "port":initiating_peer.port},
                            "peerPublicContact":{
                                "ip":peer.ip,
                                "port":peer.port
                            }})"""
    

    incoming_message = json.loads(body)

    linked_peers = LinkedPeers()

    peers_host = os.getenv("PEERS_HOST", "localhost")
    peers_channel = grpc.insecure_channel(f"{peers_host}:50051")

    files_host = os.getenv("FILES_HOST","localhost")
    files_channel = grpc.insecure_channel(f"{files_host}:50051")

    files_stub = files_pb2_grpc.FilesStub(files_channel)
    peers_stub = peers_pb2_grpc.PeersStub(peers_channel)

    linked_peers_request = peers_pb2.PeerListRequest(linkedPeers=1)
    available_files_request = files_pb2.AvailableFilesRequest()

    files_response = files_stub.listAvailableFiles(available_files_request)
    linked_peers_response  = peers_stub.ListPeers(linked_peers_request)

    initiating_peer= peers_pb2.Peer(ip=incoming_message["initiatingPeer"]["ip"],port=incoming_message["initiatingPeer"]["port"])


    connection = pika.BlockingConnection(pika.ConnectionParameters(host=initiating_peer.ip, port=initiating_peer.port))
    channel = connection.channel()

    request = json.dumps({"files":[
                           {"filename": file.filename,
                            "filepath":file.filepath} for file in linked_peers_response.file],
                            "peerPublicContact":{
                                "ip":peer.ip,
                                "port":peer.port
                            }})

    peer.channel.basic_publish(exchange='',
                                routing_key='peer_info',
                                body=request)


    for peer in linked_peers_response.peerEntry:

        linked_peers.add_peer(peer)
    
     

    

    linked_peers.broadcast_fetch(initiating_peer,30)

    


    pika.BlockingConnection()



    

    

    pass

def fetch_response_callback(ch, method, properties, body):
    pass



    



    pass

def init_queue_server():



    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters(messaging.HOST, 5672, '/', credentials)  
    time.sleep(30)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()


    queue = channel.queue_declare("fetch_request")
    channel.basic_consume(queue="fetch_request", on_message_callback=fetch_request_callback, auto_ack=True)
    
    channel.queue_declare("peer_info")


    channel.start_consuming()



    
    pass


if __name__ == "__main__":

    fetch_request_callback("","","","")

