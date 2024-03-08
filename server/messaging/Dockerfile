FROM python

RUN mkdir /service
COPY protobufs/ /service/protobufs/
COPY messaging/ /service/messaging/
WORKDIR /service/messaging
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/messaging.proto
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/peers.proto
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/files.proto
EXPOSE 50051
ENTRYPOINT [ "python","-u" ,"messaging.py" ]