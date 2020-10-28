#!/usr/bin/env bash
BUILD_VERSION=$1
if [ "$BUILD_VERSION" == "" ]; then
	BUILD_VERSION=0.1.2
fi
LOCAL_NAME=choppy-lite
REMOTE_NAME=code.ornl.gov:4567/6ng/choppy-lite/choppy-lite
DOCKERFILE="$HOME/dev/choppy-lite/Dockerfile"
CHOPPY_CONTEXT="$HOME/dev/choppy-lite"
PASSIVEFILE="$HOME/dev/choppy-lite/Dockerfile[passive]"
docker build -t $LOCAL_NAME:latest -t $LOCAL_NAME:$BUILD_VERSION \
	-t $REMOTE_NAME:latest -t $REMOTE_NAME:$BUILD_VERSION -f $DOCKERFILE \
	$CHOPPY_CONTEXT
docker push $REMOTE_NAME:latest
docker push $REMOTE_NAME:$BUILD_VERSION
LOCAL_NAME=passive-choppy
REMOTE_NAME=code.ornl.gov:4567/6ng/choppy-lite/$LOCAL_NAME
docker build -t $LOCAL_NAME:latest -t $LOCAL_NAME:$BUILD_VERSION \
	-t $REMOTE_NAME:latest -t $REMOTE_NAME:$BUILD_VERSION -f $PASSIVEFILE \
	$CHOPPY_CONTEXT
docker push $REMOTE_NAME:latest
docker push $REMOTE_NAME:$BUILD_VERSION

