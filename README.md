# Project 2: Distributed File System, Innopolis University Fall 2020
**Team**:

[Natalia Matrosova](https://github.com/MatrosovaTalia) - responsible for client and hosting

[Alisa Martyanova](https://github.com/AlisaMartyanova) - responsible for data and naming servers


## How to use the file system

run the following command in console: 
```dif
*docker run -e N_SERVER_HOST=3.16.46.152 -e N_SERVER_PORT=5550 -e -it  matrosovatalia/client:v1*
```
It will automatically connect to docker swarm with servers and launch the client. You will see the following:

![alt text](https://github.com/AlisaMartyanova/DistributedSystems/blob/master/term.png)

### You can type the following commands in client: 
```dif
send_f - send file from client to server

read_f - download file from server to client

mkdir_server - make directory on server

rmdir_server - remove directory from server

info - get information about file on server

ls_server - list directory on server

send_all - send all updates from client to server

rm_f_server - remove file from server
```
```
init - launches automatically when client runs and clears root directory (dfs) on client

init_size - get information about free size on client

create_f - create file on client

mkdir - make directory on client

rmdir - remove directory from client

rm_f - remove file from client

ls - list directory on client

cd - change directory on client

mv - move file from one directory to another on client

cp - make copy of file

help - list all possible commands
```

**Links to dockerhub:**
[storage server](https://hub.docker.com/repository/docker/matrosovatalia/storage-server), [name server](https://hub.docker.com/repository/docker/matrosovatalia/nameserver), [client](https://hub.docker.com/repository/docker/matrosovatalia/client)

## Architectural Diagram

![alt text](https://github.com/AlisaMartyanova/DistributedSystems/blob/master/architecture_diagram.png)

## Description of communication protocols
As main communication protocol we used the **Hypertext Transfer Protocol (HTTP)** - an application-level TCP/IP based protocol. 

**Client**

The HTTP client sends a request to the server in the form of a request method, URI, and protocol version, followed by a MIME-like message containing request modifiers, client information, and possible body content over a TCP/IP connection.

**Server**

The HTTP server responds with a status line, including the message's protocol version and a success or error code, followed by a MIME-like message containing server information, entity meta information, and possible entity-body content.
