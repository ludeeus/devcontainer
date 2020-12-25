ARG BUILD_FROM
FROM ${BUILD_FROM}

COPY ./include /include

ARG OS_VARIANT
RUN \
    sh /include/install/base/${OS_VARIANT}.sh \
    && bash /include/cleanup/build.sh