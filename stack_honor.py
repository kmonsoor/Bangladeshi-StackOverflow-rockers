###############################
# author     :   Khaled Monsoor (k@kmonsoor.com)
# Created at :  2015.12.10
# Distribution : The MIT License
#
# (c) 2015  Khaled Monsoor
###############################

import csv
from tabulate import tabulate

reader = csv.DictReader(open('stack.csv'))
table = [['SO profile', 'StackExchange Flair', 'Github', 'Website', 'contact']]

for row in reader:
    trow = ['[' + row['DisplayName'] + "](http://stackoverflow.com/users/" + row['Id'] + ')',
            '![Flair](http://stackexchange.com/users/flair/' + row['AccountId']+'.png)', 
            '[?](http://github.com/)',
            (row['WebsiteUrl'])[:50], 
            '?@?']
    table.append(trow)

tabulated = tabulate(table, headers='firstrow', tablefmt='pipe')
    
with open('stack_out.txt', 'w') as output:
    for row in tabulated:
        output.write(row)
