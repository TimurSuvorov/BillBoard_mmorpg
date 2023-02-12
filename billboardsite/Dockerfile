FROM python:3.8-slim

# set work directory
WORKDIR /billboardsite/

# set app-environment variables
ENV PYTHONDONTWRITEBYTECODE 1  # Prevents Python from writing pyc files to disc
ENV PYTHONUNBUFFERED 1  #Prevents Python from buffering stdout and stderr.

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /billboardsite/requirements.txt
RUN chmod +x /billboardsite/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /billboardsite/