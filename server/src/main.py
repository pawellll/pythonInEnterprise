#!/usr/bin/env python
from Server import Server as srv

if __name__ == '__main__':
    server = srv()
    server.listen()
