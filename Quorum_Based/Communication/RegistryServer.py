import sys
import Replica

sys.path.insert(1, '../Protos')

from concurrent import futures

import CommWithRegistryServer_pb2_grpc
import CommWithRegistryServer_pb2
import CommWithReplica_pb2_grpc
import CommWithReplica_pb2
import logging
import grpc
import threading
from multiprocessing import Process
import time
import random

Replicas = {}
N_R = 0
N_W = 0
N = 0
initiated_servers = 0


def addReplicas(name, ip, port):

    for replica in Replicas.keys():
        addr = Replicas[replica][0] + str(Replicas[replica][1])
        check_addr = ip + str(port)
        if addr == check_addr:
            return 1

    Replicas[name] = [ip, port]
    return 0


class CommWithRegistryServerServicer(CommWithRegistryServer_pb2_grpc.CommWithRegistryServerServicer):

    def Register(self, request, context):
        global N, N_R, N_W, initiated_servers
        print("REGISTRY SERVER: JOIN REQUEST FROM " + request.ip + ":" + str(request.port) + "\n")

        nextcount = len(Replicas) + 1
        name = 'replica_' + str(nextcount)
        
        # Checks if the addition of a new server, violates quorum requirements
        if initiated_servers == N:
            return CommWithRegistryServer_pb2.RegisterReplicaResponse(status="FAIL", selfName=None)

        result = addReplicas(name, request.ip, request.port)
        if result == 0:
            initiated_servers += 1
            return CommWithRegistryServer_pb2.RegisterReplicaResponse(status="SUCCESS", selfName=name)
        else:
            return CommWithRegistryServer_pb2.RegisterReplicaResponse(status="FAIL", selfName=None)


    def getCompleteReplicaList(self, request, context):
        print("REGISTRY SERVER: REPLICA LIST REQUEST FROM CLIENT " + request.ip + ":" + str(request.port) + "\n")
        for replica in Replicas.keys():
            ip = Replicas[replica][0]
            port = Replicas[replica][1]
            yield CommWithRegistryServer_pb2.ReplicaListResponse(replicaServer= CommWithReplica_pb2.Address(name=replica, ip=ip, port=port))

    def getReadReplicaList(self, request, context):
        # random_keys = random.sample(Replicas.keys(), N_R)
        random_keys = random.sample(list(Replicas.keys()), N_R)
        print("Randomly chosen replicas are: ", random_keys)
        print("REGISTRY SERVER: READ LIST REQUEST FROM CLIENT " + request.ip + ":" + str(request.port) + "\n")
        for replica in random_keys:
            ip = Replicas[replica][0]
            port = Replicas[replica][1]

            yield CommWithRegistryServer_pb2.ReplicaListResponse(replicaServer= CommWithReplica_pb2.Address(name=replica, ip=ip, port=port))

    def getWriteReplicaList(self, request, context):
        # random_keys = random.sample(Replicas.keys(), N_W)
        random_keys = random.sample(list(Replicas.keys()), N_W)
        print("Randomly chosen replicas are: ", random_keys)
        print("REGISTRY SERVER: WRITE LIST REQUEST FROM CLIENT " + request.ip + ":" + str(request.port) + "\n")
        for replica in random_keys:
            ip = Replicas[replica][0]
            port = Replicas[replica][1]
            yield CommWithRegistryServer_pb2.ReplicaListResponse(replicaServer= CommWithReplica_pb2.Address(name=replica, ip=ip, port=port))
 

    def getQuorumParams(self, request, context):
        print("REGISTRY SERVER: GET QUORUM PARAMS REQUEST FROM CLIENT " + request.ip + ":" + str(request.port) + "\n")
        return CommWithRegistryServer_pb2.QuorumParams(totalReplicas = N, numReads = N_R, numWrites = N_W)
    
def startRegistryServer(totalServers, numRead, numWrite):
    global N, N_R, N_W
    N = totalServers
    N_R = numRead
    N_W = numWrite

    # Validate input data

    if(not (N_W > N//2 and N_W + N_R > N and N_W <= N and N_R <= N)):
        print("ERROR: INVALID VALUES OF N, N_R and N_W, try again")
        exit(1)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    CommWithRegistryServer_pb2_grpc.add_CommWithRegistryServerServicer_to_server(CommWithRegistryServerServicer(), server)
    server.add_insecure_port('[::]:8888')
    server.start()
    print("REGISTRY SERVER STARTED SUCCESSFULLY")
    print("N: ",N)
    print("N_R: ",N_R)
    print("N_W: ",N_W)
    
    server.wait_for_termination()
    

if __name__ == '__main__':
    logging.basicConfig()
