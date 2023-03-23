import sys
sys.path.insert(1, '../Protos')

from concurrent import futures

import CommWithRegistryServer_pb2_grpc
import CommWithRegistryServer_pb2
import CommWithReplica_pb2_grpc
import CommWithReplica_pb2
import logging
import grpc
import threading

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


class CommWithRegistryServerServicer(CommWithRegistryServer_pb2_grpc.CommWithRegistryServerServicer):

    def Register(self, request, context):
        print("JOIN REQUEST FROM " + request.IP + ":" + str(request.port))
        nextcount = len(Replicas) + 1
        name = 'replica_' + str(nextcount)
        result = addReplicas(name, request.IP, request.port)
        if result == 0:
            if request.port != PR_details["port"]:
                addr=PR_details["IP"]+":"+str(PR_details["port"])
                with grpc.insecure_channel(addr) as channel:
                    stub = CommWithReplica_pb2_grpc.CommWithReplicaStub(channel)
                    request = CommWithReplica_pb2.Address(IP=request.IP, port=request.port)
                    status = stub.SendDetailsOfPR(request)
                    print(status)
            return CommWithRegistryServer_pb2.RegisterReplicaResponse(status="SUCCESS", primaryServerAddress=CommWithReplica_pb2.Address(IP=PR_details['IP'],port=PR_details['port']))
        else:
            return CommWithRegistryServer_pb2.RegisterReplicaResponse(status="FAIL", primaryServerAddress=None)


    def getReplicaList(self, request, context):
        print("REPLICA LIST REQUEST FROM " + request.address.IP + ":" + str(request.address.port))
        for replica in Replicas.keys():
            IP = Replicas[replica][0]
            port = Replicas[replica][1]
            yield CommWithRegistryServer_pb2.ReplicaListResponse(name=replica, address= CommWithReplica_pb2.Address(IP=IP, port=port))


def startRegistryServer():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    CommWithRegistryServer_pb2_grpc.add_CommWithRegistryServerServicer_to_server(CommWithRegistryServerServicer(), server)
    server.add_insecure_port('[::]:8888')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
