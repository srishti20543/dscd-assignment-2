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
import uuid

unique_id = str(uuid.uuid1())


def getListOfServers(stub, request):
    status = stub.getReplicaList(request)
    for x in status:
        print(x.replicaServer.name + " - " + x.replicaServer.IP + ":" + str(x.replicaServer.port))


def runRegistryServer(IP, port):
    with grpc.insecure_channel('localhost:8888') as channel:
        stub = CommWithRegistryServer_pb2_grpc.CommWithRegistryServerStub(channel)
        request = CommWithReplica_pb2.Address(name=None, IP=IP, port=port)
        getListOfServers(stub, request)


def runServer(client, choice):
    print("Enter Server Information")
    info = input()
    list_string = info.split(' ')
    server = ["", "", ""]
    server[0] = list_string[0]
    server[1], server[2] = list_string[1].split(":")
    server[2] = int(server[2])
    # if choice == 2:
    #     joinServer(client, server)
    # elif choice == 3:
    #     leaveServer(client, server)
    # elif choice == 4:
    #     getArticles(client, server)
    # elif choice == 5:
    #     publishArticles(client, server)


if __name__ == '__main__':
    pass
