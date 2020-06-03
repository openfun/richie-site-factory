# Richie site factory

This repository is a workbench for France Université Numérique to develop
themed sites based on [Richie](https://github.com/openfun/richie), the CMS
for Open Education.

## Prerequisite

First, make sure you have a recent version of Docker and [Docker
Compose](https://docs.docker.com/compose/install) installed on your laptop:

```
$ docker -v
  Docker version 19.03.10, build 9424aeaee9

$ docker-compose --version
  docker-compose version 1.25.5, build 8a1c60f6
```

## Getting started

First, you need to activate the site on which you want to work. We provide
a script that will list existing sites and let you choose one:

```bash
$ bin/activate
Select an available site to activate:
[1] demo (default)
[2] funmooc
Your choice: 2

# Check your environment with:
$ make info
RICHIE_SITE: funmooc
```

Once your environment is set, start the full project by running:

```bash
$ make bootstrap
```

This command builds the containers, starts the services and performs
database migrations. It's a good idea to use this command each time you are
pulling code from the project repository to avoid dependency-related or
migration-related issues.

Once the bootstrap phase is finished, you should be able to view the site at
[localhost:8080](http://localhost:8080)

> If you've just bootstrapped this project, you are probably planning to use AWS
> to store and distribute your media and static files. Luckily for you, we've
> cooked `terraform` scripts and a documentation for you! Read more about it:
> [docs/aws.md](./docs/aws.md)

## Usage

### Managing services

If you need to build or rebuild the containers, use:

```
$ make build
```

> Note that if the services are already running, you will need to stop them
> first and then restart them to fire up your newly built containers.

To start the development stack (_via_ Docker compose), use:

```
$ make run
```

You can inspect logs (in follow mode) with:

```
$ make logs
```

You can stop all services with:

```
$ make stop
```

If you need to stop and remove containers (to drop your database for example),
there is a command for that:

```
$ make down
```

### Housekeeping

Once the CMS is up and running, you can create a superuser account:

```
$ make superuser
```

To perform database migrations, use:

```
$ make migrate
```

You can create a basic demo site by running:

```
$ make demo-site
```

> Note that if you don't create the demo site and start from a blank CMS, you
> will get some errors requesting you to create some required root pages. So it
> is easier as a first approach to test the CMS with the demo site.

### Going further

To see all available commands, run:

```
$ make help
```

## Contributing

This project is intended to be community-driven, so please, do not hesitate to
get in touch if you have any question related to our implementation or design
decisions.

We try to raise our code quality standards and expect contributors to follow the
recommandations from our
[handbook](https://openfun.gitbooks.io/handbook/content).

## License

This work is released under the GNU Affero General Public License v3.0 (see
[LICENSE](./LICENSE)).
