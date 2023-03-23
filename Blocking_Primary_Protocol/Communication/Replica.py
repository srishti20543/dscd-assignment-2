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
import os

selfName = ""

PR_details = {}
Replicas = {}
Files = {}


class CommWithReplicaServicer(CommWithReplica_pb2_grpc.CommWithReplicaServicer):

    def SendDetailsOfPR(self, request, context):
        print("NEW BACK UP SERVER HAS JOINED")
        print(request)
        if request.name in Replicas.keys():
            return CommWithReplica_pb2.SendDetailsOfPRResponse(Status="FAIL")
        Replicas[request.name] = (request.IP, request.port)
        return CommWithReplica_pb2.SendDetailsOfPRResponse(Status="SUCCESS")       

    def WriteRequest(self, request, context):
        flag = 1
        if request.uuid not in Files.keys():
            for uuid in Files.keys():
                if Files[uuid][0] == request.name:
                    flag = 0
                    break
                    
            if flag == 1:
                # Open a file for writing
                directory = "../Datafile/"+selfName+"/"
                with open(directory+request.name, "w") as f:
                    # Write some text to the file
                    f.write(request.content)
                return CommWithReplica_pb2.WriteResponse(Status="SUCCESS") 
            else:
                return CommWithReplica_pb2.WriteResponse(Status="FAIL, FILE WITH THE SAME NAME ALREADY EXISTS")
        else:
            for uuid in Files.keys():
                if Files[uuid][0] == request.name:
                    flag = 0
                    break
                    
            if flag == 0:
                # Open a file for writing
                directory = "../Datafile/"+selfName+"/"
                with open(directory+request.name, "w") as f:
                    # Write some text to the file
                    f.write(request.content)
                return CommWithReplica_pb2.WriteResponse(Status="SUCCESS") 
            else:
                return CommWithReplica_pb2.WriteResponse(Status="FAIL, DELETED FILE CANNOT BE UPDATED")


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

            directory = "../Datafile/"+selfName+"/"
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Directory {directory} created successfully.")
            else:
                print(f"Directory {directory} already exists.")

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

