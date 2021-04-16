ARG BASE_IMG=tensorflow/tensorflow:2.1.0-py3-jupyter
#ARG BASE_IMG=python:3.8

FROM $BASE_IMG
# @note: args don't last past a FROM command. Hence, they must be put after FROM.
#        typically, these are to be filled in by your CI/CD system.
ARG PROJECT_ROOT="."
ARG PROJECT_MOUNT_DIR="/inference"

# We avoid running docker as root at construction.
# @note: if you mount your host filesystem on docker
#        changes you make to the filesystem mounted on docker
#        apply to your host filesystem.
#        e.g. if you delete a file X, it will be deleted on your host as well.
#        by creating a separate user and assign a limited permission to it,
#        we avoid the catastrophic situation. by default, docker runs as root!
# https://stackoverflow.com/questions/27701930/add-user-to-docker-container
# https://medium.com/jobteaser-dev-team/docker-user-best-practices-a8d2ca5205f4
# ARG USER_NAME="ml_deploy"
# RUN adduser --disabled-password --gecos '' $USER_NAME

# @note: this will create the path if not existing (=mkdir -p).
# ADD $PROJECT_ROOT $PROJECT_MOUNT_DIR

# change the workdir to $PROJECT_MOUNT_DIR
# @note: this will create the path if not existing (=mkdir -p).
WORKDIR /code/

# pip3 by default as the base image is python 3+
# @note: each docker RUN create a new "layer".
#        to avoid unnecessary networking/computations
#        it's best practice to group commands
#        if they can be meaningfully and functionally grouped.

    #&& \ pip install .
RUN pip3 install tensorflow-text && \
    pip3 install  tfx==0.25.0 && \
    pip3 install boto3 && \
    pip3 install fastapi uvicorn

COPY . /code/

EXPOSE 8000
CMD ["python", "main.py"]
# set the default user
# USER $USER_NAME
