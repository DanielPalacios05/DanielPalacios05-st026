FROM python

RUN mkdir /service
COPY protobufs/ /service/protobufs/
COPY peers/ /service/peers/
WORKDIR /service/peers
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/files.proto
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/peers.proto
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/messaging.proto

EXPOSE 50051
ENTRYPOINT [ "python", "peers.py" ]