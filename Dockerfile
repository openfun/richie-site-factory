ARG NGINX_VERSION=1.18
ARG STATIC_ROOT=/data/static

# The ID of the user running in the container
ARG DOCKER_USER=10000

# ---- base image to inherit from ----
FROM python:3.7-stretch as base

# ---- front-end builder image ----
FROM node:10 as front-builder

# Copy frontend app sources
COPY ./src/frontend /builder/src/frontend

WORKDIR /builder/src/frontend

RUN yarn install --frozen-lockfile && \
    yarn sass-production

# ---- back-end builder image ----
FROM base as back-builder

WORKDIR /builder

# Copy required python dependencies
COPY requirements/base.txt /builder/requirements.txt

# Upgrade pip to its latest release to speed up dependencies installation
RUN pip install --upgrade pip

RUN mkdir /install && \
    pip install --prefix=/install -r requirements.txt

# ---- Core application image ----
FROM base as core

# Install gettext
RUN apt-get update && \
    apt-get install -y \
    gettext && \
    rm -rf /var/lib/apt/lists/*

# Copy installed python dependencies
COPY --from=back-builder /install /usr/local

# Copy runtime-required files
COPY ./src/backend /app/
COPY ./docker/files/usr/local/bin/entrypoint /usr/local/bin/entrypoint

# Copy distributed application's statics
COPY --from=front-builder /builder/src/backend/base/static/richie /app/base/static/richie

WORKDIR /app

# Gunicorn
RUN mkdir -p /usr/local/etc/gunicorn
COPY ./docker/files/usr/local/etc/gunicorn/funmooc.py /usr/local/etc/gunicorn/funmooc.py

# Give the "root" group the same permissions as the "root" user on /etc/passwd
# to allow a user belonging to the root group to add new users; typically the
# docker user (see entrypoint).
RUN chmod g=u /etc/passwd

# We wrap commands run in this container by the following entrypoint that
# creates a user on-the-fly with the container user ID (see USER) and root group
# ID.
ENTRYPOINT [ "/usr/local/bin/entrypoint" ]

# ---- Static files/links collector ----
FROM core as collector

ARG STATIC_ROOT

# Install rdfind
RUN apt-get update && \
    apt-get install -y \
    rdfind && \
    rm -rf /var/lib/apt/lists/*

# Collect static files
RUN python manage.py collectstatic --noinput
# Replace duplicated file by a symlink to decrease the overall size of the
# final image
RUN rdfind -makesymlinks true ${STATIC_ROOT}

# ---- Development image ----
FROM core as development

# Copy required python dependencies
COPY requirements/dev.txt /tmp/requirements.txt

# Install development dependencies
RUN pip install -r /tmp/requirements.txt

# Un-privileged user running the application
ARG DOCKER_USER
USER ${DOCKER_USER}

# Run django development server
CMD python manage.py runserver 0.0.0.0:8000

# ---- Production image ----
FROM core as production

ARG STATIC_ROOT

# Copy collected symlinks to static files
COPY --from=collector ${STATIC_ROOT}/staticfiles.json ${STATIC_ROOT}/

# Un-privileged user running the application
ARG DOCKER_USER
USER ${DOCKER_USER}

# The default command runs gunicorn WSGI server in the sandbox
CMD gunicorn -c /usr/local/etc/gunicorn/funmooc.py funmooc.wsgi:application

# ---- Nginx ----
FROM nginx:${NGINX_VERSION} as nginx

ARG STATIC_ROOT

RUN mkdir -p ${STATIC_ROOT}

COPY --from=collector ${STATIC_ROOT} ${STATIC_ROOT}
