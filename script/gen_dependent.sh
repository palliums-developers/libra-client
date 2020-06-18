#!/bin/sh

cd ..

git mv canoser/ libra_client/
git mv crypto/ libra_client/
git mv error/ libra_client/
git mv json_rpc/ libra_client/
git mv move_core_types/ libra_client/

cp libra_client violas_client -rf
git add violas-client/*

git mv test/ libra_client/test



