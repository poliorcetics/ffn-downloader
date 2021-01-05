### What are the things to check for when changes were made to the code ?

This document provides a list of steps to carry out when significant changes (like adding a site) have been made to the code to ensure nothing is broken and no features were lost.

**Backward compatibilty should never be broken outside of major versions** and if it is, a program allowing passage from one to the other shall be provided for a time.

Without further ado, here is the list of the actions to try when testing. It aims to be as extensive as possible and if, for example, you only modified a message in a string you are not required to perform them all.

Checking the logs and the console while you do those tests is recommended. If needed, set `constants.LOG_LEVEL` to `DEBUG` to get a maximum of informations (**warning**: can be overwhelming to read).

1. Launch the app.
2. Add two URLs with the URL entry bar and deselect them **one by one**.
3. Add them again and deselect them **all at once**.
4. Download several stories **for each site** (see `test_stories.txt`), with the following requirements:
    - Two differents authors,
    - A one chapter story,
    - A story with three or more chapters,
    - Two stories belonging to a series.
5. For **each** site, mark one story as read, then unread, then read again, create the series for the corresponding stories.
6. Check if the informations and chapters are correctly written.
7. Select successively **each** site and check the results are correct.
8. Select successively **each** sorting options and check the results are correct.
9. Close the app, open it again and re-do steps **7** and **8**, to ensure no data was erased.
10. Compile the statistics for the **selected** site and then for **each** site.
11. Open the statistics files for **each** site and check the following items:
    - All informations are present and correct.
    - The link to the indexes are present and correct.
    - Clicking a value sort the statistics following this column.
12. Delete one chapter in a story for **each** site via your file manager and update them in the app. Ensure the deleted chapter is present again. 
13. Update the informations for one story of **each** site.
14. Fully delete a story from the app for **each** site, not the one you updated the informations of. Check if all files were correctly deleted, including the folder containing the story and nothing more.
15. Delete the series for **each** site.
16. Update the statistics and check them again just as you did during step **11**. Additionally, check the deleted stories are not present.
17. Add a series but add no stories to it and close the sub-window. Reopen it and check the series is **not** present.
18. Try changing your settings (the save folder) and then changing them back. If everything loads without a problem, congratulations, the application is working perfectly !