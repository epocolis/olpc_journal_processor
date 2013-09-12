#!/usr/bin/python
# coding=utf-8
# vim: ai ts=4 sts=4 et sw=4 ft=python

from distutils.core import setup
from subprocess import check_output

# Get the git version from `git describe`
git_version = check_output(['git', 'describe',
                            '--long', '--tags', '--dirty', '--always'])
git_version = git_version.rstrip('\n')

# Setup!
setup(name='olpc-journal-processor',
      description='Script to extract data from the OLPC Journal data store',
      long_description='A script to extract data from the OLPC Journal data store on an XS school\n' \
                       'server and output it in CSV format for further processing.',
      version=git_version,
      author='Leotis Buchanan, Philip Withnall',
      author_email='philip@tecnocode.co.uk',
      license='GPLv3',
      platforms=['noarch'],
      url='https://github.com/Leotis/olpc_journal_processor',
      scripts=['olpc-journal-processor', 'olpc-journal-aggregator'])
