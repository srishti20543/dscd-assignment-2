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

myIP = 0
myPort = 0
def getListOfServers(stub, request):
    status = stub.getCompleteReplicaList(request)
    for x in status:
        print(x.replicaServer.name + " - " + x.replicaServer.ip + ":" + str(x.replicaServer.port))
    print("\n")

def getListOfReadServers(stub, request):
    return stub.getReadReplicaList(request)

def getListOfWriteServers(stub, request):
    return stub.getWriteReplicaList(request)


def runRegistryServer(ip, port):
    global myIP, myPort
    with grpc.insecure_channel('localhost:8888') as channel:
        stub = CommWithRegistryServer_pb2_grpc.CommWithRegistryServerStub(channel)
        request = CommWithReplica_pb2.Address(name=None, ip=ip, port=port)
        myIP = ip
        myPort = port
        getListOfServers(stub, request)

def read(uuid):
    global myIP, myPort

    with grpc.insecure_channel('localhost:8888') as channel:
        stub = CommWithRegistryServer_pb2_grpc.CommWithRegistryServerStub(channel)
        request = CommWithReplica_pb2.Address(name=None, ip=myIP, port=myPort)
        readServersInfo = getListOfReadServers(stub, request)
        latest = 0
        for x in readServersInfo:
            server = [x.replicaServer.ip, x.replicaServer.port]
            readResponse = read_single(server, uuid)
            if(latest == 0):
                latest = readResponse
            else:
                if(datetime.fromtimestamp(latest.version.seconds) < datetime.fromtimestamp(readResponse.version.seconds)):
                    latest = readResponse

        
        time = latest.version
        date = datetime.fromtimestamp(time.seconds)

        print("CLIENT:")
        print("Status: " + latest.status)
        print("Name: " + latest.name)
        print("Content: " + latest.content)
        if latest.name == "" and latest.status != "FAIL, FILE ALREADY DELETED":
            date = ""
        print("Version: " + str(date) + "\n")
        return latest

def read_single(server, uuid):
    serverAddr = server[0]+":"+str(server[1])
    with grpc.insecure_channel(serverAddr) as channel:
        stub = CommWithReplica_pb2_grpc.CommWithReplicaStub(channel)
        status = stub.Read(CommWithReplica_pb2.ReadRequest(uuid=uuid))

        time = status.version
        date = datetime.fromtimestamp(time.seconds)
        print("REPLICA Server Address:", serverAddr)
        print("Status: " + status.status)
        print("Name: " + status.name)
        print("Content: " + status.content)
        if status.name == "" and status.status != "FAIL, FILE ALREADY DELETED":
            date = ""
        print("Version: " + str(date) + "\n")

        return status



def write(uuid, fileName, content):
    global myIP, myPort
    statusList = []
    with grpc.insecure_channel('localhost:8888') as channel:
        stub = CommWithRegistryServer_pb2_grpc.CommWithRegistryServerStub(channel)
        request = CommWithReplica_pb2.Address(name=None, ip=myIP, port=myPort)
        status = getListOfWriteServers(stub, request)
        for x in status:
            server = [x.replicaServer.ip, x.replicaServer.port]
            statusList.append(write_single(server, uuid, fileName, content))
    return statusList

def write_single(server, uuid, fileName, content):
    serverAddr = server[0]+":"+str(server[1])
    with grpc.insecure_channel(serverAddr) as channel:
        stub = CommWithReplica_pb2_grpc.CommWithReplicaStub(channel)
        status = stub.Write(CommWithReplica_pb2.WriteRequest(uuid=uuid, name=fileName, content=content))
        time = status.version
        date = datetime.fromtimestamp(time.seconds)
        print("CLIENT: ")
        print("Status for write to server: " + serverAddr + " is: " + status.status)
        print("UUID: " + status.uuid)
        if 'FAIL' in status.status:
            date = ""
        print("Version: " + str(date) + "\n")
        return [status.status, status.uuid]

def delete(uuid):
    global myIP, myPort

    with grpc.insecure_channel('localhost:8888') as channel:
        stub = CommWithRegistryServer_pb2_grpc.CommWithRegistryServerStub(channel)
        request = CommWithReplica_pb2.Address(name=None, ip=myIP, port=myPort)
        status = getListOfWriteServers(stub, request)
        for x in status:
            server = [x.replicaServer.ip, x.replicaServer.port]
            delete_single(server, uuid)


def delete_single(server, uuid):
    # TODO: Add the special case to Replica.py
    serverAddr = server[0]+":"+str(server[1])
    with grpc.insecure_channel(serverAddr) as channel:
        stub = CommWithReplica_pb2_grpc.CommWithReplicaStub(channel)
        status = stub.Delete(CommWithReplica_pb2.DeleteRequest(uuid=uuid))
        print("CLIENT: \nStatus for delete to server: " + serverAddr + " is " + status.status + "\n")
        

if __name__ == '__main__':
    pass
