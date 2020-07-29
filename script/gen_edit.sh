#!/bin/sh

cd ..

sed -i "s/from violas_client.libra_client/from libra_client/g" `grep 'violas_client.libra_client' -rl ./violas_client`
sed -i "s/from violas_client.canoser/from canoser/g" `grep 'violas_client.canoser' -rl ./violas_client`
sed -i "s/from violas_client.crypto/from crypto/g" `grep 'violas_client.crypto' -rl ./violas_client`
sed -i "s/from violas_client.error/from error/g" `grep 'violas_client.error' -rl ./violas_client`
sed -i "s/from violas_client.json_rpc/from json_rpc/g" `grep 'violas_client.json_rpc' -rl ./violas_client`
sed -i "s/from violas_client.lbrtypes/from lbrtypes/g" `grep 'violas_client.lbrtypes' -rl ./violas_client`
sed -i "s/from violas_client.move_core_types/from move_core_types/g" `grep 'violas_client.move_core_types' -rl ./violas_client`


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

sed -i "s/from libra_client/from libra_client/g" `grep 'violas_client.libra_client' -rl ./*`

cd ./script





