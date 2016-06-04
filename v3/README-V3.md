# FFN DOWNLOADER - VERSION 3

Hello !

This program is here to help you download stories from fanfiction.net. Hopefully, you should be able to download each and every story published there, but since I didn't try, I don't know for sure.

**This was not tested on any other system than OS X 10.11. I hope it works on Windows or Linux but I didn't try. You can try though, I can't think of any way for this program to harm your computer, I certainly didn't want to create a virus.**

**This is a terminal program, not a proper application with a shiny User Interface (UI).**

### So, how does it work ?

It works great !

Seriously, here is how it works:

First, you give the link. [https://www.fanfiction.net/s/5904185/1/Emperor](https://www.fanfiction.net/s/5904185/1/Emperor) and [https://www.fanfiction.net/s/5904185/1/](https://www.fanfiction.net/s/5904185/1/) are both fine and will be handled in the exact same way.

Second, you say if you want the story to be updated or fully downloaded. Be aware that if you ask for an update, you must already have a downloaded it once in its previous state of completion to allow the program to have its way. Be sure to run the program in the correct directory too.

Third, you sit and wait. Depending on the number of chapters and their length, it can take quite some time ([Tales of Fairies](https://www.fanfiction.net/s/10264509/1/Tales-of-Fairies) comes to my mind for the number of chapters).

### You said it used a directory, can you detail ?

Yep !

I will take an example to explain. Say I want to download [HPMOR](https://www.fanfiction.net/s/5782108/1/Harry-Potter-and-the-Methods-of-Rationality) (actually, I did it a long time ago and even did a nice .pdf with it).

The link I will use here is [https://www.fanfiction.net/s/5782108/1/Harry-Potter-and-the-Methods-of-Rationality](https://www.fanfiction.net/s/5782108/1/Harry-Potter-and-the-Methods-of-Rationality).

Let's define some variables:

 - the numeric id, called `num_id`: 5782108,
 - the text id, called `text_id`: Harry-Potter-and-the-Methods-of-Rationality
 
(This IDs can be both found in the full link, but since I accept the short version, I get them elsewhere in the code of the page)

First, the program will create a directory named `(text_id)_(num_id)` (here: `Harry-Potter-and-the-Methods-of-Rationality_5782108`). Then it will change its working place to write directly inside this newly created directory.

Second, it will write the informations file, named `(text-id)_infos.html` (here: `Harry-Potter-and-the-Methods-of-Rationality_infos.html`).

Third, it will finally begin to actually download the 122 chapters of this truly amazing story and write them one by one in their proper file. Each chapter contains links to access the previous and the next ones, except if there are no such things (one-shot stories, first chapter, last chapter). The files are named with the following reasoning: `(zeros)(chap_number).html`. `zeros` is here to equalize the length of the name. In our example, HPMOR got 122 chapters, so the first one is named `001.html`, the tenth `010.html` and the hundredth `100.html`.

Finally the file containing the full story is written. It is named with the same pattern as the directory, except this time it is a file: `(text_id)_(num_id).html` (here: `Harry-Potter-and-the-Methods-of-Rationality_5782108.html`). This contains at its beginning a table of contents which allow the reader to easily access any chapter by simply clicking on its link in this very table of contents.

### You said we can update our stories, what is it ?

I don't have any joke for this ...

Once you download a story, if the author publishes a new chapter, you may want to update the story instead of downloading it in its entirety again and again.

To do so, just run the program in the following way:

 - Run it in the parent directory of the directory containing the story. For example, if your story is in `/foo/Harry-Potter-and-the-Methods-of-Rationality_5782108`, run the program in `/foo`.
 - When giving the adress, set the parameter `update` to `True`.
 
 It will update the story by downloading the new informations and the new chapter(s). The files containing the informations and the full story will be obviously updated in the process to keep up with the story itself.

### What else do I need to know ?

42 !

There are a few things you need to know to ensure you don't become mad using this. I would rather not have people flame me, even through a screen.

1. Don't hold me responsible for any damage this program might do to your computer. I tried to avoid all of them by choosing to let the program crash intead of using a sideway and hopefully stopping any damages before they are done but I can't test everything.

2. Credit me if you use this program as a base to work further (I plan to do an UI someday, wouldn't that be a nice thing ?). Just say the original work is from me, I will be happy, no need to pay me, contact me, sign something. Fanfictions on FFN are free, my way to download them too.

3. **Why `.html` ?** I used `html` files because they are reabable by almost any devices with a UI, light and easy to format to get the proper style.

On this theme, you are **entirely** free to change the setup I used for the header. I tried to do something basic which can satisfy most people, but who am I to pretend I know what most people desire ?

### A quick exemple

As a parting gift, I thought I would show you what using the program will give in your terminal:

The adress used is [https://www.fanfiction.net/s/2746577/1/Resistance](https://www.fanfiction.net/s/2746577/1/Resistance).

The end of `main3.py` looks like that for this test:

```python
main("https://www.fanfiction.net/s/2746577/1/Resistance")
```

The results in the console:

```
~$: python3 main3.py
________________________________________________________________________________



DOING: Resistance

AUTHOR: lorien829
ID: 2746577
URL: https://www.fanfiction.net/s/2746577/1/Resistance
CHAPTERS: 28

DONE -- Resistance_infos.html
DONE -- 01.html
DONE -- 02.html
DONE -- 03.html
DONE -- 04.html
DONE -- 05.html
DONE -- 06.html
DONE -- 07.html
DONE -- 08.html
DONE -- 09.html
DONE -- 10.html
DONE -- 11.html
DONE -- 12.html
DONE -- 13.html
DONE -- 14.html
DONE -- 15.html
DONE -- 16.html
DONE -- 17.html
DONE -- 18.html
DONE -- 19.html
DONE -- 20.html
DONE -- 21.html
DONE -- 22.html
DONE -- 23.html
DONE -- 24.html
DONE -- 25.html
DONE -- 26.html
DONE -- 27.html
DONE -- 28.html
DONE -- Resistance_2746577.html
~$: 
```

To give you and idea of what the infos file looks like (text version):

```
Resistance


By: lorien829
URL: https://www.fanfiction.net/s/2746577/1/Resistance

Voldemort has launched an all out war on the Wizarding World, and has taken the Boy Who Lived. But he has not reckoned on the resourcefulness of Hermione Granger. HHr developing in a sort of postapocalyptic environment.

Other informations:
- Rated: Fiction T 
- English 
- Angst 
- Hermione G., Harry P. 
- Chapters: 28 
- Words: 269,062 
- Reviews: 392 
- Favs: 474 
- Follows: 202 
- Updated: 2/8/2009 
- Published: 1/10/2006 
- Status: Complete 
- id: 2746577 

Chapters (28):

1. Loss
2. Absolution
3. Stratagem
4. Search
5. Recovery
6. Raid
7. Schism
8. Awakening
9. Betrayal
10. Revelations
11. Rally
12. Aftershock
13. Maneuvers
14. Changes
15. Exile
16. Cloak
17. Union
18. Lake
19. Passages
20. Circle
21. Mission
22. Liberation
23. Yule
24. Venture
25. Consequences
26. Preparation
27. Crescendo
28. Zenith
```
