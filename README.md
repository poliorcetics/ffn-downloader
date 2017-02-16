# FFN DOWNLOADER

## 0. Licence

**MIT License**

**Copyright (c) [2017] [BOURGET Alexis]**

**Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:**

**The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.**

**THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.**

**NOTE: In no way, shape or form any story downloaded with this Software (including, but not restricted to, the provided example) is the propriety of the author of this Software.**

## I. What does it do ?

1. It allows you to download any story from [fanfiction.net](https://www.fanfiction.net) (well, probably, it wasn't really tested that far, just with a few hundreds of them).
2. It also allows you to make statistics from a group a stories. (See below, **III. How to use it ?**, and the provided example)

All files created by this application should be `.html` files or `plain text` files. Furthermore, if correctly used (see `example.py` and the documentation for further precisions), you should always be able to tell what files and folders were created/modified/deleted by the application. DO NOT HESITATE TO ASK FOR TIPS AND INFORMATIONS, I will answer as soon and as clearly as I can.

## II. What do I need to make it work ?

In the current version (*v5.0*), you only need **Python 3.6 or higher**.

## III. How to use it ?

### III.A Usage in scripts

#### III.A.1: Downloading stories.

I will use two stories as examples:
 - [Past and Future King, 1 chapter, one universe](https://www.fanfiction.net/s/8956689/1/Past-and-Future-King),
 - [A New Chosen One, 16 chapters, crossover](https://www.fanfiction.net/s/9141379/1/A-New-Chosen-One).

Let's look at `example.py`:

```py
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
```

Now run `python3.6 example.py` in a shell or build it directly. Here's what you should obtain:
```text

---- FOLDER: example ----


________________________________________________________________________________

Title:      PAST AND FUTURE KING
From:       One Piece
Author:     Kitsune Foxfire
Url:        https://www.fanfiction.net/s/8956689/1/Past-and-Future-King
Tokens:     Rated: Fiction K - English - Gol D. Roger, Luffy - Words: 6,875 - Reviews: 112 - Favs: 1,611 - Follows: 352 - Published: 1/28/2013 - Status: Complete - id: 8956689

A pirate on the Grand Line should know to expect the unexpected, particularly when he is the King. Little did Roger know just how unexpected the results of calling out to a stranger in the fog would be. Who knew there were islands that could warp time? This meeting would always be one of his treasures. Oneshot


DONE -- Past-and-Future-King_infos.html
DOWNLOADED -- n° 1 /1
SAVED.

________________________________________________________________________________

Title:      A NEW CHOSEN ONE
From:       Star Wars + Harry Potter Crossover
Author:     ficfan11
Url:        https://www.fanfiction.net/s/9141379/1/A-New-Chosen-One
Tokens:     Rated: Fiction T - English - Romance/Adventure - [Padmé Amidala, Harry P.] - Chapters: 16 - Words: 46,832 - Reviews: 150 - Favs: 629 - Follows: 748 - Updated: 1/29/2014 - Published: 3/27/2013 - Status: In Progress - id: 9141379

A Harry Potter/Starwars fanfic. Lily sent Harry to a galaxy far far away to be trained in the ways of the Jedi and to escape the corrupt wizarding world. An adventure story with Harry as the Chosen One and a Harry/Padme romance.


DONE -- A-New-Chosen-One_infos.html
DOWNLOADED -- n° 01 /16
SAVED.
DOWNLOADED -- n° 02 /16
SAVED.
DOWNLOADED -- n° 03 /16
SAVED.
DOWNLOADED -- n° 04 /16
SAVED.
DOWNLOADED -- n° 05 /16
SAVED.
DOWNLOADED -- n° 06 /16
SAVED.
DOWNLOADED -- n° 07 /16
SAVED.
DOWNLOADED -- n° 08 /16
SAVED.
DOWNLOADED -- n° 09 /16
SAVED.
DOWNLOADED -- n° 10 /16
SAVED.
DOWNLOADED -- n° 11 /16
SAVED.
DOWNLOADED -- n° 12 /16
SAVED.
DOWNLOADED -- n° 13 /16
SAVED.
DOWNLOADED -- n° 14 /16
SAVED.
DOWNLOADED -- n° 15 /16
SAVED.
DOWNLOADED -- n° 16 /16
SAVED.

---- FOLDER: example ----

REGISTERED -- A New Chosen One                                             1/2
REGISTERED -- Past and Future King                                         2/2
DONE -- stats_example_2017-02-12.html
```

Note: `new_stories` (in `worker.py`, class `OnComputer`) also create the statistics, as you can see in the example above.

#### III.A.2: Updating stories.

This program also allows you to update stories instead of fully downloading them each time the author adds a new chapter.

See the `update_stories` method (in `worker.py`, class `OnComputer`).

### III.B: Usage directly in a shell.

This program can also be used directly in a shell.

Note: This functionality has only been tested on a Unix system, it may not work on a Windows environment.

Here is the help for this functionality:

```text
Help for program: worker.py

This program is a shell program designed to use the FFN DOWNLOADER application.

Command syntax: python3.6 worker.py [fld] [opt] [...]
                                    help

Options:
••••••••

  - [fld]: The folder in which the program will run. Can be a full path or a relative one.

  - [opt]: can take the following values

    ui: updates informations in multiple paths
        Syntax for [...]: [path1] [path2] ...

    ut: updates statistics in multiple paths
        Syntax for [...]: [renew] [main] [path1] [path2] ...

    us: updates stories in a single path
        Syntax for [...]: [path] [url1/id1] [url2/id2] ...

    ns: downloads new stories in a single path
        Syntax for [...]: [path] [url1/id1] [url2/id2] ...

  - help: displays this help

Note:
•••••

It is possible to use either URLs or IDs to identify stories. It is also possible to mix the two type of identification without a problem.

Example:
••••••••

(This examples assume you are in the correct directory to directly access worker.py)

This will download "https://www.fanfiction.net/s/1/1/Example-Url" in "ffn/", which is found in "/":

  python3.6 worker.py / ns ffn/ https://www.fanfiction.net/s/1/1/Example-Url

This command will accomplish exactly the same task:

  python3.6 worker.py / ns ffn/ 1
```

### III.C: Warning about statistics.

Statistics are made based on raw informations files (named following this pattern: `.{numerical_id}`) present in each story directory so if you don't update these informations for a long time, you may not have up-to-date statistics.

To solve this problem, the `update_stats` method (in `worker.py`, class `OnComputer`) accepts a `renew` parameter that you can set to `True` to update the informations of each story in the targeted directories.

## IV. Known Problems:

### IV.A: SSL Error with certificates.

If you get the following error message: **`[SSL: CERTIFICATE_VERIFY_FAILED]`** when trying to run the program for the first time, here's what to do:

1. Go to the directory where your copy of Python 3.6 is installed.
2. Run `Install Certificates.command`.

If it still doesn't work, I don't have a solution for you, sorry.
