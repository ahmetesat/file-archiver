# file-archiver

This script runs once in a day at ex. 3 am (after midnight) to archive the the files exist on the path.
Paths will be supplied by the user into path_for_archive file as line by line via.

Path structure is: PATH;DAY (If you doesn't supply day, default will be 0. Every files will be archive)

EXAMPLE ==> C:\Users\ahmetesat\Documents\restorer;1
1) C:\Users\ahmetesat\Documents\restorer means which directory you want to archive
2) 1 means how many days before you will store (If the date is 23.05.2017 and day is 1, script doesn't
include the day 23)
Then, scripts place every file in that path to the subfiles according to the file's generated date.
Structure is like path/Archive/Year/Mounth/Day
