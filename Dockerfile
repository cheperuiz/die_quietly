FROM ubuntu:latest
LABEL authors="chepe"

ENTRYPOINT ["top", "-b"]