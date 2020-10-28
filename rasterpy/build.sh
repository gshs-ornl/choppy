#!/usr/bin/env bash
if [ $# -eq 0 ]; then
	BUILD_VERSION=0.1.2
else
	BUILD_VERSION=$1
fi
if [ "$BUILD_VERSION" == "" ]; then
	BUILD_VERSION=0.1.2
fi
LOCAL_NAME=rasterpy
REMOTE_NAME=code.ornl.gov:4567/6ng/choppy-lite/rasterpy
DOCKERFILE="$HOME/dev/choppy-lite/rasterpy/Dockerfile"
CONTEXT="$HOME/dev/choppy-lite/rasterpy"
docker build -t $LOCAL_NAME:latest -t $LOCAL_NAME:$BUILD_VERSION \
	-t $REMOTE_NAME:latest -t $REMOTE_NAME:$BUILD_VERSION \
	-f $DOCKERFILE $CONTEXT
docker push $REMOTE_NAME:latest
docker push $REMOTE_NAME:$BUILD_VERSION
