import pandas as pd
import ConfigParser

configParser = ConfigParser.RawConfigParser()
configFilePath = r'config.conf'
configParser.read(configFilePath)

path_first_file = configParser.get('merge', 'path_first_file')
path_second_file = configParser.get('merge', 'path_second_file')
colunm_join = configParser.get('merge', 'column_join')

first_file = open(path_first_file, 'r')
second_file = open(path_second_file, 'r')
first_csv = pd.read_csv(first_file)
second_csv = pd.read_csv(second_file)
df = pd.merge(first_csv,second_csv, on=colunm_join)
df.to_csv('out.csv', mode='a')