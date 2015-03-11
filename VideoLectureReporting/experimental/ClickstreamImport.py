

import json
import DatabaseConnection

#print j.decoder.c_scanstring()

'C:\Users\Administrator\Desktop\click data\phys1-001_clickstream_export'

def get_clickstream_data(filename, value_str=False):
    
    """
    clickstream data comes in a json file and needs to be converted to
    Python objects to upload to a SQL Database. 

    Returns a list of dictionaries.

    If value_str is True will return the value string as a dictionary
    of Python objects too. This takes longer and uses a lot of memory.
    """

    with open(filename, 'rb') as data:
        
        clickdata_raw = data.readlines()

        clickdata_decoded = map(json.loads, clickdata_raw)
        
        if value_str==True:
            for c in clickdata_decoded:
                c['value'] = json.loads(c['value'])

    return clickdata_decoded

