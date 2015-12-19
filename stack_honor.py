#!/usr/bin/python
__author__  = 'Khaled Monsoor <k@kmonsoor.com>'
__license__ = 'The MIT License: <http://kmonsoor.mit-license.org/>'
__version__ = '0.5.0'
###############################


import csv
import json

# external dependencies 
import requests
import tldextract
from bs4 import BeautifulSoup
from tabulate import tabulate


###############################
# update these value with your id & secret from `https://github.com/settings/developers`
# Without authenticated ID/secret, Github API hits fail after few hits
github_client_id = 'f34560-FAKE-FAKE-40c'   
github_client_secret = 'f5943e41f96-OBVIOUSLY-FAKE-1b4d7ea91aad37'
###############################


def stackoverflow_to_github_user(stackoverflow_id):
    '''
    Given a numerical `userID` on StackOverflow, it returns user's username on Github, if available.
    If `userID` is invalid on StackOverflow, it raise `ValueError`.
    If `userID` is valid on StackOverflow but has no Github info associated, \
        it will return empty string('').
    '''
    url = 'http://stackoverflow.com/users/' + str(int(stackoverflow_id))
    response = requests.get(url)
    
    if response.status_code != 200:
        raise ValueError('Invalid user ID: {}'.format(stackoverflow_id))
        
    soup = BeautifulSoup(response.content)
    github_user = ''
    for tag in soup.find_all('a', attrs={'class': 'url'}):
        if 'github' in tag.get('href', ''):
            github_user = tag['href'].split('/')[-1]
    return github_user


def github_user_to_email(username):
    '''
    Given a valid Github username, this function returns the users email address.
    If `username` is invalid on Github.com, it will raise ValueError.
    If `username` is valid but the user's email-address is not public, 
        an empty string('') will be returned.
    '''
    if not len(str(username)):
        raise ValueError

    api_url = 'https://api.github.com/users/{0}?client_id={1}&client_secret={2}'.format(username, \
                                                                                        github_client_id, \
                                                                                        github_client_secret)
    
    response = requests.get(api_url)
    if response.status_code != 200:
        print 'Github access failure'
        raise ValueError('Invalid username: {}'.format(username))

    user = json.loads(response.content)
    return user['email'] if user['email'] else ''

    

# Main module
reader = csv.DictReader(open('stack.csv'))   # csv from `http://data.stackexchange.com/stackoverflow/query/412368/`
table = [['SO profile', 'StackExchange Flair', 'Github', 'Website', 'contact']]

for row in reader:
    # trying to get Github profile, and then email from there
    print row
    try:
        github_user = stackoverflow_to_github_user(row['Id'])
        github = '' if not len(github_user) else '[{0}](http://github.com/{0})'.format(github_user)
    except ValueError:
        github = ''
        github_email = ''
    else:
        try:
            github_email = github_user_to_email(github_user)
        except:
            github_email = ''
            
    
    # Validating website address & purging invalid address
    site = row['WebsiteUrl']
    try:
        response = requests.get(site)
    except:
        site = ''
        site_label = ''
    else:
        if response.status_code == 200:
            site_label = tldextract.extract(site).registered_domain + '/...'
        else:
            site = ''
            site_label = ''
    
    # finally adding the row for MarkDown conversion
    trow = ['[' + row['DisplayName'] + "](http://stackoverflow.com/users/" + row['Id'] + ')',
            '![Flair](http://stackexchange.com/users/flair/' + row['AccountId']+'.png)', 
            github,
            '[' + site_label + '](' + site + ')', 
            github_email]
    table.append(trow)

# converting the output to a MarkDown(*.md) formatted table
tabulated = tabulate(table, headers='firstrow', tablefmt='pipe')
with open('stack_out.md', 'w') as output:
    for row in tabulated:
        output.write(row)
