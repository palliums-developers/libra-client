#!/bin/sh

cd ..

git mv libra_client/canoser .
git mv libra_client/crypto .
git mv libra_client/error .
git mv libra_client/json_rpc .
git mv libra_client/move_core_types .
git mv libra_client/lbrtypes .
git mv libra_client/test .

git rm violas_client/canoser -rf
git rm violas_client/crypto  -rf
git rm violas_client/error -rf
git rm violas_client/json_rpc -rf
git rm violas_client/move_core_types -rf
git rm violas_client/lbrtypes -rf

rm violas_client/canoser -rf
rm violas_client/crypto -rf
rm violas_client/error -rf
rm violas_client/json_rpc -rf
rm violas_client/move_core_types -rf
rm violas_client/lbrtypes -rf

git rm violas_client/account.py -f
git rm violas_client/client.py -f
git rm violas_client/key_factory.py -f
git rm violas_client/methods.py -f
git rm violas_client/wallet_library.py -f
git rm violas_client/__init__.py -f







