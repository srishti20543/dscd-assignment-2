from __future__ import print_function

import sys
sys.path.insert(1, '../Protos')

from concurrent import futures
from google.protobuf.timestamp_pb2 import Timestamp

import CommWithRegistryServer_pb2_grpc
import CommWithRegistryServer_pb2
import CommWithReplica_pb2_grpc
import CommWithReplica_pb2
import grpc
import logging
import datetime

Replicas = []

def registerServer(stub, request):
    status = stub.Register(request)
    print(status)
    if "SUCCESS" in str(status):
        return 0


class CommWithReplicaServicer(CommWithReplica_pb2_grpc.CommWithServerServicer):

    def SendDetailsOfPR(self, request, context):
        print("NEW BACK UP SERVER HAS JOINED")
        if (request.IP, request.port) in Replicas:
            return CommWithReplica_pb2.SendDetailsOfPRResponse(Status="FAIL")
        Replicas.append((request.IP, request.port))
        return CommWithReplica_pb2.SendDetailsOfPRResponse(Status="SUCCESS")              

def connectToRegistry(IP, port):
    with grpc.insecure_channel('localhost:8888') as channel:
        stub = CommWithRegistryServer_pb2_grpc.CommWithRegistryServerStub(channel)
        request = CommWithReplica_pb2.Address(IP=IP, port=port)
        status = registerServer(stub, request)
        return status
    
def SendDetailsForPR(IP, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    CommWithReplica_pb2_grpc.add_CommWithRegistryReplicaservicer_to_server(CommWithReplicaServicer(), server)
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    server.wait_for_termination()


# def connectToClient(arg):
#     server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
#     CommWithReplica_pb2_grpc.add_CommWithReplicaServicer_to_server(CommWithReplicaServicer(), server)
#     server.add_insecure_port('[::]:' + str(arg[2]))
#     server.start()
#     server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()

