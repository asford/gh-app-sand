FROM python:3.6-alpine

RUN pip install aiohttp-devtools

COPY requirements.txt /gh_app_sand/requirements.txt
RUN pip install -r /gh_app_sand/requirements.txt
