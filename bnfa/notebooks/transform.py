# pull source input XML and convert to transformed XML via XSL.

import pathlib
import subprocess

loc1 = pathlib.Path.cwd()
print('loc1')
print(loc1)
print([x for x in loc1.iterdir()])
loc2 = pathlib.Path.cwd().parents[0]
print('loc2')
print(loc2)
print([x for x in loc2.iterdir()])
loc3 = pathlib.Path.cwd().parents[1]
print('loc3')
print(loc3)
print([x for x in loc3.iterdir()])

saxon_path = pathlib.Path.cwd().parents[1] / 'saxon' / 'saxon-he-12.3.jar'
print(saxon_path, saxon_path.exists())
saxon_path = pathlib.Path.cwd().parents[0] / 'saxon' / 'saxon-he-12.3.jar'
print(saxon_path, saxon_path.exists())
if not saxon_path.exists():
    raise Exception('saxon does not exist.')

source_path = pathlib.Path.cwd().parents[0] / 'input' / '0.xml'
if not source_path.exists():
    raise Exception('source does not exist.')

transform_path = pathlib.Path.cwd().parents[0] / '20230601_BNFA-RDF-XML_withoutComments.xsl'
if not transform_path.exists():
    raise Exception('transform does not exist.')

output_path = pathlib.Path.cwd().parents[0] / 'transform' / '0.xml'
subprocess.call(['java', '-jar', str(saxon_path), f'-s:{source_path}', f'-xsl:{transform_path}', f'-o:{output_path}'])
if not output_path.exists():
    raise Exception('output does not exist.')
