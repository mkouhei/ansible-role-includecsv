# Ansible Role: include_csv

This role contains no tasks, but provides the ``include_csv`` module which loads
data from a CSV file.

Ansible Galaxy Page: https://galaxy.ansible.com/mkouhei/include_csv/

## install

```bash
$ virtualenv /path/to/venv
$ /path/to/venv/bin/pip install ansible
$ cd /path/to/your_playbook
$ /path/to/venv/bin/ansible-galaxy install -p ./library mkouhei.include_csv
```

### usages

Path ` -M library/mkouhei.include_csv/library` option to `ansible` or `ansible-playbook` command.


## include_csv module

Example task:

```yaml
- include_csv: src=path/to/fruits.csv
```

The first line of the CSV file must be a header containing a list of field
names, for example:

```csv
id,name,price
0,apple,100
1,banana,200
2,cherry,300
3,durian,400
```

- `include_csv` reads the data into a list of dictionaries,
  one dictionary per line.
- The dictionary keys are the field names.
- The data is stored in a variable whose name is the CSV file
  name without the extension.

For example, the data for the above CSV file can be accessed as follows:

```yaml
- debug: msg="{{ fruits }}"
```

```python
ok: [localhost] => {
  "msg": "[{u'price': u'100', u'id': u'0', u'name': u'apple'}, {u'price': u'200', u'id': u'1', u'name': u'banana'}, {u'price': u'300', u'id': u'2', u'name': u'cherry'}, {u'price': u'400', u'id': u'3', u'name': u'durian'}]"
  }
```

## Options

| parameter | required | default | choices | comments                                                                                                                                      |
|:----------|:---------|:--------|:--------|:----------------------------------------------------------------------------------------------------------------------------------------------|
| src       | yes      |         |         | Specify the CSV file path. The path can be absolute or relative. (Detection of files under roles/foo/files is not supported.) |
| delimiter | no       | '       |         | Single-character field separator.                                                                                         |
| quotechar | no       | "       |         | Single-character quote character.                                                                                       |

## Examples

Use ``include_vars`` as follows:

```yaml
- include_csv: src=foo.csv
```

```yaml
- include_csv: src=bar.csv delimiter="|" quotechar="'"
```

### Load locally

In the previous examples the CSV file is loaded on every remote node
targeted by the play.

To load CSV data from a file on the Ansible control server,
use `local_action` or `connection: local`, for example:

```yaml
- include:csv: src=bar.csv
  connection: local
  sudo: no
```

### Load locally, only once

There are two potential problems with the previous example (depending
on the desired behaviour):
- the local file is loaded *multiple times*; once for each target node
- `ansible-playbook` output will appear to show the task running against every
  target node

To load CSV data *only once* from a file on the control server,
use a separate play within your playbook which 
targets localhost. Subsequent plays can access the data via `hostvars`, for
example:

```yaml
- hosts: localhost
  roles:
    - role: mkouhei.include_csv
  tasks:
    - include_csv: src=fruits.csv

- hosts: t1, t2
  tasks:
  - debug: msg="{{item.name}}"
    with_items: "{{hostvars.localhost.fruits}}"
```

## Requirements
None.

## Role variables

None.

## Dependencies

None.

## License

GPLv3

## Author Information

[Kouhei Maeda](https://github.com/mkouhei)

