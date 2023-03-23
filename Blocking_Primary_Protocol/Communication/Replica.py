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

PR_details = {}
Replicas = {}
selfName = ''


class CommWithReplicaServicer(CommWithReplica_pb2_grpc.CommWithReplicaServicer):

    def SendDetailsOfPR(self, request, context):
        print("NEW BACK UP SERVER HAS JOINED")
        print(request)
        if request.name in Replicas.keys():
            return CommWithReplica_pb2.SendDetailsOfPRResponse(Status="FAIL")
        Replicas[request.name] = (request.IP, request.port)
        return CommWithReplica_pb2.SendDetailsOfPRResponse(Status="SUCCESS")            

def connectToRegistry(IP, port):
    global selfName

    with grpc.insecure_channel('localhost:8888') as channel:
        stub = CommWithRegistryServer_pb2_grpc.CommWithRegistryServerStub(channel)
        request = CommWithReplica_pb2.Address(IP=IP, port=port, name=None)
        status = stub.Register(request)
        if status.status == "SUCCESS":
            selfName = status.selfName
            PR_details['name'] = status.primaryServerAddress.name
            PR_details['IP'] = status.primaryServerAddress.IP
            PR_details['port'] = status.primaryServerAddress.port
            print(selfName + " SUCCESSFULLY REGISTERED")
            print("PR Details ", PR_details)
        else:
            print(status.status)

    
def ConnectToReplica(IP, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    CommWithReplica_pb2_grpc.add_CommWithReplicaServicer_to_server(CommWithReplicaServicer(), server)
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

