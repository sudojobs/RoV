#!/bin/bash

# Start streaming video from Raspberry Pi camera module
raspivid -o - -t 0 -n -w 1280 -h 720 -fps 30 | \
ffmpeg -i - -vcodec copy -an -f rtsp -rtsp_transport tcp rtsp://localhost:8554/unicast
