# peers.py
import pika  # Assuming you're using the pika library for RabbitMQ

class LinkedPeer:
    def __init__(self, ip, port, queue_names):
        self.ip = ip
        self.port = port
        self.queue_names = queue_names  # List of queue names to declare

        # Set up RabbitMQ connection
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.ip, port=self.port))
        self.channel = self.connection.channel()

        # Declare queues
        for queue_name in self.queue_names:
            self.channel.queue_declare(queue=queue_name)

    def send_message(self, queue_name, message):
        # Send a message to the specified queue
        self.channel.basic_publish(exchange='', routing_key=queue_name, body=message)

    def receive_message(self, queue_name):
        # Receive a message from the specified queue
        method_frame, header_frame, body = self.channel.basic_get(queue=queue_name)
        if method_frame:
            return body.decode('utf-8')
        else:
            return None
    
    
        


    # Add other relevant methods (e.g., handling acknowledgments)

# Usage example:
if __name__ == "__main__":
    peer1 = LinkedPeer(ip='localhost', port=5672, queue_names=['queue1', 'queue2'])
    peer2 = LinkedPeer(ip='localhost', port=5672, queue_names=['queue2', 'queue3'])
    # Use peer1.send_message(queue_name, message) and peer2.receive_message(queue_name) to communicate
