# Molehole

 Websocket based, client-to-server cross-platform backdoor

![image](https://github.com/user-attachments/assets/e33c0b56-8def-4bcc-a05b-b87d28ba9a7f)

Molehole is a websocket SocketIO based backdoor which allows to connect to the websocket server as a client and execute commands.

# Installation

1. ```git clone git@github.com:alkhachatryan/molehole.git```
2. ```cd molehole```
3. ```cp .env.example .env``` and set the vars

### Requirements
A little bit python, docker and linux skills, then...

For development purposes it's required to have a docker on your machine so you are able to use a local "lab", because here you can use lightweight versions of popular distros such as debian, arch, ubuntu and so on. It's required to have a docker for testing purposes too - when you finish your contribution(development) you could run tests locally before on github in your PR.

**If you don't plan to develop and contribute, but just want to generate a backdoor** you required to have:
1. python 3.12 (didn't tested with older versions)
2. That's it

Then let's understand how could you start with development or just the backdoor creation process.

### Backdoor creation
The following command will generate a cross-platform backdoor file:
```pyinstaller server.spec```
Now you can put that file in a server you want to access and start the process. 
The better way - to run it in background AND create a cron operation on reboot or just simple ```./server```
Make sure that file is executable and ran by root (to have access to the whole server)

### Contribution workflow
If you want to contribute, develop and test locally with local "lab", start do the following:
1. ```sudo make start``` - it will up the project, pull all distros so you are allowed to test the backdoor on different machines and create the dist file shared across with all machines
2. ```sudo make serve_all_backdoors``` - will run backdoor on all machines - represents the network of infected machines where you have backdoor installed
3. ```sudo make connect_python_app``` - you'll connect the "client-machine" from which will connect to backdoors

#### Testing and development
From client container run:
```python src/client.py``` to run the client
```pytest``` to run all tests

**If you have changed anything and want a new dist file** - just run ```pyinstaller server.spec``` in python app container to generate a new dist file. Since that folder is a volume shared across all test-machines and client container there is nothing else to do, the pyisntaller will put the new binary in the right place.

If there is no any need in testing "lab", shut the backdoor process by:

```sudo make stop_all_backdoors```


To stop the project containers simply run:

```sudo make stop```

# How it works?
This is a simple SocketIO client-to-server stateful TCP connection which allows many connections to one server. 

You set the auth token, server host and port which should server use from .env file.
To prevent unauthenticated access to the server(through your backdoor), there is a auth token. Set it **BEFORE** backdoor generation and connect to the server using that token (check .env).

When all variables are set in .env run ```pyinstaller server.spec``` - your backdoor is ready, put it on a server and then connect to it with a client script: ```python src/client.py```

Run ```python src/client.py``` to see the usage (you may connect to another server by sy setting --host --port and --auth)

So by one client script you are allowed to connect to multiple servers. 

One server allows multiple connections and each connection has its own state i.e. current_path.

# What is testing lab?
Different OS/Distros docker-containerized with shared dist backdoor file which can be used for testing to be sure the backdoor works well and for local testing purposes. Check docker/_testing dir. Once new OS is supported by this backdoor - it will have its dockerfile for future testing operations.

# Tested Operating Systems/Distros

The generated backdoor binary file works well and tested on the following OS/Distros

| OS/Distro | Status |
|-----------|--------|
| Ubuntu    | ✅      |
| Debian    | ✅      |
| Arch      | ✅      |
| Fedora    | ✅      |
| Centos    | 🛑     |

There is a little issue related with centos, the process cannot be ran, so it marked as #1 TODO. There are more upcoming machines in test "lab" and supportable by this program.

# Features
1. Multiple connections to the server
2. State for each connection, i.e. current_path

Items from the table below will be added here over and over again 👇

# TODOs
1. Fix centos
2. Github testing workflow
3. Client dist binary file like for server - a cross-platform single-file client for cross-platform backdoors
4. Upload/Download files, so there is a way to change the file content
5. Install linter
6. Encryption/encoding of the source code of backdoor
7. Remote restart - restart the backdoor by a special command
8. Self-upgrade - send a command with a tag from github to pull, rebuild and restart
9. Set the proxy to connect to the server (default should be tor)
10. Self-replicating in a single machine or nearest machines by infection

# Open source tools/lib/packages used
- Socket.io
- Docker
- More in requirements.txt

# Versioning
Used semantic versioning - X.Y.Z where X is vendor, Y is major and Z is minor changes.

# License
MIT. Please see the [license file](https://github.com/alkhachatryan/molehole/blob/master/LICENSE "MIT") for more information.

# DISCLAIMER
This project is intended for testing and educational purposes only. By using this software, you agree that you are solely responsible for any actions you take and their consequences. Neither the authors of this project, contributors, nor the hosting platform (GitHub) are responsible for any misuse of this software.

You are strictly prohibited from using this software to engage in any illegal activity, including unauthorized access to computer systems, networks, or devices. This project is meant to be used by security professionals and researchers for penetration testing and learning, in environments where you have explicit permission to perform such activities. There is a testing "lab" special for you to test your skills.

Please respect the law and use responsibly.
