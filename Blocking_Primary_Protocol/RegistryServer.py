import sys
sys.path.insert(1, 'Proto')

from concurrent import futures

import CommWithRegistryServer_pb2_grpc
import CommWithRegistryServer_pb2
import logging
import grpc

PR_details = {}
Replicas = {}


def addReplicas(name, IP, port):

    if name == 'replica_1':
        PR_details['IP'] = IP
        PR_details['port'] = port

    for replica in Replicas.keys():
        addr = Replicas[replica][0] + str(Replicas[replica][1])
        check_addr = IP + str(port)
        if addr == check_addr:
            return 1

    Replicas[name] = [IP, port]
    return 0



class CommWithRegistryReplicaservicer(CommWithRegistryServer_pb2_grpc.CommWithRegistryReplicaservicer):

    def Register(self, request, context):
        print("JOIN REQUEST FROM " + request.address.IP + ":" + str(request.address.port))
        nextcount = len(Replicas) + 1
        name = 'replica_' + str(nextcount)
        result = addReplicas(name, request.address.IP, request.address.port)
        if result == 0:
            return CommWithRegistryServer_pb2.RegisterResponse(status="SUCCESS", primaryServerAddress=CommWithRegistryServer_pb2.Address(IP=PR_details['IP'],Port=PR_details['port']))
        else:
            return CommWithRegistryServer_pb2.RegisterResponse(status="FAIL", primaryServerAddress=None)


    def getReplicaList(self, request, context):
        print("REPLICA LIST REQUEST FROM " + request.address.IP + ":" + str(request.address.port))
        for replica in Replicas.keys():
            IP = Replicas[replica][0]
            port = Replicas[replica][1]
            yield CommWithRegistryServer_pb2.ReplicaListResponse(name=replica, address= CommWithRegistryServer_pb2.Address(IP=IP, port=port))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    CommWithRegistryServer_pb2_grpc.add_CommWithRegistryReplicaservicer_to_server(CommWithRegistryReplicaservicer(), server)
    server.add_insecure_port('[::]:8888')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
