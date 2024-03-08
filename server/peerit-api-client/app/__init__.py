import os
import urllib.parse
from flask import Flask,jsonify
from flask import request as req
import grpc
import peers_pb2
import peers_pb2_grpc
import messaging_pb2
import messaging_pb2_grpc
import files_pb2
import files_pb2_grpc

def get_hostname_and_port(url):
    """Extracts hostname and port from a URL.

    Args:
        url: The URL to parse.

    Returns:
        A tuple containing (hostname, port). If a port is not specified in the
        URL, the port is returned as None.
    """

    parsed_url = urllib.parse.urlparse(url)
    hostname = parsed_url.hostname
    port = parsed_url.port

    if not port:
        # If port is not specified, use default for the scheme
        scheme = parsed_url.scheme
        if scheme == "http":
            port = 80
        elif scheme == "https":
            port = 443

    return hostname,port

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    @app.route("/fetch/peers",methods=['GET'])
    def startFetch():

        args = req.args

        messaging_host = os.getenv("MESSAGING_HOST", "localhost")
        peers_host = os.getenv("PEERS_HOST","localhost")

        messaging_channel = grpc.insecure_channel(f"{messaging_host}:50051")
        peers_channel = grpc.insecure_channel(f"{peers_host}:50051")
        
        # Create a stub (client)
        msg_stub = messaging_pb2_grpc.FetchingStub(messaging_channel)
        peers_stub = peers_pb2_grpc.PeersStub(peers_channel)
        

        # Create a valid request message
        peer = peers_pb2.Peer(host=args.get("host"),port=args.get("port"))

        peers_request = peers_pb2.PeerListRequest(linkedPeers=1)

        linked_peers = peers_stub.ListPeers(peers_request).peers
        fetch_request = messaging_pb2.FetchRequest(initiatingPeer=peer,linkedPeers=linked_peers)

        # Make the call
        response = msg_stub.initFetch(fetch_request)
        
        return jsonify({"peersFetched":response.peersFetched,"filesFetched":response.filesFetched})
    
        
    
    @app.route('/peers/', methods=['POST','GET'])
    def link_peer():
        # Parse the JSON sent to this endpoint
        print(req.get_json())
        if req.method == 'POST':
            data = req.get_json()

            hostname,port = get_hostname_and_port(data['peerUrl'])
            
            # Log the received data (just to show we've received it)
            print("Received data:", data)

            host = os.getenv("PEERS_HOST", "localhost")
            channel = grpc.insecure_channel(
                f"{host}:50051"
            )


            # Create a stub (client)
            stub = peers_pb2_grpc.PeersStub(channel)

            # Create a valid request message
            peer = peers_pb2.Peer(host=hostname, port=port)
            request = peers_pb2.PeerLinkRequest(peer=peer, linkPeer=data['toLink'])

            # Make the call
            response = stub.AddPeer(request)

            # Echo back the modified data
            return jsonify({"host": hostname, "port": port, "toLink": data['toLink'], "added": response.added})
        elif req.method == 'GET':
            host = os.getenv("PEERS_HOST", "localhost")
            channel = grpc.insecure_channel(f"{host}:50051")

            # Create a stub (client)
            stub = peers_pb2_grpc.PeersStub(channel)

            # Create a valid request message
            request = peers_pb2.PeerListRequest()

            # Make the calls
            response = stub.ListPeers(request)

            # Convert the response to a list of dictionaries
            peers = [{"host": peer.peer.host, "port": peer.peer.port, "toLink": peer.linkPeer} for peer in response.peerEntry]

            # Return the list of peers
            return jsonify(peers)
        
    @app.route('/files/', methods=['POST','GET'])
    def addFiles():
        host = os.getenv("FILES_HOST", "localhost")
        
        channel = grpc.insecure_channel(
                f"{host}:50051"
            )
        

            # Create a stub (client)
        stub = files_pb2_grpc.FilesStub(channel)
        # Parse the JSON sent to this endpoint
        print(req)
        if req.method == 'POST':
            data = req.get_json()            
            # Log the received data (just to show we've received it)
            print("Received data:", data)

           


            for file in data:
                file = files_pb2.File(filename=file.get("filename"), filepath=file.get("filepath"))
                request = files_pb2.AddFileRequest(file=file)

                response = stub.addFile(request)

                if not response.isFileUploaded:

                    return str(f"File {file.filename} was not able to be uploaded"),500
            

            return jsonify("Files sucessfully added"),200
        elif req.method == 'GET':

            # Create a valid request message
            request = files_pb2.AvailableFilesRequest()

            # Make the calls
            response = stub.listAvailableFiles(request)

            files = [{"filename":file.filename,"filepath":file.filepath} for file in response.file]

            # Convert the response to a list of dictionaries
            # Return the list of peers
            return jsonify(files)





    return app