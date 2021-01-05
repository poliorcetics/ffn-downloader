# MULTI-SITES FANFICTION DOWNLOADER

## 0. Licence

**MIT License**

**Copyright (c) [2017-2018] [BOURGET Alexis]**

**Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:**

**The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.**

**THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.**

**NOTE: Any story downloaded with the Software belongs to their legal owner.**

## Requirements

To make this program work you need to have **Python 3.6 or higher** installed with (most notably) the following modules: `tkinter`, `re`, `urllib` and `logging`. Those are part of the packages found at [python.org](https://www.python.org) by default and as such you shouldn't need to install any additional packages.

## I. What does it do ?

This programs provides a GUI (graphical user interface) which allows you to download and update stories from the handled sites.

When a story is downloaded, several files will be written in a folder specific to the story:

- an `.html` file will be done to provide useful data about the story, like a link to the original story, the author's name or pseudonym, the provided summary, the number of chapters, ...
- an `.html` file will be created for each chapter of the story

In addition, logs files, a database to save the downloaded stories and `.css` files will be written/updated to ensure reading the story will be as enjoyable as possible.

Statistics can compiled for each site (on the condition stories from this site have been downloaded) and will provide informations about all the stories downloaded from the site they represent. Statistics are not updated automatically after downloading or updating a story.

From the statistics of a site it is possible to access the informations file of any story present at the time they were compiled and from then the chapters themselves. From the chapters it is possible to go back to the informations files and then to the statistics for the site or to go to the adjacent chapters (the previous one and the following one).
