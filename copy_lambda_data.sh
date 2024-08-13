#!/bin/bash

while true; do
    rsync -r xspadmin@164.54.106.69:/home/xspadmin/6idb/ /home/beams/USER6IDB/data/lambda/
    sleep 5;
done

