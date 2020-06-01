# ----------- download python dependencies -----------
FROM python:3.7-alpine AS install
# install pipenv
RUN pip install pipenv

WORKDIR /app
# copy dependencies
COPY Pipfile* ./

# install dependencies
RUN pipenv lock -r > requirements.txt
RUN pip install -r requirements.txt

# ----------------------Final image-------------------
FROM python:3.7-alpine AS image
# copy dependencies
COPY --from=install /usr/local /usr/local

# copy app
COPY . /app/
WORKDIR /app

# create version file
ARG release_version=development
ENV RELEASE_FILE_PATH=/app/release.txt
RUN echo $release_version > $RELEASE_FILE_PATH

ENV JSON_LOGGING='true'

# start app
EXPOSE 8080
# --log-level WARNING is just for first 3 gunicorn lines as it can not log in jsons
CMD gunicorn --workers=4 --bind 0.0.0.0:8080 --log-level WARNING app:app