#!/bin/sh

cd ..

git mv libra_client/test .
sudo rm libra_client -rf

git mv violas_client/bank_client .
git mv violas_client/banktypes .
git mv violas_client/canoser .
git mv violas_client/crypto  .
git mv violas_client/error .
git mv violas_client/exchange_client .
git mv violas_client/extypes .
git mv violas_client/json_rpc .
git mv violas_client/lbrtypes .
git mv violas_client/libra_client .
git mv violas_client/move_core_types .
git mv violas_client/vlstypes .

sed -i "s/from violas_client.libra_client/from libra_client/g" `grep 'violas_client.libra_client' -rl ./*`

cd ./script





