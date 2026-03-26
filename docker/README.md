# Dockerfiles for PostgreSQL with PGDG RPM Packages

**Devrim Gündüz** \<devrim@gunduz.org\>

---

## Contents

1. [Introduction](#1-introduction)
2. [Available Dockerfiles](#2-available-dockerfiles)
3. [Building an image from the Dockerfile](#3-building-an-image-from-the-dockerfile)
4. [Running the PostgreSQL server container](#4-running-the-postgresql-server-container)
5. [Connecting to the PostgreSQL server container](#5-connecting-to-the-postgresql-server-container)
6. [SSH into the container](#6-ssh-into-the-container)
7. [Further information resource](#7-further-information-resource)

---

## 1) Introduction

This document explains the layout of the container images for PostgreSQL,
based on PGDG RPMs, and documents the build and run procedures.

PostgreSQL YUM Repository Project provides Dockerfiles for the latest
Fedora, Red Hat UBI, Rocky Linux and AlmaLinux distributions. More may/will come later.

The examples below use `podman` as the primary command. `podman` is a
daemonless, rootless-capable OCI container engine and the recommended tool
on Fedora and RHEL-based systems. Every command works identically with
`docker` — simply substitute `podman` with `docker`.

---

## 2) Available Dockerfiles

| Dockerfile | Base OS | PostgreSQL |
|---|---|---|
| `Dockerfile-Fedora43-PG18` | Fedora 43 | PostgreSQL 18 |
| `Dockerfile-RHEL-UBI-PG18` | Red Hat UBI 8 minimal | PostgreSQL 18 |
| `Dockerfile-RockyLinux10-PG18` | Rocky Linux 10 | PostgreSQL 18 |
| `Dockerfile-AlmaLinux10-PG18` | AlmaLinux | PostgreSQL 18 |

---

## 3) Building an image from the Dockerfile

After downloading the suitable Dockerfile, rename it to `Dockerfile`, then
run this command to build an image:

```bash
podman build -t pgdg_postgresql .

# docker equivalent:
docker build -t pgdg_postgresql .
```

---

## 4) Running the PostgreSQL server container

After creating the image, run it in the background:

```bash
podman run -d -P --name pg_yum_test pgdg_postgresql

# docker equivalent:
docker run -d -P --name pg_yum_test pgdg_postgresql
```

To run the image in the foreground:

```bash
podman run --rm -P --name pg_yum_test pgdg_postgresql

# docker equivalent:
docker run --rm -P --name pg_yum_test pgdg_postgresql
```

---

## 5) Connecting to the PostgreSQL server container

There are two ways to connect to the PostgreSQL server container:

### a) Using a shared network

Create a named network and attach both the server and the client container
to it. The `--link` flag is deprecated and should no longer be used.

```bash
podman network create pgnet
podman run -d -P --name pg_yum_test --network pgnet pgdg_postgresql
podman run --rm -it --network pgnet pgdg_postgresql bash
$ psql -h pg_yum_test -p 5432 -d docker -U docker --password

# docker equivalents:
docker network create pgnet
docker run -d -P --name pg_yum_test --network pgnet pgdg_postgresql
docker run --rm -it --network pgnet pgdg_postgresql bash
$ psql -h pg_yum_test -p 5432 -d docker -U docker --password
```

### b) Connecting from your host system

Assuming you have the `postgresql18` packages installed, you can use the
host-mapped port to connect. First, find the mapped port:

```bash
podman ps

# docker equivalent:
docker ps
```

Example output:

```
CONTAINER ID  IMAGE             COMMAND                 CREATED        STATUS        PORTS                    NAMES
fe9158def36b  pgdg_postgresql   "/usr/pgsql-18/bin/p"  1 minute ago   Up 1 minute   0.0.0.0:32773->5432/tcp  pg_yum_test
```

In this example, `32773` is the host-side port mapped to `5432` inside the
container. Connect to the instance by:

```bash
psql -h localhost -p 32773 -d docker -U docker --password
```

> **Note:** You may need to replace `localhost` with the host address on some platforms.

If everything goes normally, you should see the psql prompt.

---

## 6) SSH into the container

The recommended way to get a shell inside a running container is with
`podman exec` / `docker exec`, which does not require an SSH server inside
the container:

```bash
podman exec -it pg_yum_test bash

# docker equivalent:
docker exec -it pg_yum_test bash
```

If you specifically need SSH access, install and configure `openssh-server`
inside the container. The easiest approach is to add the following to your
`Dockerfile` before the `USER postgres` line:

```dockerfile
# Install and configure SSH server
RUN dnf -q -y install openssh-server && \
    ssh-keygen -A && \
    echo "root:pgdg" | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

EXPOSE 22
```

Then start the container with port 22 mapped to a host port, for example 2222:

```bash
podman run -d -p 2222:22 -P --name pg_yum_test pgdg_postgresql /usr/sbin/sshd -D

# docker equivalent:
docker run -d -p 2222:22 -P --name pg_yum_test pgdg_postgresql /usr/sbin/sshd -D
```

Connect from your host:

```bash
ssh -p 2222 root@localhost
```

> **Security note:** Enabling SSH with password authentication is convenient
> for local testing but is not recommended for production use. Prefer
> key-based authentication and restrict `PermitRootLogin` accordingly.

---

## 7) Further information resource

More information is available at <https://yum.postgresql.org>.

Please help make these images better — let us know if you find problems,
or better ways of doing things. You can reach us by e-mail at
<pgsql-pkg-yum@postgresql.org> or create an issue at the issue tracker at
<https://github.com/pgdg-packaging/pgdg-rpms/issues/new>
