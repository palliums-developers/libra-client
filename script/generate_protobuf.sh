#!/bin/sh

python3 -m grpc_tools.protoc \
    -I ../proto \
    --python_out=../violas/proto \
    --grpc_python_out=../violas/proto \
    ../proto/*.proto
