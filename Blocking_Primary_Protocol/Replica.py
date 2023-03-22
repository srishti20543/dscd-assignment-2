from __future__ import print_function

import sys
sys.path.insert(1, 'proto')

from concurrent import futures
from google.protobuf.timestamp_pb2 import Timestamp

import CommWithRegistryServer_pb2_grpc
import CommWithRegistryServer_pb2
import CommWithReplica_pb2_grpc
import CommWithReplica_pb2
import grpc
import logging
import datetime

def registerServer(stub, request):
    status = stub.Register(request)
    print(status)
    if "SUCCESS" in str(status):
        return 0


class CommWithReplicaServicer(CommWithReplica_pb2_grpc.CommWithReplicaServicer):

    def SendDetailsOfPR(self, request, context):
        pass 
                            

def connectToRegistry(arg):
    with grpc.insecure_channel('localhost:8888') as channel:
        stub = CommWithRegistryServer_pb2_grpc.CommWithRegistryServerStub(channel)
        request = CommWithRegistryServer_pb2.RegisterRequest(IP=arg[1], port=int(arg[2]))
        status = registerServer(stub, request)
        return status


# def connectToClient(arg):
#     server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
#     CommWithReplica_pb2_grpc.add_CommWithReplicaServicer_to_server(CommWithReplicaServicer(), server)
#     server.add_insecure_port('[::]:' + str(arg[2]))
#     server.start()
#     server.wait_for_termination()


if __name__ == '__main__':
    arg = sys.argv[1:]
    logging.basicConfig()
    status = connectToRegistry(arg)
    # if status == 0:
    #     connectToClient(arg)
