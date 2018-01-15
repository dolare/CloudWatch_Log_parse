#!/bin/bash
rm -rf deploy/target
mkdir -p deploy/target
pip install requests==2.18.4 -t deploy/target
cp *.py deploy/target/
cd deploy/target
zip -r ../deploy.zip .
cd ../..

