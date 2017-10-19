from download import download
from export import export
from save_data import save_as_excel
from parse import parse_for_excel
from clean_folder import clean_folder
import os
import time
import sys


if __name__ == "__main__":

    #clean the folder before
    clean_folder(os.path.dirname(__file__) + '/tmp')

    #export log to s3 and return taskid
    export_task = export(int(sys.argv[1]), int(sys.argv[2]))

    #wait for trasfering and download log gz files from s3 bucket
    time.sleep(3)
    file_names = download(export_task)

    #parse the data and return data as json(dict) format
    data = parse_for_excel(file_names)
    time.sleep(3)

    #save data as excel 
    save_as_excel(data)