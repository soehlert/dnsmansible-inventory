#!/usr/bin/env python3
import os
import sys
import argparse

from configparser import ConfigParser

def local_connection():
    server = ""
    port = ""
    user = ""
    ssh_key = ""
    return server, port, user, ssh_key

# Turn off help, so we print all the options and not just the CLI flags
parser = argparse.ArgumentParser(add_help=False)

parser.add_argument("-l", "--local-conn", help="Use local connection; ie file is located on this host", default=False, action="store_true", dest='local_conn')
parser.add_argument("--password-auth", help="Use password authentication instead of keys", default=False, action="store_true", dest='password_auth')
parser.add_argument("--version", help="Print version", action="version", version="%(prog)s 0.1.0-alpha")
parser.add_argument("-c", "--config", help="Specify config file location", default="/tmp/test.conf", dest='conf_file')

args, remaining_argv = parser.parse_known_args()

conf_file = args.conf_file

conf = ConfigParser()
conf.read([conf_file])

if conf_file:
    hosts_file = conf.get('files', 'hosts_file')
    inventory = conf.get('files', 'inventory')
    if args.local_conn:
        local_conn = args.local_conn
        local_connection()
    else:
        server = conf.get('ssh', 'server')
        port = conf.get('ssh', 'port')
        user = conf.get('ssh', 'user')
        ssh_key = conf.get('ssh', 'ssh_key')
        local_conn = False
else:
    hosts_file = "/tmp/dns"
    inventory = "/tmp/inventory"
    local_connection()
    if args.local_conn:
        local_conn = args.local_conn
    else:
        local_conn = False

if args.password_auth:
    password_auth = args.password_auth
else:
    password_auth = False

# inherit options from previous parser, print script description with -h/--help
conf_parser = argparse.ArgumentParser(parents=[parser], description=__doc__)

conf_parser.add_argument("-f", "--file", help="Path of hosts file", dest='hosts_file')
conf_parser.add_argument("-i", "--inventory", help="Path of inventory file", dest='inventory')
conf_parser.add_argument("-s", "--server", help="Server to connect to (ip address)", dest='server')
conf_parser.add_argument("-p", "--port", help="SSH port to connect over", dest='port')
conf_parser.add_argument("-u", "--user", help="User to connect as", dest='user')
conf_parser.add_argument("-k", "--key", help="SSH key to use", dest='ssh_key')

cli_args = conf_parser.parse_args(remaining_argv)

if cli_args.hosts_file:
    hosts_file = cli_args.hosts_file
if cli_args.inventory:
    inventory = cli_args.inventory
if cli_args.server:
    server = cli_args.server
if cli_args.port:
    port = cli_args.port
if cli_args.user:
    user = cli_args.user

server, port, user, ssh_key = local_connection()

print(server)
print(port)
print(user)
print(ssh_key)
