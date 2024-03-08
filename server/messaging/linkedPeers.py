# linkedPeers.py
import json
import time
from linkedPeer import LinkedPeer
import pika
class LinkedPeers:
    def __init__(self):
        self.peers_list = []  # Initialize an empty list to store peers

    def add_peer(self, peer):
        # Add a peer to thze list
        self.peers_list.append(peer)

    def remove_peer(self, peer):
        # Remove a peer from the list
        self.peers_list.remove(peer)

    def get_all_peers(self):
        # Retrieve the list of all peers
        return self.peers_list
    
    def broadcast_fetch(self,initiating_peer,ttl):

        """TODO: Create Fetching TTL so whent it ends it starts consuming
        the peersFetched queue for every peer it adds it to the discovered peers
        with the files"""

        for peer in self.peers_list:

            request = json.dumps({"initiatingPeer":
                           {"ip":initiating_peer.ip,
                            "port":initiating_peer.port},
                            "peerPublicContact":{
                                "ip":peer.ip,
                                "port":peer.port
                            }})

            peer.channel.basic_publish(exchange='',
                                routing_key='fetch_requests',
                                body=request)
            
        print("waiting for fetch:",ttl,"seconds left")
        
        time.sleep(ttl)
            


            

    # Add other relevant methods as needed (e.g., broadcasting messages)

# Usage example:
if __name__ == "__main__":
    linked_peers = LinkedPeers()
    # Add peers using linked_peers.add_peer(peer_instance)
    # Remove peers using linked_peers.remove_peer(peer_instance)
    # Retrieve all peers using linked_peers.get_all_peers()
