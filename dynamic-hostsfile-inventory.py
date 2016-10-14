#!/usr/bin/env python3
import os
import sys
import signal
import argparse

from IPy import IP
from configparser import ConfigParser

def die():
    """ Function to kill program on error """
    sys.exit(0)

def test_bool(bool_var):
    """ Test if a boolean is true and exists """
    try:
        bool_var
    except NameError:
        print("Failure with bool_var")
    else:
        return True

def test_file(file_name):
    """ Test to see if file exists/can be accessed """
    if os.path.isfile(file_name):
        return True
    else:
        print("\nERROR: Cannot access {}\nPossible Issues:\n\tDoes it exist?\n\tDo you have permissions to read it?\n".format(file_name))
        die()

def local_connection():
    """ Set ssh values all to nothing since we don't need them """
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
parser.add_argument("-c", "--config", help="Specify config file location", default="example.conf", dest='conf_file')

args, remaining_argv = parser.parse_known_args()

conf_file = args.conf_file

conf = ConfigParser()
conf.read([conf_file])

if conf_file:
    hosts_file = conf.get('files', 'hosts_file')
    inventory = conf.get('files', 'inventory')
    if args.local_conn:
        local_conn = args.local_conn
        server, port, user, ssh_key = local_connection()
    else:
        server = conf.get('ssh', 'server')
        try:
            port = conf.getint('ssh', 'port')
        except ValueError:
            print("\nERROR: Conf file argument 'port': invalid int value: '{}'\n".format(conf.get('ssh', 'port')))
            die()
        user = conf.get('ssh', 'user')
        ssh_key = conf.get('ssh', 'ssh_key')
        local_conn = False
else:
    hosts_file = "/tmp/dns"
    inventory = "/tmp/inventory"
    server, port, user, ssh_key = local_connection()
    if args.local_conn:
        local_conn = args.local_conn

if args.password_auth:
    password_auth = args.password_auth
else:
    password_auth = False

# inherit options from previous parser, print script description with -h/--help
conf_parser = argparse.ArgumentParser(parents=[parser], description=__doc__)

conf_parser.add_argument("-f", "--file", help="Path of hosts file", dest='hosts_file')
conf_parser.add_argument("-i", "--inventory", help="Path of inventory file", dest='inventory')
conf_parser.add_argument("-s", "--server", help="Server to connect to (ip address)", dest='server') conf_parser.add_argument("-p", "--port", help="SSH port to connect over", type=int, dest='port')
conf_parser.add_argument("-u", "--user", help="User to connect as", dest='user')
conf_parser.add_argument("-k", "--key", help="SSH key to use", dest='ssh_key')

cli_args = conf_parser.parse_args(remaining_argv)

# This seems iffy
for arg, value in vars(cli_args).items():
    if value:
        exec(arg + '=value')


if __name__ == '__main__':
    if test_bool(local_conn):
        print("local: {}".format(local_conn))
    if test_bool(password_auth):
        print("password: {}".format(password_auth))

    print("conf: {}".format(conf_file))

    if test_file(hosts_file):
        print("hosts: {}".format(hosts_file))
    if test_file(inventory):
        print("inventory: {}".format(inventory))

    if not local_conn:
        print("user: {:s}".format(user))
        if test_file(ssh_key):
            print("ssh key: {}".format(ssh_key))

        try:
            print("port: {:d}".format(port))
        except TypeError:
            print("Port should be an integer")
            die()

        try:
            print("server: {}".format(IP(server)))
        except:
            if server:
                print("\nERROR: Not a valid IP address\n")
                die()

