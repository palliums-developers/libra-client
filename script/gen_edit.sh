#!/bin/sh

cd ..

git mv libra_client/test .
sudo rm libra_client -rf

git mv violas_client/canoser .
git mv violas_client/crypto  .
git mv violas_client/error .
git mv violas_client/exchange_client .
git mv violas_client/extypes .
git mv violas_client/json_rpc .
git mv violas_client/lbrtypes .
git mv violas_client/libra_client .
git mv violas_client/move_core_types .

cd ./script




