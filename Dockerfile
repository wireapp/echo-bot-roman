# ----------- download python dependencies -----------
FROM python:3.10-alpine AS install
# ref: https://pipenv.pypa.io/en/latest/basics/#pipenv-and-docker-containers
# install pipenv
RUN pip install --user pipenv

# Tell pipenv to create venv in the current directory
ENV PIPENV_VENV_IN_PROJECT=1

WORKDIR /app
# copy dependencies
COPY Pipfile* ./

# install dependencies
RUN /root/.local/bin/pipenv sync

# ----------------------Final image-------------------
FROM python:3.10-alpine AS image

# copy app
COPY . /app/

# copy dependencies
RUN mkdir -v /app/.venv
COPY --from=install /app/.venv/ /app/.venv/

WORKDIR /app

# create version file
ARG release_version=development
ENV RELEASE_FILE_PATH=/app/release.txt
RUN echo $release_version > $RELEASE_FILE_PATH

ENV JSON_LOGGING='true'

# start app
EXPOSE 8080
# --log-level WARNING is just for first 3 gunicorn lines as it can not log in jsons
CMD /app/.venv/bin/gunicorn --workers=4 --bind 0.0.0.0:8080 --log-level WARNING app:app