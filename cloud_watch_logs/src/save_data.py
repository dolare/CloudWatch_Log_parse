import xlsxwriter
import pandas as pd
import os

def save_as_excel(data_list):#data is a list, each element is a list too, the lenth of data == how many excel files will be generated

    for data in data_list:
        excel_name = None
        for record in data:
            for k,v in record.items():
                if k == 'gradet' and 'CUSTOMER_EMAIL' in record[k].keys():
                    record[k] = record[k]['CUSTOMER_EMAIL']
                elif k == 'gradet' and not 'CUSTOMER_EMAIL' in record[k].keys():
                    record[k] = None
                if k == 'api_start_time':
                    arr = v.split('T')
                    arr0 = arr[0].split('-')
                    date = arr0[1] + '/' + arr0[2] + '/' + arr0[0]
                    arr1 = arr[1].split('.')
                    time = arr1[0]


                    record[k] = "{} {}".format(date,time)
                    if excel_name == None:
                        excel_name = arr[0]#define the excel name to make the generated excel more clearly

                    print(record[k])

        df = pd.DataFrame(data=data)


        writer = pd.ExcelWriter(os.path.dirname(__file__) + '/tmp/' + excel_name +'.xlsx', engine='xlsxwriter')
        df.to_excel(writer,sheet_name='Sheet1')

        writer.save()
        excel_name = None
