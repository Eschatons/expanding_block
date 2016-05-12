# -*- coding: utf-8 -*-
"""
Created on Thu May 12 10:14:18 2016

@author: efron
"""
from expanding_block import expanding_block
import datetime

def mass_expanding_block(filenames, output_folder, authentic_prefix = 'AU_', 
     modified_prefix = 'CM_', logFileName = 'DEFAULT'):

# default LOG
    if logFileName.upper() == 'DEFAULT':
        today = datetime.datetime.today()
        today = ('%s_%s_%s_%s_%s' %
        (today.year, today.month, today.day, today.hour, today.minute))
        logFileName = 'expanding_block_%s.csv' % (today)

# open log:
    try:
        log = open(logFileName, 'w')
    except IOError as io:
        print('warning!')
        print('Unable to create file on disk while opening log')
        print(io)
    finally:
        try:
            log.close()
        except Exception:           
            # we're not worried about side effects of closing the file.
            pass
    
    def log(bufferedLog):        
        try:
            log = open(logFileName, 'a')
            log.write(bufferedLog)
        except IOError as io:
            print('warning!')
            print('unable to write to log:')
            print(io)
        finally:
            try:
                log.close()
            except Exception:
                pass

    
    for filename in filenames:
        imgModified, imgOut = expanding_block(filename)
        if imgModified:
            output_filename = authentic_prefix + filename
        
        