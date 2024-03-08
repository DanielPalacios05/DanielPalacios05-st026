# Use an official Python runtime as a parent image
FROM python:3.8-slim

RUN mkdir /service
COPY protobufs/ /service/protobufs/
COPY /peerit-api-client /service/peerit-api-client
WORKDIR /service/peerit-api-client
# Copy the current directory contents into the container at /code
ENV PYTHONUNBUFFERED=1
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/peers.proto

RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/messaging.proto

RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/files.proto


# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
