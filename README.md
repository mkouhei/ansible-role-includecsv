# Ansible Role: include_csv

This role contains no tasks, but provides ``include_csv`` module which loads variables from a CSV file.

## include_csv module

This module will load variables from a CSV file.

Example task::

```yaml
- include_csv: src=path/to/foo.csv
```

The first line it will be read as the name of the parameter.
It will read the subsequent second line as data.::

```csv
id,name,price
0,apple,100
1,banana,200
2,cherry,300
3,durian,400
```

The variables named using file name without the extention.
To use variable as follow

```yaml
- debug: msg="{{ foo }}"
```

```python
ok: [localhost] => {
  "msg": "[{u'price': u'100', u'id': u'0', u'name': u'apple'}, {u'price': u'200', u'id': u'1', u'name': u'banana'}, {u'price': u'300', u'id': u'2', u'name': u'cherry'}, {u'price': u'400', u'id': u'3', u'name': u'durian'}]"
  }

## Options

ToDo

## Examples

ToDo

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

