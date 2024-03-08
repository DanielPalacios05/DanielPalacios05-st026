# rpc_server.py
import os
import grpc
from concurrent import futures
from multiprocessing import Process
import queue_server
import rpc_server
import messaging_pb2 as pb2
import messaging_pb2_grpc as pb2_grpc
HOST = os.getenv("MQ_HOST","127.0.0.1")
"""QUEUES

fetch_request: Receives a peer fetching request and start sending peer info 
the initiatingPeer peer_info queue
fetch_response : Receives a linking peer confirmation that processed the call correctyle

peer_info : Receives the peers info and for every peer in it it will handle it

Each of these 
"""



if __name__ == '__main__':
    """There are 2 ongoing processes here:
    - RPC server for internal communication
    - RabbitMQ server that sets up the behaviour for every queue and starts consuming
    """

    rpc_process = Process(target=rpc_server.init_rpc_server)
    queue_server_process = Process(target=queue_server.init_queue_server)

    rpc_process.start()
    queue_server_process.start()
    
