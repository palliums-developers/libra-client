#!/bin/bash

sudo docker stop violas-client
sudo docker rm violas-client
sudo docker image rm violas-client
sudo docker image build --no-cache -t violas-client .
sudo docker run --name=violas-client --network=host -itd violas-client