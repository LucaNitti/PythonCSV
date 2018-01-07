# PythonCSV
Two simple scripts that help handling CSV.
Both are configurable using the config file

##Match.py
Match extract all the records from the fist file that match part of one of the value present in the second file.
It's possible extract all record or just the first.

**Example**

First.csv                           
Title,Author,Year                   
Pulp fiction,Tarantino,1994
Django Unchained,Tarantino,2012
Jackie Brown,Tarantino,1997
Full Metal Jacket, Kubrick, 1987
A Clockwork Orange, Kubrick, 1971
Forrest Gump,Zemeckis,1994



Second.csv
Year
1994
198

out.csv if first_or_all = first
Author,Title,Year
Tarantino,Pulp fiction,1994
Kubrick,Full Metal Jacket,1987

out.csv if first_or_all = all
Title,Author,Year
Pulp fiction,Tarantino,1994
Forrest Gump,Zemeckis,1994
Full Metal Jacket, Kubrick,1987

##Merge.py
really simple scripts that merge two csv file matching the value of a designed column




 