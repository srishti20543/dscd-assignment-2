import sys
sys.path.insert(1, '../Protos')

from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime

import CommWithRegistryServer_pb2_grpc
import CommWithRegistryServer_pb2
import CommWithReplica_pb2_grpc
import CommWithReplica_pb2
import grpc
import logging


def getListOfServers(stub, request):
    status = stub.getReplicaList(request)
    for x in status:
        print(x.replicaServer.name + " - " + x.replicaServer.ip + ":" + str(x.replicaServer.port))
    print("\n")


def runRegistryServer(ip, port):
    with grpc.insecure_channel('localhost:8888') as channel:
        stub = CommWithRegistryServer_pb2_grpc.CommWithRegistryServerStub(channel)
        request = CommWithReplica_pb2.Address(name=None, ip=ip, port=port)
        getListOfServers(stub, request)


def write(server, uuid, fileName, content):
    serverAddr = server[0]+":"+str(server[1])
    with grpc.insecure_channel(serverAddr) as channel:
        stub = CommWithReplica_pb2_grpc.CommWithReplicaStub(channel)
        status = stub.Write(CommWithReplica_pb2.WriteRequest(uuid=uuid, name=fileName, content=content))
        time = status.version
        date = datetime.fromtimestamp(time.seconds)
        print("CLIENT: ")
        print("Status for write: " + status.status)
        print("UUID: " + status.uuid)
        print("Version: " + str(date) + "\n")

def read(server, uuid):
    serverAddr = server[0]+":"+str(server[1])
    with grpc.insecure_channel(serverAddr) as channel:
        stub = CommWithReplica_pb2_grpc.CommWithReplicaStub(channel)
        status = stub.Read(CommWithReplica_pb2.ReadRequest(uuid=uuid))
        time = status.version
        date = datetime.fromtimestamp(time.seconds)
        print("CLIENT:")
        print("Status: " + status.status)
        print("Name: " + status.name)
        print("Content: " + status.content)
        print("Version: " + str(date) + "\n")

def delete(server, uuid):
    serverAddr = server[0]+":"+str(server[1])
    with grpc.insecure_channel(serverAddr) as channel:
        stub = CommWithReplica_pb2_grpc.CommWithReplicaStub(channel)
        status = stub.Delete(CommWithReplica_pb2.DeleteRequest(uuid=uuid))
        print("CLIENT: \nStatus for delete: " + status.status + "\n")

if __name__ == '__main__':
    pass
