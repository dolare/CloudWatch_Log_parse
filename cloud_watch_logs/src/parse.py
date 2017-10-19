import re
import json
import os

def parse_for_excel(file_names):#file_names should be file path list

    pattern1 = re.compile("\d*-\d*-\d*T\d*:\d*:\d*.\d*Z --*")
    pattern2 = re.compile("\d*-\d*-\d*T\d*:\d*:\d*.\d*Z {")
    pattern3 = re.compile("\d*-\d*-\d*T\d*:\d*:\d*.\d*Z }")

    data = [] #arra with the dataname
    for file in file_names:
        with open(os.path.dirname(__file__) + '/tmp/' + file, "r") as ins:
            
            array = []
            temp = ''
            for line in ins:
                if pattern1.match(line):
                    if temp != '': 
                        print(temp)
                        try:
                            array.append(json.loads(temp))
                        except:
                            print('fail + 1')
                    print('=======')
                    temp = ''
                    continue
                elif pattern2.match(line):
                    line = "{"
                elif pattern3.match(line):
                    line = "}"
                temp += line

            array.append(json.loads(temp))
            
        data.append(array)


    return data
