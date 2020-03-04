# HTTP resolver - IPK project 1

* Author: **Juraj Lahvička**
* Subjcet: IPK project 1 2019/2020
* login: **xlahvi00**

## How to run resolver/server

a) `make run PORT=XXXX`

where `XXXX` is port number.

b) `python3 ./src/Main.py XXXX`

where `XXXX` is port number.

_**option a) is preffered.**_

## _[Main.py](src/Main.py)_

_[Main.py](src/Main.py)_ is file which cointains several functions. `run_server()` function checks for correct input of port number and creates TCP socket with address family IPv4. Next bind is used to associate the socket a specific network interface (in our case the localhost) and port number. It also keeps the socket/server alive. `run_socket(s)` at the beginning calls `listen()` method that enables the server to listen and `accept()` _"blocks"_ the server making the socket to be _"listening"_ and waiting for client to connect, establishing connection and getting client's socket. If no data are received it closes the connection. `run_socket(s)` function also calls various responses and other functions that handle or raise exceptions and parse data.

## _[Exceptions.py](src/IPKExceptions.py)_

File _[Exceptions.py](src/IPKExceptions.py)_ contains various specific exception classes.

## _[Response.py](src/Response.py)_

This class contains different response methods. It handles sending replies to client.

## Tests

Tests can be found in _src/tests_ directory. To run go to _src/tests/_ and run `./test.sh`. This scripts runs individual commands from *.in file, appends the results to *.out file and then uses diff to check for difference between *.out file and *.check file, where expected results are stored.

**Please keep in mind, that the ip address can change so the __*.check__ files needs to be updated.**

## How to terminate resolver/server

SIGINT => `ctrl+c` in terminal.
