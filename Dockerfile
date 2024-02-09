FROM python:3.11.7-alpine3.19
LABEL maintainer="mdarmaan13"

# This is to prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Copy the requirements file to the temp directory
COPY ./requirements.txt /tmp/requirements.txt
#*************************IMPORTANT************************
#The RUN command executes these commands at build time, not at runtime. The working directory does not affect these commands because absolute paths are used.



# The following commands are executed in the container
#python -m venv /py creates a virtual environment in the /py directory
# /py/bin/pip install --upgrade pip upgrades pip to the latest version
# /py/bin/pip install -r /tmp/requirements.txt installs the dependencies listed in the requirements.txt file . This installs the dependencies in the virtual environment because we specified the path to the pip executable in the virtual environment
# rm -rf /tmp removes the /tmp directory and its contents because we no longer need it and make it lightweight

# The adduser command creates a new user named appuser. The --disabled-password flag prevents the creation of a password for the user. The --no-create-home flag prevents the creation of a home directory for the user. The appuser user is created to run the application in the container. This is a security best practice. The user is not created with root privileges, so it cannot modify the system files in the container. The user is also not created with a home directory, so it cannot store files in the container. This is a security best practice. The user is created to run the application in the container

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    adduser \
    --disabled-password \
    --no-create-home \
    appuser


# Copying the app directory to the container in the /app directory
COPY ./app app

WORKDIR /app

EXPOSE 8000

# It add Path in the linux environment such that we can run the python commands without specifying the path to the python executable in the virtual environment , all the commands we run in the container are executed in the virtual environment
ENV PATH="/py/bin:$PATH"

# The USER command sets the user to appuser. This means that all the commands that follow are executed as the appuser user.
USER appuser