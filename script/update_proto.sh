#!/bin/sh
git clone -b testnet https://github.com/libra/libra.git
cd libra

rm ../../proto/*.proto
find . -name *.proto | xargs cp -t ../../proto/
cd ../../
rpl "shared/mempool_status" "mempool_status" proto/mempool.proto

cd ./scripts/
./generate_protobuf.sh
