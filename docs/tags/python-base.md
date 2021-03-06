# python-base

[Back to overview](../index.md)

**Base image**: `alpine:3.12.3`  
**Full name**: `ludeeus/container:python-base`  
[View this on Docker Hub](https://hub.docker.com/r/ludeeus/container/tags?page=1&name=python-base)

## Environment variables

Variable | Value 
-- | --
`CONTAINER_TYPE` | python-base

## Alpine packages

Package | Version 
-- | --
`bash` | 5.0.17-r0
`ffmpeg-dev` | 4.3.1-r0
`gcc` | 9.3.0-r2
`git` | 2.26.2-r0
`libc-dev` | 0.7.2-r3
`libffi-dev` | 3.3-r2
`make` | 4.3-r0
`openssh` | 8.3_p1-r1
`openssl-dev` | 1.1.1i-r0
`py3-pip` | 20.1.1-r0
`python3-dev` | 3.8.5-r0
`python3` | 3.8.5-r0



***
<details>
<summary>Generated dockerfile</summary>

<pre>
FROM alpine:3.12.3

ENV CONTAINER_TYPE=python-base



RUN  \ 
    apk add --no-cache  \ 
        bash=5.0.17-r0 \ 
        ffmpeg-dev=4.3.1-r0 \ 
        gcc=9.3.0-r2 \ 
        git=2.26.2-r0 \ 
        libc-dev=0.7.2-r3 \ 
        libffi-dev=3.3-r2 \ 
        make=4.3-r0 \ 
        openssh=8.3_p1-r1 \ 
        openssl-dev=1.1.1i-r0 \ 
        py3-pip=20.1.1-r0 \ 
        python3-dev=3.8.5-r0 \ 
        python3=3.8.5-r0 \ 
    && ln -s /usr/bin/python3 /usr/bin/python \ 
    && rm -rf /var/cache/apk/* \ 
    && rm -fr /tmp/* /var/{cache,log}/*




</pre>

<i>This is a generated version of the context used while building the container, some of the labels will not be correct since they use information in the action that publishes the container</i>
</details>
