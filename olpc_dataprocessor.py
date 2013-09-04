#!/usr/bin/python
# coding=utf-8

'''
olpc XO log files processor
~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2013 by the Leotis Buchanan, see AUTHORS for more details.
:license: GPL, see LICENSE for more details.
'''


import argparse
import glob
import csv
import time


all_data = {}
users_meta_data = {}


def get_metadata_paths(base_dir):
    paths = glob.glob(base_dir + '/users/*/*/*/*/metadata/*')
    return paths


def process(paths, output_file_name):
    cnt = 0
    for path in paths:
        # Read the content of the file.
        f = open(path)
        meta_data_content = f.read()

        path = path.split('/')
        meta_data_name = clean(path[7])
        if meta_data_name == 'preview':
            meta_data_content = 'NA'
        user_id = clean(path[5])

        # Get this user's metadata.
        if user_id in users_meta_data:
            # Get the dictionary.
            user_meta_data_dict = users_meta_data[user_id]
            user_meta_data_dict[meta_data_name] = clean(meta_data_content)
        else:
            # Add a dictionary.
            user_meta_data_dict = {}
            meta_data_content = clean(meta_data_content)
            user_meta_data_dict[meta_data_name] = clean(meta_data_content)
            user_meta_data_dict['SH'] = clean(path[2])
            # Stick the dictionary back in.
            users_meta_data[user_id] = user_meta_data_dict

    csvfile = open(output_file_name, 'w+')
    writer = csv.writer(csvfile, delimiter='*')
    size = []
    idx = 0

    # Write header row.
    writer.writerow([
        'idx',
        'act',
        'icon_color',
        'activity_id',
        'keep',
        'mime_type',
        'mtime',
        'preview',
        'share_scope',
        'timestamp',
        'title',
        'title_set_by_user',
        'uid'
    ])

    for key in users_meta_data:
        a = users_meta_data[key]

        sh = a.get('SH', 'NA')
        act = a.get('activity', 'NA')
        share_scope = a.get('share-scope', 'NA')
        activity_id = a.get('activity_id', 'NA')
        icon_color = a.get('icon-color', 'NA')
        keep = a.get('keep', 'NA')
        mime_type = a.get('mime_type', 'NA')
        mtime = a.get('mtime', 'NA')
        preview = a.get('preview', 'NA')
        share_scope = a.get('share-scope', 'NA')
        timestamp = a.get('timestamp', 'NA')
        title = a.get('title', 'NA')
        title_set_by_user = a.get('title_set_by_user', 'NA')
        uid = a.get('uid', 'NA')

        writer.writerow([
            idx,
            act,
            icon_color,
            activity_id,
            keep,
            mime_type,
            mtime,
            preview,
            share_scope,
            timestamp,
            title,
            title_set_by_user,
            uid
        ])
        idx = idx + 1


def clean(data):
    data = data.replace(',', ',')
    if len(data) == 0:
        return 'NA'
    else:
        return data


if __name__ == '__main__':
    __author__ = 'Leotis Buchanan'

    parser = argparse.ArgumentParser(
        description='Generates a CSV file from one or more XOs’ log data.')
    parser.add_argument('-r', '--root', required=True,
                        help='X0’s logs root directory')
    parser.add_argument('-o', '--output', required=True,
                        help='Output file name')
    args = parser.parse_args()

    root_directory = args.root
    output_path = args.output
    paths = get_metadata_paths(root_directory)
    process(paths, output_path)
