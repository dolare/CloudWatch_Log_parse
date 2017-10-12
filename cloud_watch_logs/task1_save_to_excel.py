from src.download import download
from src.export import export
from src.save_data import save_as_excel
from src.parse import parse_for_excel
import time
import sys


if __name__ == "__main__":
    #export log to s3 and return taskid
    export_task = export(sys.argv[0],sys.argv[1])

    #wait for trasfering and download log gz files from s3 bucket
    time.sleep(3)
    download(export_task, '.tmp/service.log')

    #parse the data and return data as json(dict) format
    data = parse_for_excel('.tmp/service.log')
    time.sleep(3)

    #save data as excel 
    save_as_excel(data, '.tmp/service.log', './tmp/logs.xlsx')