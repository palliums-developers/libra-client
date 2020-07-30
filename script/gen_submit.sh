#!/bin/sh

cd ..

cp canoser/ violas_client/ -rf
cp crypto/ violas_client/ -rf
cp error/ violas_client/ -rf
cp json_rpc/ violas_client/ -rf
cp lbrtypes/ violas_client/ -rf
cp libra_client/ violas_client/ -rf
cp move_core_types/ violas_client/ -rf

git mv exchange_client/ violas_client/
git mv extypes/ violas_client/
git mv bank_client/ violas_client/
git mv banktypes/ violas_client/
git mv vlstypes/ violas_client/

git mv canoser/ libra_client/
git mv crypto/ libra_client/
git mv error/ libra_client/
git mv json_rpc/ libra_client/
git mv lbrtypes/ libra_client/
git mv move_core_types/ libra_client/

git add violas_client/

sed -i "s/from libra_client/from violas_client.libra_client/g" `grep "from libra_client" -rl ./violas_client`
sed -i "s/from bank_client/from violas_client.bank_client/g" `grep "from bank_client" -rl ./violas_client`
sed -i "s/from banktypes/from violas_client.banktypes/g" `grep "from banktypes" -rl ./violas_client`
sed -i "s/from exchange_client/from violas_client.exchange_client/g" `grep "from exchange_client" -rl ./violas_client`
sed -i "s/from extypes/from violas_client.extypes/g" `grep "from extypes" -rl ./violas_client`
sed -i "s/from vlstypes/from violas_client.vlstypes/g" `grep "from vlstypes" -rl ./violas_client`

sed -i "s/from canoser/from violas_client.canoser/g" `grep "from canoser" -rl ./violas_client`
sed -i "s/from canoser/from libra_client.canoser/g" `grep "from canoser" -rl ./libra_client`

sed -i "s/from crypto/from violas_client.crypto/g" `grep "from crypto" -rl ./violas_client`
sed -i "s/from crypto/from libra_client.crypto/g" `grep "from crypto" -rl ./libra_client`

sed -i "s/from error/from violas_client.error/g" `grep "from error" -rl ./violas_client`
sed -i "s/from error/from libra_client.error/g" `grep "from error" -rl ./libra_client`

sed -i "s/from json_rpc/from violas_client.json_rpc/g" `grep "from json_rpc" -rl ./violas_client`
sed -i "s/from json_rpc/from libra_client.json_rpc/g" `grep "from json_rpc" -rl ./libra_client`

sed -i "s/from lbrtypes/from violas_client.lbrtypes/g" `grep "from lbrtypes" -rl ./violas_client`
sed -i "s/from lbrtypes/from libra_client.lbrtypes/g" `grep "from lbrtypes" -rl ./libra_client`

sed -i "s/from move_core_types/from violas_client.move_core_types/g" `grep "from move_core_types" -rl ./violas_client`
sed -i "s/from move_core_types/from libra_client.move_core_types/g" `grep "from move_core_types" -rl ./libra_client`


sed -i "s/move_core_types.language_storage.TypeTag/violas_client.move_core_types.language_storage.TypeTag/g" `grep "move_core_types.language_storage.TypeTag" -rl ./violas_client`
sed -i "s/move_core_types.language_storage.TypeTag/libra_client.move_core_types.language_storage.TypeTag/g" `grep "move_core_types.language_storage.TypeTag" -rl ./libra_client`

sed -i "s/move_core_types.language_storage.StructTag/violas_client.move_core_types.language_storage.StructTag/g" `grep "move_core_types.language_storage.StructTag" -rl ./violas_client`
sed -i "s/move_core_types.language_storage.StructTag/libra_client.move_core_types.language_storage.StructTag/g" `grep "move_core_types.language_storage.StructTag" -rl ./libra_client`

cd ./script
