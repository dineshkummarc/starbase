
# script to create a new user

import ConfigParser
import sys
import shutil
import sqlite3
import os

from starbase.utils import file_exists

def create_user(username, accesstoken, verbose=0):
    if verbose:
        print "trying to create user", username
    
    # read configuration
    config = ConfigParser.RawConfigParser()
    config.read('../config.cfg')
    
    user_data_folder = config.get('general', 'user_data_folder')
    user_database = user_data_folder + username + '.sql'
    user_url = config.get('general', 'domain') + username

    # check if user already exists
    if file_exists(user_database):
        if verbose:        
            print "error: user already exists"
        return 2
    
    # here be dragons
    try:
        # copy over initial database
        shutil.copy2('default.sql', user_database)

        # initialize database
        db = sqlite3.connect(user_database)
        db.execute('INSERT INTO admin (authkey, name, url) VALUES (?, ?, ?) ', 
                   (accesstoken, username, user_url))
        db.commit()
        db.close()
        
    except Exception, e:
        # delete the file if it was created
        if file_exists(user_database):
            os.remove(user_database)
        if verbose:
            print e
        return 2
    else:
        if verbose:        
            print "success"
        return 0

def main():
    if len(sys.argv) != 3:
        print "usage: python newuser.py <username> <accesstoken>"
        return 2
    username = sys.argv[1]
    accesstoken = sys.argv[2]
    return create_user(username, accesstoken, 1)
    
        
if __name__ == "__main__":
    sys.exit(main())
    
