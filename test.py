#!/usr/bin/env python3

import os


def main():
    switchfile = 'switch.txt'
    if os.path.exists(switchfile):
        with open(switchfile, 'r') as f:
            for sw in f.readlines():
                sw = sw.strip()
                print(sw)

    '''delete empty directory'''
#    if len(os.listdir(tempdir)) == 0:
#        try:
#            os.rmdir(tempdir)
#        except OSError as e:
#            print('Error while deleting directory %s ', (tempdir, e))


if __name__ == '__main__':
    main()