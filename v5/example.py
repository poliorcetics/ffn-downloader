"""
File: example.py
Author: BOURGET Alexis
License: see LICENSE.txt
App version: 5.1.3
File version: 1.1

Contains an example of the use of this app.
"""
import os
import worker as w


def example():
    os.chdir('example')
    path = os.getcwd()
    oc = w.OnComputer(path)

    oc.new_stories({
        path: ['https://www.fanfiction.net/s/3677636/1/Remember',
               'https://www.fanfiction.net/s/5522734/1/It-s-That-Time'],
        })

if __name__ == '__main__':
    example()
