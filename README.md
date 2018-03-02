# FFN DOWNLOADER

## 0. Licence

**MIT License**

**Copyright (c) [2017-2018] [BOURGET Alexis]**

**Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:**

**The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.**

**THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.**

**NOTE: In no way, shape or form any story downloaded with this Software (including, but not restricted to, the provided example) is the propriety of the author of this Software.**

## I. What does it do ?

1. It allows you to download any story from [fanfiction.net](https://www.fanfiction.net) (well, probably, it wasn't really tested that far, just with a few millions of them).
2. It also allows you to make statistics from a group a stories. (See below, **III. How to use it ?**, and the provided example)

All files created by this application should be `.html` files or `plain text` files. Furthermore, if correctly used (see `example.py` and the documentation for further precisions), you should always be able to tell what files and folders were created/modified/deleted by the application. DO NOT HESITATE TO ASK FOR TIPS AND INFORMATIONS, I will answer as soon and as clearly as I can.

## II. What do I need to make it work ?

In the current version (*5*), you only need **Python 3.6 or higher**.

## III. How to use it ?

### III.A Usage in scripts

#### III.A.1: Downloading stories.

I will use two stories as examples:
 - [Remember, 1 chapter, one universe](https://www.fanfiction.net/s/3677636/1/Remember),
 - [It's that time, 2 chapters, one universe](https://www.fanfiction.net/s/5522734/1/It-s-That-Time).

Let's look at `example.py`:

```py
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
```

Now run `python3.6 example.py` in a shell or build it directly. Here's what you should obtain:
```text

---- FOLDER: example ----


________________________________________________________________________________

Title:      REMEMBER
From:       Harry Potter
Author:     Marquis Black
Url:        https://www.fanfiction.net/s/3677636/1/Remember
Tokens:     Rated: Fiction M - English - Drama/Angst - Words: 1,188 - Reviews: 9 - Favs: 27 - Follows: 13 - Published: 7/24/2007 - Status: Complete - id: 3677636

Enter the mind of one of the left behind those who, while others march off to war, stay at home. What do they think of when the war ends? Rating for allusions to suggestive situations. AU. Oneshot.


DONE -- Remember_infos.html
DOWNLOADED -- n° 1 /1
SAVED.

________________________________________________________________________________

Title:      IT'S THAT TIME
From:       One Piece
Author:     elvenarchress
Url:        https://www.fanfiction.net/s/5522734/1/It-s-That-Time
Tokens:     Rated: Fiction K+ - English - Humor - Straw Hats P., Luffy - Chapters: 2 - Words: 2,861 - Reviews: 114 - Favs: 734 - Follows: 148 - Updated: 12/16/2009 - Published: 11/20/2009 - Status: Complete - id: 5522734

AU: gender reversed!Straw Hats When it's that time of the month, a new Marine recruit learns just why they should stay far, far away...Full List UP!


DONE -- It-s-That-Time_infos.html
DOWNLOADED -- n° 1 /2
SAVED.
DOWNLOADED -- n° 2 /2
SAVED.

---- FOLDER: example ----

REGISTERED -- It's That Time                                                        1 / 2
REGISTERED -- Remember                                                              2 / 2
DONE -- stats_example_2017-10-25.html
```

Note:
- `new_stories` (in `worker.py`, class `OnComputer`) also create the statistics, as you can see in the example above.
- The numbers may be different because time has passed since I did this example. It is to be expected and is perfectly normal.

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
        Syntax for [...]: [renew] [path1] [path2] ...

    us: updates stories in a single path
        Syntax for [...]: [path] [url1/id1] [url2/id2] ...

    ns: downloads new stories in a single path
        Syntax for [...]: [path] [url1/id1] [url2/id2] ...

  - help: displays this help

Note:
•••••

- It is possible to use either URLs or IDs to identify stories. It is also possible to mix the two type of identification without a problem.
- The main stats file will never be updated if you have one. That is because it can not find all story folders so to avoid errors in counting them you will have to do it yourself separately if you wish to update it.

Example:
••••••••

(This examples assume you are in the correct directory to directly access worker.py)

This will download "https://www.fanfiction.net/s/1/1/Example-Url" in "ffn/", which is found in "/":

  python3.6 worker.py / ns ffn/ https://www.fanfiction.net/s/1/1/Example-Url

This command will accomplish exactly the same task:

  python3.6 worker.py / ns ffn/ 1
```

### III.C: How to read a story.

#### III.C.1: Selecting a story.

To select a story, you should first open your stats file if you have more than a few stories: it will help you choose by giving you informations about the numbers of chapters and words, the ratio words per chapter (on average), the universe and the summary provided by the author of the story.

#### III.C.2: The informations page.

Once you have selected your story, if you have done it using a stats file, you will find yourself on the informations page. It gives you all the informations which could be found from the site.

For example, you can go to the first chapter of the story using the URL provided or go to the author's page.

Go down the page to find the chapters list, select a chapter and start reading.

#### III.C.3: Reading a story.

You have chosen to start this story but you see many things that are not the story itself on the page.

Why ?

First, the link that is the story's title brings back to the informations page. You can use it to jump chapters for example. This link exists at both the top and the bottom of each chapter.

Then you will see the author's name as a link. It is a link to their page on fanfiction.net. Again, this link can be found at the top and the bottom of each chapter.

At the top of each chapter (except the first one) you will find a *Previous* link with the precedent chapter's title next to it. Use it to go back a chapter.

At the bottom of each chapter (except the last one) you will a *Next* link, with the next chapter's title next to it. Use to go further in the story, one chapter at a time.

### III.D: Warning about statistics.

Statistics are made based on raw informations files (named following this pattern: `.{numerical_id}`) present in each story directory so if you don't update these informations for a long time, you may not have up-to-date statistics.

To solve this problem, the `update_stats` method (in `worker.py`, class `OnComputer`) accepts a `renew` parameter that you can set to `True` to update the informations of each story in the targeted directories.

## IV. Known Problems:

### IV.A: SSL Error with certificates.

If you get the following error message: **`[SSL: CERTIFICATE_VERIFY_FAILED]`** when trying to run the program for the first time, here's what to do:

1. Go to the directory where your copy of Python 3.6 is installed.
2. Run `Install Certificates.command`.

This problem was present in the very first release of Python 3.6, if you've got an up-to-date version, you shouldn't have any problem.

If it still doesn't work, I don't have a solution for you, sorry.
