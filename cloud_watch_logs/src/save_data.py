import xlsxwriter

def save_as_excel(data, source,target):

    for record in data:
        for k,v in record.items():
            if k == 'gradet' and 'CUSTOMER_NAME' in record[k].keys():
                print(record[k])
                record[k] = record[k]['CUSTOMER_NAME']

    df = pd.DataFrame(data=data)

    writer = pd.ExcelWriter(target, engine='xlsxwriter')
    df.to_excel(writer,sheet_name='Sheet1')

    writer.save()