# Tanishk is the best
1. Download GRPC Stuff in a new venv:   https://grpc.io/docs/languages/python/quickstart/
2. To compile the proto: 
`python -m grpc_tools.protoc -I protos --python_out=protos --pyi_out=protos --grpc_python_out=protos protos/registryServer.proto`