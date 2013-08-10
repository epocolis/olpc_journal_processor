"""
olpc XO log files processor
~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2013 by the Leotis Buchanan, see AUTHORS for more details.
:license: GPL, see LICENSE for more details.
"""


import argparse
import glob
import csv
import time



all_data = {} 
users_meta_data = {}

def getMetaDataPath(base_dir):
    paths = glob.glob(base_dir + '/users/*/*/*/*/metadata/*')
    return paths


def process(paths,output_file_name):
    cnt = 0
    for path in paths:
        #read the content of the file
        f = open(path)
        meta_data_content = f.read()


        #print(meta_data_content)
        path = path.split("/")
        meta_data_name = clean(path[7])
        if meta_data_name == "preview":
            meta_data_content = "NA"
        user_id = clean(path[5])
        #get this user meta data
        if user_id in users_meta_data:
            #get the dictionary
            user_meta_data_dict = users_meta_data[user_id]
            user_meta_data_dict[meta_data_name] = clean(meta_data_content)
        else:
            #we add a dictionary
            user_meta_data_dict = {}
            meta_data_content = clean(meta_data_content)
            user_meta_data_dict[meta_data_name] = clean(meta_data_content)
            user_meta_data_dict['SH'] = clean(path[2])
            #stick the dictionary back in
            users_meta_data[user_id] = user_meta_data_dict

    
    csvfile = open(output_file_name,'w+')
    writer = csv.writer(csvfile, delimiter='*')
    size = []
    idx = 0
    #write header row
    writer.writerow([
            "idx",
            "act",
            "icon_color",
            "activity_id",
            "keep",
            "mime_type",
            "mtime",
            "preview",
            "share_scope",
            "timestamp",
            "title",
            "title_set_by_user",
            "uid"])
        
    for key in users_meta_data:
        a = users_meta_data[key]
        sh = a.get('SH', "NA")     
        act = a.get('activity',"NA")
        share_scope = a.get('share-scope',"NA")
        activity_id = a.get('activity_id',"NA")

        icon_color = a.get('icon-color',"NA")
        keep = a.get('keep',"NA")
        mime_type = a.get('mime_type',"NA")
        mtime = a.get('mtime',"NA")
        preview = a.get('preview',"NA")
        share_scope = a.get('share-scope',"NA")
        timestamp = a.get('timestamp',"NA")
        title = a.get('title',"NA")
        title_set_by_user = a.get('title_set_by_user',"NA")
        uid = a.get('uid',"NA")
        writer.writerow([idx,act, icon_color,activity_id,
                  keep,
                  mime_type,
                  mtime,
                  preview,
                  share_scope,
                  timestamp,
                  title,
                  title_set_by_user,
                  uid])
        idx = idx + 1
   

        
def clean(data):
    #data = data.strip()
    data = data.replace(",",",")
    if len(data)== 0:
        return "NA"
    else:
        return data



if __name__ == '__main__':
    __author__ = 'Leotis Buchanan'
    parser = argparse.ArgumentParser(description='This script generates a csv file from one or more  OX\'s log data.')
    parser.add_argument('-r','--root', help='X0\'s logs root directory',required=True)
    parser.add_argument('-o','--output',help='Output file name', required=True)
    args = parser.parse_args()

    root_directory = args.root
    output_path  = args.output
    paths =  getMetaDataPath(root_directory)
    process(paths, output_path)   




