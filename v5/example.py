"""
File: example.py
Author: BOURGET Alexis
License: see LICENSE.txt
App version: 5.0.2
File version: 1.0

Contains an example of the use of this app.
"""
import os
import worker as w


def example():
    os.chdir('example')
    path = os.getcwd()
    oc = w.OnComputer(path)

    oc.new_stories({
        path: ['https://www.fanfiction.net/s/8956689/1/Past-and-Future-King',
               'https://www.fanfiction.net/s/9141379/1/A-New-Chosen-One'],
        })

if __name__ == '__main__':
    example()
