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
import json
import os


all_data = {}
entries_meta_data = {}

"""List of metadata keys to ignore."""
IGNORE_METADATA_KEYS = ['preview']


def get_metadata_paths(base_dir):
    paths = glob.glob(base_dir + '/users/*/*/*/*/metadata/*')
    return paths


def process(paths, output_file_name, uris_output_file_name=None):
    for path in paths:
        # path will look something like the following, after being split. The
        # 0th element may contain an arbitrarily long base_dir:
        # ['olpc_journal_processor/data/users', 'SHC1010111B',
        #  'datastore-2013-08-06_21:22', '01',
        #  '016d6a99-ae8e-4915-8a8b-f3ba0609da72', 'metadata', 'activity']
        (prefix, xo_serial, datastore_id, entry_uid_prefix, entry_uid, _, meta_data_name) = \
            path.rsplit('/', 6)

        # Read the content of the file.
        try:
            if meta_data_name in IGNORE_METADATA_KEYS:
                # Skip reading this metadata value.
                continue

            # Load all other metadata.
            with open(path, 'r') as file_fd:
                meta_data_content = file_fd.read()
        except EnvironmentError as err:
            print('Error reading file ‘%s’: %s' % (path, err))
            continue

        if len(meta_data_content) == 0:
            meta_data_content = 'NA'

        # Build the expected name of the data file for this journal entry.
        # Note: This file might not actually exist.
        data_file_path = os.path.join(prefix, xo_serial, datastore_id,
                                      entry_uid_prefix, entry_uid, 'data')

        # Get the metadata for this journal entry (identified by entry_uid).
        entry_meta_data_dict = None
        if entry_uid in entries_meta_data:
            # Get the dictionary.
            entry_meta_data_dict = entries_meta_data[entry_uid]
        else:
            # Add a dictionary.
            entry_meta_data_dict = {
                'xo_serial': xo_serial,
                'data_file_path': data_file_path,
            }
            entries_meta_data[entry_uid] = entry_meta_data_dict

        entry_meta_data_dict[meta_data_name] = meta_data_content

    csvfile = open(output_file_name, 'w+')
    writer = csv.writer(csvfile)
    idx = 0

    if uris_output_file_name is not None:
        uris_csv_file = open(uris_output_file_name, 'w+')
        uris_writer = csv.writer(uris_csv_file)
        uris_idx = 0
    else:
        uris_writer = None

    # Write header row.
    writer.writerow([
        'idx',
        'act',
        'icon_color',
        'activity_id',
        'keep',
        'mime_type',
        'mtime',
        'share_scope',
        'timestamp',
        'title',
        'title_set_by_user',
        'uid',
        'creation_time',
        'filesize',
        'xo_serial',
    ])

    if uris_writer is not None:
        uris_writer.writerow([
            'idx',
            'entry_idx',  # Foreign key to 'idx' in the main CSV file
            'uri',
        ])

    for key in entries_meta_data:
        a = entries_meta_data[key]

        activity = a.get('activity', 'NA')
        activity_id = a.get('activity_id', 'NA')
        icon_color = a.get('icon-color', 'NA')
        keep = a.get('keep', 'NA')
        mime_type = a.get('mime_type', 'NA')
        mtime = a.get('mtime', 'NA')
        share_scope = a.get('share-scope', 'NA')
        timestamp = a.get('timestamp', 'NA')
        title = a.get('title', 'NA')
        title_set_by_user = a.get('title_set_by_user', 'NA')
        uid = a.get('uid', 'NA')
        creation_time = a.get('creation_time', 'NA')
        filesize = a.get('filesize', 'NA')  # TODO: Could get default from data
        xo_serial = a.get('xo_serial', 'NA')

        data_file_path = a.get('data_file_path')  # Note: No default

        writer.writerow([
            idx,
            activity,
            icon_color,
            activity_id,
            keep,
            mime_type,
            mtime,
            share_scope,
            timestamp,
            title,
            title_set_by_user,
            uid,
            creation_time,
            filesize,
            xo_serial,
        ])

        # If the entry is for the Browse activity, try and parse the data file
        # to log the URIs the user visited.
        if activity == 'org.laptop.WebActivity' and uris_writer is not None \
           and data_file_path is not None:
            try:
                with open(data_file_path, 'r') as file_fd:
                    data = json.load(file_fd)

                # Log the URIs.
                tab_histories = data['history']
                for tab_history in tab_histories:
                    for entry in tab_history:
                        uris_writer.writerow([
                            uris_idx,
                            idx,
                            entry['url'],
                        ])
                        uris_idx += 1
            except EnvironmentError as err:
                print('Error reading WebActivity file ‘%s’: %s' %
                      (data_file_path, err))

        idx = idx + 1


if __name__ == '__main__':
    __author__ = 'Leotis Buchanan'

    parser = argparse.ArgumentParser(
        description='Generates a CSV file from one or more XOs’ log data.')
    parser.add_argument('-r', '--root', required=True,
                        help='X0’s logs root directory')
    parser.add_argument('-o', '--output', required=True,
                        help='Output file name')
    parser.add_argument('-u', '--uris-output', required=False,
                        help='Output file name for browser history')
    args = parser.parse_args()

    root_directory = args.root
    output_path = args.output
    uris_output_path = args.uris_output
    paths = get_metadata_paths(root_directory)
    process(paths, output_path, uris_output_path)
