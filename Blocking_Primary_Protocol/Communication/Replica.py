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

selfDetails = {}
PR_details = {}
Replicas = {}
Files = {}


class CommWithReplicaServicer(CommWithReplica_pb2_grpc.CommWithReplicaServicer):

    def SendDetailsOfPR(self, request, context):
        print("NEW BACK UP SERVER HAS JOINED")
        print(request)
        if request.name in Replicas.keys():
            return CommWithReplica_pb2.StatusRepReq(status="FAIL")
        Replicas[request.name] = (request.ip, request.port)
        return CommWithReplica_pb2.StatusRepReq(status="SUCCESS")  

    def ConnectToReplica(self, request, context):
        Files[request.uuid] = [request.name, request.version]
        requestTowrite = CommWithReplica_pb2.WriteRequest(uuid=request.uuid, name=request.name, content=request.content)
        status = writeInFile(requestTowrite)
        return status
    
    def ConnectToPR(self, request, context):

        flag = 1
        if request.uuid not in Files.keys():
            for uuid in Files.keys():
                if Files[uuid][0] == request.name:
                    flag = 0
                    break
                    
            if flag == 1:
                ct = datetime.datetime.now()
                timestamp = ct.timestamp()
                time = Timestamp(seconds=int(timestamp))
                Files[request.uuid] = [request.name, time]
                
        else:
            for uuid in Files.keys():
                if Files[uuid][0] == request.name:
                    flag = 0
                    break
                    
            if flag == 0:
                # Open a file for writing
                ct = datetime.datetime.now()
                timestamp = ct.timestamp()
                time = Timestamp(seconds=int(timestamp))
                Files[request.uuid][1] = time

        status = writeInFile(request)

        if "SUCCESS" in status.status:
            # Contact all replicas and get ack
            count = 0

            for replica in Replicas.keys():
                serverAddr = Replicas[replica][0] + ":" + str(Replicas[replica][1])

                with grpc.insecure_channel(serverAddr) as channel:
                    stub = CommWithReplica_pb2_grpc.CommWithReplicaStub(channel)
                    status = stub.ConnectToReplica(CommWithReplica_pb2.Request(uuid=request.uuid, name=request.name, content=request.content, version=Files[request.uuid][1]))
                
                if 'SUCCESS' in status.status:
                    count +=1

            if count == len(Replicas):
               return CommWithReplica_pb2.StatusRepReq(status=status.status) 

            # Then contact final backup 
            return CommWithReplica_pb2.StatusRepReq(status="FAIL, WRITE NOT COMPLETED IN ALL REPLICAS")

        else:
            # Connect to final backup and send FAIL to client
            return CommWithReplica_pb2.StatusRepReq(status=status.status)


    def Write(self, request, context):
        # Primary Replica -> Connection
        serverAddr = PR_details["ip"] + ":" + str(PR_details["port"])
        with grpc.insecure_channel(serverAddr) as channel:
            stub = CommWithReplica_pb2_grpc.CommWithReplicaStub(channel)
            status = stub.ConnectToPR(CommWithReplica_pb2.WriteRequest(uuid=request.uuid, name=request.name, content=request.content))
            return status

    def Read(self, request, context):
        if request.uuid in Files.keys():
            for uuid in Files.keys():
                if uuid == request.uuid:
                    if Files[uuid][0] == "":
                        return CommWithReplica_pb2.ReadResponse(status="FAIL, FILE ALREADY DELETED", name=None, content=None, version=None)
                    else:
                        directory = "../Datafile/"+selfDetails["name"] + "/"
                        with open(directory+Files[uuid][0], "r") as f:
                            # Write some text to the file
                            content = f.read()
                        return CommWithReplica_pb2.ReadResponse(status="SUCCESS", name=Files[uuid][0], content=content, version=Files[uuid][1])
        else:
            return CommWithReplica_pb2.ReadResponse(status="FAIL, FILE DOESNOT EXIST", name=None, content=None, version=None)

def writeInFile(request):
    flag = 1
    if request.uuid not in Files.keys():
        for uuid in Files.keys():
            if Files[uuid][0] == request.name:
                flag = 0
                break
                
        if flag == 1:
            # Open a file for writing
            directory = "../Datafile/"+selfDetails["name"] + "/"
            with open(directory+request.name, "w") as f:
                # Write some text to the file
                f.write(request.content)
            return CommWithReplica_pb2.StatusRepReq(status="SUCCESS") 
        else:
            return CommWithReplica_pb2.StatusRepReq(status="FAIL, FILE WITH THE SAME NAME ALREADY EXISTS")
    else:
        for uuid in Files.keys():
            if Files[uuid][0] == request.name:
                flag = 0
                break
                
        if flag == 0:
            # Open a file for writing
            directory = "../Datafile/"+selfDetails["name"]+"/"
            with open(directory+request.name, "w") as f:
                # Write some text to the file
                f.write(request.content)
            return CommWithReplica_pb2.StatusRepReq(status="SUCCESS") 
        else:
            return CommWithReplica_pb2.StatusRepReq(status="FAIL, DELETED FILE CANNOT BE UPDATED")


def connectToRegistry(ip, port):

    with grpc.insecure_channel('localhost:8888') as channel:
        stub = CommWithRegistryServer_pb2_grpc.CommWithRegistryServerStub(channel)
        request = CommWithReplica_pb2.Address(ip=ip, port=port, name=None)
        status = stub.Register(request)

        if status.status == "SUCCESS":
            selfDetails["name"] = status.selfName
            selfDetails["ip"] = ip
            selfDetails["port"] = port
            PR_details['name'] = status.primaryServerAddress.name
            PR_details['ip'] = status.primaryServerAddress.ip
            PR_details['port'] = status.primaryServerAddress.port
            print(selfDetails["name"] + " SUCCESSFULLY REGISTERED")
            print("PR Details ", PR_details)

            directory = "../Datafile/"+selfDetails["name"]+"/"
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Directory {directory} created successfully.")
            else:
                print(f"Directory {directory} already exists.")

        else:
            print(status.status)

    
def ConnectToReplica(ip, port):
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

