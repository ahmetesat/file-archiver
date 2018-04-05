"""
@Author: Ahmet Esat Kara
@Date_Generated:   23.05.2017
@Date_Modified: -
@Description: This script runs once in a day at ex. 3 am (after midnight)to archive the the files exist on the path.
              Paths will be supplied by the user into path_for_archive file as line by line via.
              Path structure is: PATH;DAY (If you doesn't supply day, default will be 0. Every files will be archive)
              EXAMPLE ==>C:\Users\ahmetesat\Documents\restorer;1
              1) C:\Users\ahmetesat\Documents\restorer means which directory you want to archive
              2) 1 means how many days before you will store (If the date is 23.05.2017 and day is 1, script doesn't
              include the day 23)
              Then, scripts place every file in that path to the subfiles according to the file's generated date.
              Structure is like path/Archive/Year/Mounth/Day
"""

import os
import shutil
import logging
from datetime import datetime,date,timedelta
from time import gmtime, strftime


current_date = strftime("%Y_%m_%d", gmtime())                                 #Gets current date for log file

LOG_FILENAME = current_date+".log"

def generate_folder(path, folder_name):
    """
    :param path: Gets the path of working path
    :param folder_name: The name which will be generated if it is non exist
    :return: generates folder
    """
    archive_file = os.path.join(path,folder_name)
    if not os.path.exists(archive_file):                                      # Checks whether there is a Archive folder
        return os.makedirs(archive_file)                                      # If not make a dir Archive

def archiver():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s --- %(levelname)s --- %(message)s',
                        filename=LOG_FILENAME)
    logging.info('------------ LOG STARTED-------------------------------------')
    logging.info('------------ BE SURE THAT YOUR PATHS ARE CORRECT ------------')
    logging.info('------------ FUNCTION STARTED -------------------------------')
    Archive = "Archive"

    with open("path_for_archive") as f:                                       #Reads the file ful with paths

        for x in f.readlines():                                               #Reads lines of path file
            if not x:
                logging.info('There is no path in the path file')
            line = x.strip('\n').split(";")                                   #Clean the newline element and
                                                                              #seperates its path and numbet
            path_src = line[0]                                                #Gets path

            archive_day_before = line[1]                                      #Gets day number. Makes 2 digit if not
            if not archive_day_before: archive_day_before = 0                 #If there is no day value, then make 0

            today = date.today()
            day_ago = today - timedelta(days=int(archive_day_before))

            generate_folder(path_src,Archive)
            path_archive = os.path.join(path_src, Archive)

            for file in os.listdir(path_src):                                 #Goes sour path to read files

                file_path = os.path.join(path_src, file)
                if os.path.isfile(file_path):                                 #If it is a file
                    try:
                        mtime = os.path.getmtime(os.path.join(path_src, file))#Gets modification time the file
                    except OSError:
                        mtime = 0

                    time_file = datetime.fromtimestamp(mtime)                 #Convert it as datetime

                    if day_ago >= time_file.date():
                        Year = time_file.strftime('%Y')                       #Gets year
                        Month = time_file.strftime('%m')                      #Gets month
                        Day = time_file.strftime('%d')                        #Gets day

                        generate_folder(path_archive,Year)
                        path_archive_year = os.path.join(path_archive, Year)  #Path year such as ../Archive/Year

                        generate_folder(path_archive_year, Month)
                        path_archive_month = os.path.join(path_archive_year, Month)#Path month such as ../Archive/Month

                        generate_folder(path_archive_month, Day)
                        path_archive_day = os.path.join(path_archive_month, Day)
                        try:
                            shutil.move(file_path, path_archive_day)          #Cut and copy file to its new destination
                            logging.info('File ==>%s added to %s path' % (file, path_archive_day))
                        except shutil.Error, exc:
                            logging.info('ERROR OCCURED. File ==>%s cant be added to %s path'% (file, path_archive_day))
                            logging.exception(exc)

    logging.info('------------ LOG FINISHED------------------------------------')
if __name__ == '__main__':
    archiver()