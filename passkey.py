#!/usr/bin/python3

import sys

import bash

USAGE = """
    print - Print out the current password DB
    clear - Clear the current password DB (Be careful if you do this!)
    status - Print some status characteristics
    insert {key} {password} - insert "password" under the ownership of "key"
    delete {key} | delete {password} - deletes entries matching either key or password
"""

DEFAULT_FILE_NAME = '.psk'

def usage():
    """Print out usage information"""
    print("%s" % USAGE)

def read_file(master_password, filename=""):
    """Opens filename and returns it as a string"""
    bash.run('touch "%s" ]' % (filename,), False)
    ret = bash.run('cat "%s" | aescrypt -d -p "%s" -o - -' \
            % (master_password, filename,), False)
    if ret.return_code_success():
        return ret.stdout()
    else:
        print("Decryption failed.  Did you enter the wrong master password?")
        return ""


def write_file(contents, master_password, filename=DEFAULT_FILE_NAME):
    """Writes the content to filename"""
    ret = bash.run('echo "%s" | aescrypt -e -p "%s" -o "$HOME/%s" -' \
            % (contents, master_password, filename,), False)
    if not ret.return_code_success():
        print('saving master keyfile failed!: %s' % (ret.stderr(),))

if __name__ == '__main__':
    usage()
    sys.exit(0)
