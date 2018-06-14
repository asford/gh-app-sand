FROM python:3.6-alpine

COPY requirements.txt /gh_app_sand/requirements.txt
RUN pip install -r /gh_app_sand/requirements.txt

COPY . /gh_app_sand
WORKDIR /gh_app_sand
