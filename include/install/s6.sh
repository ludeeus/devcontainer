#!/usr/bin/env bash

# https://github.com/just-containers/s6-overlay

echo -e "\\033[0;34mRunning install script 's6'\\033[0m"

S6_VERSION="v2.1.0.2"
ARCH=$(uname -m)

if [ "$ARCH" == "armv7l" ]; then
    wget -q -nv -O /tmp/s6.tar.gz "https://github.com/just-containers/s6-overlay/releases/download/${S6_VERSION}/s6-overlay-armhf.tar.gz";
elif [ "$ARCH" == "aarch64" ]; then
    wget -q -nv -O /tmp/s6.tar.gz "https://github.com/just-containers/s6-overlay/releases/download/${S6_VERSION}/s6-overlay-aarch64.tar.gz";
elif [ "$ARCH" == "x86_64" ]; then
    wget -q -nv -O /tmp/s6.tar.gz "https://github.com/just-containers/s6-overlay/releases/download/${S6_VERSION}/s6-overlay-amd64.tar.gz";
fi

tar xzf /tmp/s6.tar.gz -C /
rm /tmp/s6.tar.gz