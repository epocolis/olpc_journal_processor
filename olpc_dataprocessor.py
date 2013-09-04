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


all_data = {}
entries_meta_data = {}


def get_metadata_paths(base_dir):
    paths = glob.glob(base_dir + '/users/*/*/*/*/metadata/*')
    return paths


def process(paths, output_file_name):
    for path in paths:
        # Read the content of the file.
        f = open(path)
        meta_data_content = f.read()

        # path will look something like the following, after being split. The
        # 0th element may contain an arbitrarily long base_dir:
        # ['olpc_journal_processor/data/users', 'SHC1010111B',
        #  'datastore-2013-08-06_21:22', '01',
        #  '016d6a99-ae8e-4915-8a8b-f3ba0609da72', 'metadata', 'activity']
        (_, xo_serial, datastore_id, _, entry_uid, _, meta_data_name) = \
            path.rsplit('/', 6)

        if meta_data_name == 'preview' or len(meta_data_content) == 0:
            meta_data_content = 'NA'

        # Get the metadata for this journal entry (identified by entry_uid).
        entry_meta_data_dict = None
        if entry_uid in entries_meta_data:
            # Get the dictionary.
            entry_meta_data_dict = entries_meta_data[entry_uid]
        else:
            # Add a dictionary.
            entry_meta_data_dict = { 'xo_serial': xo_serial }
            entries_meta_data[entry_uid] = entry_meta_data_dict

        entry_meta_data_dict[meta_data_name] = meta_data_content

    csvfile = open(output_file_name, 'w+')
    writer = csv.writer(csvfile)
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
        'uid',
        'creation_time',
        'filesize',
        'xo_serial',
    ])

    for key in entries_meta_data:
        a = entries_meta_data[key]

        act = a.get('activity', 'NA')
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
        creation_time = a.get('creation_time', 'NA')
        filesize = a.get('filesize', 'NA')  # TODO: Could get default from data
        xo_serial = a.get('xo_serial', 'NA')

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
            uid,
            creation_time,
            filesize,
            xo_serial,
        ])
        idx = idx + 1


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
