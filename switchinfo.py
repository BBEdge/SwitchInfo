#!/usr/bin/env python3

import os, sys
import getpass
import tempfile
import argparse

from paramiko import SSHClient, AuthenticationException, SSHException, AutoAddPolicy


def switchinfo(conn, cmd, sw, outdir):
    stdin, stdout, stderr = conn.exec_command(cmd)
    stdin.close()

    swfile = os.path.join(outdir, sw)

    with open(swfile, 'w') as f:
        for item in stdout.readlines():
            f.write("%s\n" % item)


def connect(sw, user, pw, ssh_timeout=120):
    """actually connects to a switch.  returns a paramiko connection"""
    try:
        conn = SSHClient()
        conn.set_missing_host_key_policy(AutoAddPolicy())
        conn.connect(sw, username=user, password=pw, timeout=ssh_timeout)
    except AuthenticationException as e:
        print('')
        print('ATTENTION: Authentication failed, please verify your credentials')
        print('')
    except SSHException as e:
        print('')
        print('ATTENTION: Unable to establish SSH connection: %s' % e)
        print('')

    return conn


def main():
    global tempdir
    global user
    global pw
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', help='User name to connect switch')
    parser.add_argument('-c', '--command', help="Command to Collect, command must be escaped to ''")
    parser.add_argument('-f', '--finput', help='Select switch list file')
    args = parser.parse_args()

    user = args.user
    cmd = args.command

    if cmd is None or user is None or args.finput is None:
        print('')
        print('ATTENTION: Command Necessary ! Type -h')
        print('')
        print("EXAMPLE: switchinfo.py -u user -c 'find . -type f -exec grep -l 'word' {} +' -f switch.txt")
        print('')
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tempdir:
        pass
#        print('The created temporary directory is %s' % tempdir)

    '''set parameters'''
    currentdir = os.path.dirname(os.path.abspath(args.finput))
    switchfile = os.path.join(currentdir, args.finput)
    outdir = os.path.join(currentdir, tempdir)

    '''create dir to save collections'''
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    else:
        print('Creation of the directory %s failed' % outdir)

    '''get password to connect switches'''
    pw = getpass.getpass('Switch password for user %s: ' % user)

    '''read switch list and get info'''
    if os.path.exists(switchfile):
        with open(args.finput, 'r') as f:
            for sw in f.readlines():
                sw = sw.strip()
#            sw = ' '.join(f.readlines())
                conn = connect(sw, user, pw)
                switchinfo(conn, cmd, sw, outdir)
    else:
        print('ATTENTION: Command Necessary ! Type -h')
        exit(1)

    conn.close()

    print('')
    print('COMPLETE: See the collected data in the directory %s ' % tempdir)
    print('')


if __name__ == '__main__':
    main()
