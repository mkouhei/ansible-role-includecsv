#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (C) 2015 Kouhei Maeda <mkouhei@palmtb.net>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import csv
import os.path

from traceback import format_exc


DOCUMENTATION = """
---
module: include_csv
short_description: Load variables from a CSV file, dynamically within a task.
description:
    - Load variables from a CSV file dynamically during task runtime.
notes: []
version_added: null
author:
    - 'Kouhei Maeda (@mkouhei)'
options:
    src:
        required: true
        default: null
        description:
          - specify CSV file name.
    delimiter:
        required: false
        default: ,
        description:
            - a one-character string to use as the field separator.
    quotechar:
        required: false
        default: "
        description:
            - a one-character string to use as the quoting character.
"""

EXAMPLES = """
# load csv
- include_csv: src=path/to/foo.csv

# 
- include_csv: src=path/to/bar.csv delimiter="\t" quotechar='"'
"""


def _basename(filepath):
    return os.path.basename(os.path.splitext(filepath)[0])


def _change_ext(filepath):
    return '{0}.yml'.format(_basename(filepath))


def _vars_dir(filepath):
    return os.path.join(os.path.dirname(os.path.dirname(filepath)), 'vars')


def convert(csvpath, delimiter, quotechar):
    key = _basename(csvpath)
    with open(csvpath, 'rb') as fobj:
        reader = csv.DictReader(fobj,
                                delimiter=delimiter,
                                quotechar=quotechar)
        data = {'{0}'.format(key): [i for i in reader]}
    return data


def main():
    module = AnsibleModule(
        argument_spec={
            'src': dict(required=True),
            'delimiter': dict(required=False, default=','),
            'quotechar': dict(required=False, default='"'),
        },
        check_invalid_arguments=False,
        supports_check_mode=True,
    )

    try:
        src = os.path.expanduser(module.params.get('src'))
        delimiter = module.params.get('delimiter')
        quotechar = module.params.get('quotechar')

        if not os.path.exists(src):
            module.fail_json(msg="Source {0} failed to read".format(src))
        if not os.access(src, os.R_OK):
            module.fail_json(msg="Source {0} not readable".format(src))
        loaded = convert(src, delimiter=delimiter, quotechar=quotechar)
    except Exception as exc:
        module.fail_json(msg=str(exc), exc=format_exc())
    module.exit_json(ansible_facts=loaded)


from ansible.module_utils.basic import *  # noqa
main()
