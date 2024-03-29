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
        print("PRIMARY REPLICA: NEW BACK UP REPLICA HAS JOINED")
        print("Got details of replica: " + request.name + "\n")
        if request.name in Replicas.keys():
            return CommWithReplica_pb2.StatusRepReq(status="FAIL")
        Replicas[request.name] = (request.ip, request.port)
        return CommWithReplica_pb2.StatusRepReq(status="SUCCESS")  


    def ConnectToReplicaforWrite(self, request, context):
        Files[request.uuid] = [request.name, request.version]
        requestTowrite = CommWithReplica_pb2.WriteRequest(uuid=request.uuid, name=request.name, content=request.content)
        status = writeInFile(requestTowrite)
        return status
    
    def ConnectToReplicaforDelete(self, request, context):
        Files[request.uuid][1] = request.version
        requestToDelete = CommWithReplica_pb2.DeleteRequest(uuid=request.uuid)
        status = DeleteFile(requestToDelete)
        return status
    

    def ConnectToPRforWrite(self, request, context):
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
                    status = stub.ConnectToReplicaforWrite(CommWithReplica_pb2.Request(uuid=request.uuid, name=request.name, content=request.content, version=Files[request.uuid][1]))
                
                if 'SUCCESS' in status.status:
                    count +=1

            if count == len(Replicas):
               return CommWithReplica_pb2.StatusRepReq(status=status.status) 

            # Then contact final backup 
            return CommWithReplica_pb2.StatusRepReq(status="FAIL, WRITE NOT COMPLETED IN ALL REPLICAS")

        else:
            # Connect to final backup and send FAIL to client
            return CommWithReplica_pb2.StatusRepReq(status=status.status)
        

    def ConnectToPRforDelete(self, request, context):
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

        if "SUCCESS" in status.status:
            # Contact all replicas and get ack
            count = 0

            for replica in Replicas.keys():
                serverAddr = Replicas[replica][0] + ":" + str(Replicas[replica][1])

                with grpc.insecure_channel(serverAddr) as channel:
                    stub = CommWithReplica_pb2_grpc.CommWithReplicaStub(channel)
                    status = stub.ConnectToReplicaforDelete(CommWithReplica_pb2.DeleteRequestToReplica(uuid=request.uuid, version=Files[request.uuid][1]))
                
                if 'SUCCESS' in status.status:
                    count +=1

            if count == len(Replicas):
               return CommWithReplica_pb2.StatusRepReq(status=status.status) 

            # Then contact final backup 
            return CommWithReplica_pb2.StatusRepReq(status="FAIL, DELETE NOT COMPLETED IN ALL REPLICAS")

        else:
            # Connect to final backup and send FAIL to client
            return CommWithReplica_pb2.StatusRepReq(status=status.status)


    def Write(self, request, context):
        # Primary Replica -> Connection
        serverAddr = PR_details["ip"] + ":" + str(PR_details["port"])
        with grpc.insecure_channel(serverAddr) as channel:
            stub = CommWithReplica_pb2_grpc.CommWithReplicaStub(channel)
            status = stub.ConnectToPRforWrite(CommWithReplica_pb2.WriteRequest(uuid=request.uuid, name=request.name, content=request.content))

            if "SUCCESS" in status.status:
                return CommWithReplica_pb2.WriteResponse(status=status.status, uuid=request.uuid, version=Files[request.uuid][1])
            else:
                return CommWithReplica_pb2.WriteResponse(status=status.status, uuid=None, version=None)


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
        

    def Delete(self, request, context):
        # Primary Replica -> Connection
        serverAddr = PR_details["ip"] + ":" + str(PR_details["port"])
        with grpc.insecure_channel(serverAddr) as channel:
            stub = CommWithReplica_pb2_grpc.CommWithReplicaStub(channel)
            status = stub.ConnectToPRforDelete(CommWithReplica_pb2.DeleteRequest(uuid=request.uuid))
        
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
        flag = 1
        
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
        return CommWithReplica_pb2.StatusRepReq(status="FAIL, FILE DOES NOT EXIST")
    else:
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
            PR_details['name'] = status.primaryServerAddress.name
            PR_details['ip'] = status.primaryServerAddress.ip
            PR_details['port'] = status.primaryServerAddress.port
            print("REPLICA: " + selfDetails["name"] + " WAS SUCCESSFULLY REGISTERED")
            print("PR Details : ", PR_details)
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

