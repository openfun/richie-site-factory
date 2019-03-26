# ---- base image to inherit from ----
FROM python:3.7-stretch as base

# ---- back-end builder image ----
FROM base as back-builder

WORKDIR /builder

# Copy required python dependencies
COPY requirements/base.txt /builder/requirements.txt

# Upgrade pip to its latest release to speed up dependencies installation
RUN pip install --upgrade pip

RUN mkdir /install && \
    pip install --prefix=/install -r requirements.txt

# ---- final application image ----
FROM base

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

# The default command runs gunicorn WSGI server in the sandbox
CMD gunicorn -c /usr/local/etc/gunicorn/funmooc.py funmooc.wsgi:application

# Un-privileged user running the application
USER 10000
