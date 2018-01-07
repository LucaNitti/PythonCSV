import ConfigParser
import pandas as pd
import os
import sys
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

configParser = ConfigParser.RawConfigParser()
configFilePath = r'config.conf'
configParser.read(configFilePath)

current_dir = os.getcwd()

path_file_to_filter = "{}/{}".format(current_dir, configParser.get('match', 'path_file_to_filter'))
column_name_to_filter = configParser.get('match', 'column_name_to_filter')

path_file_with_value = "{}/{}".format(current_dir, configParser.get('match', 'path_file_with_value'))
column_name_with_value = configParser.get('match', 'column_name_with_value')
first_or_all = configParser.get('match', 'first_or_all')


#read file with panda

file_to_filter = pd.read_csv(open(path_file_to_filter, 'r'))
data_with_value = pd.read_csv(open(path_file_with_value, 'r'))[column_name_with_value]

result_filter = pd.DataFrame()

len_data = data_with_value.__len__()
index = 1
for data in data_with_value:
    data = str(data)
    sys.stdout.write("\033[F") #back to previous line
    #sys.stdout.write("\033[K")
    sys.stdout.write('analyze {}/{}'.format(index,len_data))
    #sys.stdout.flush()

    index = index + 1
    print file_to_filter[column_name_to_filter]
    filtered_record = file_to_filter[file_to_filter[column_name_to_filter].apply(str).str.contains(data) == True]
    if first_or_all == 'first':
        filtered_record = filtered_record.iloc[0]

    result_filter = result_filter.append(filtered_record)

result_filter.to_csv('out.csv',mode='a', index=False)

print "File Created "
print "done"
