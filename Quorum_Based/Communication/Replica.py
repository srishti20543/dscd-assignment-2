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
Replicas = {}
Files = {}


class CommWithReplicaServicer(CommWithReplica_pb2_grpc.CommWithReplicaServicer):
   
    def Write(self, request, context):
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
            return CommWithReplica_pb2.WriteResponse(status=status.status, uuid=request.uuid, version=Files[request.uuid][1])
        else:
            return CommWithReplica_pb2.WriteResponse(status=status.status, uuid=None, version=None)


    def Read(self, request, context):
        if request.uuid in Files.keys():
            for uuid in Files.keys():
                if uuid == request.uuid:
                    if Files[uuid][0] == "":
                        return CommWithReplica_pb2.ReadResponse(status="FAIL, FILE ALREADY DELETED", name=None, content=None, version=Files[request.uuid][1])
                    else:
                        directory = "../Datafile/"+selfDetails["name"] + "/"
                        with open(directory+Files[uuid][0], "r") as f:
                            # Write some text to the file
                            content = f.read()
                        return CommWithReplica_pb2.ReadResponse(status="SUCCESS", name=Files[uuid][0], content=content, version=Files[uuid][1])
        else:
            return CommWithReplica_pb2.ReadResponse(status="FAIL, FILE DOESNOT EXIST", name=None, content=None, version=None)
        

    def Delete(self, request, context):
        flag = 0
        if request.uuid in Files.keys():
            if Files[request.uuid][0] == "":
                    flag = 1
                    
            if flag == 0:
                # Open a file for writing
                ct = datetime.datetime.now()
                timestamp = ct.timestamp()
                time = Timestamp(seconds=int(timestamp))
                Files[request.uuid][1] = time

        status = DeleteFile(request)
        
        return CommWithReplica_pb2.StatusRepReq(status=status.status)


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
            if Files[request.uuid][0] == "":
                return CommWithReplica_pb2.StatusRepReq(status="FAIL, DELETED FILE CANNOT BE UPDATED")
            else:
                return CommWithReplica_pb2.StatusRepReq(status="FAIL, CANNOT HAVE TWO DIFFERENT FILES WITH SAME UUID")


def DeleteFile(request):
    flag = 0
    if request.uuid not in Files.keys():
        # File was NOT in map
        ct = datetime.datetime.now()
        timestamp = ct.timestamp()
        time = Timestamp(seconds=int(timestamp))
        Files[request.uuid] = ["", time]

        return CommWithReplica_pb2.StatusRepReq(status="FAIL, FILE DOES NOT EXIST, BUT ADDED EMPTY FILE TO MAP")
    else:
        # File found in map
        if request.uuid in Files.keys():
            if Files[request.uuid][0] == "":
                    flag = 1
                
        if flag == 0:
            # Open a file for writing
            directory = "../Datafile/" + selfDetails["name"] + "/" +  Files[request.uuid][0]
            if os.path.exists(directory):
                # Delete the file
                os.remove(directory)
                

            Files[request.uuid][0] = ""
            return CommWithReplica_pb2.StatusRepReq(status="SUCCESS") 
        else:
            return CommWithReplica_pb2.StatusRepReq(status="FAIL, FILE ALREADY DELETED")


def connectToRegistry(ip, port):

    with grpc.insecure_channel('localhost:8888') as channel:

        stub = CommWithRegistryServer_pb2_grpc.CommWithRegistryServerStub(channel)
        request = CommWithReplica_pb2.Address(ip=ip, port=port, name=None)

        status = stub.Register(request)

        if status.status == "SUCCESS":
            selfDetails["name"] = status.selfName
            selfDetails["ip"] = ip
            selfDetails["port"] = port
            print("REPLICA: " + selfDetails["name"] + " WAS SUCCESSFULLY REGISTERED")
            print("\n")

            directory = "../Datafile/"+selfDetails["name"]+"/"
            if not os.path.exists(directory):
                os.makedirs(directory)

        else:
            print("REPLICA: Status for connecting to Registry Server: " + status.status)

    
def ConnectToReplica(ip, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    CommWithReplica_pb2_grpc.add_CommWithReplicaServicer_to_server(CommWithReplicaServicer(), server)
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()

