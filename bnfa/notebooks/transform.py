# pull source input XML and convert to transformed XML via XSL.

import pathlib
import subprocess

saxon_path = pathlib.Path.cwd() / 'saxon' / 'saxon-he-12.3.jar'
if not saxon_path.exists():
    raise Exception('saxon does not exist.')

source_path = pathlib.Path.cwd() / 'bnfa' / 'input' / '0.xml'
if not source_path.exists():
    raise Exception('source does not exist.')

transform_path = pathlib.Path.cwd() / 'bnfa'  / '20230601_BNFA-RDF-XML_withoutComments.xsl'
if not transform_path.exists():
    raise Exception('transform does not exist.')

output_path = pathlib.Path.cwd() / 'bnfa' / 'transform' / '0.xml'
subprocess.call(['java', '-jar', str(saxon_path), f'-s:{source_path}', f'-xsl:{transform_path}', f'-o:{output_path}'])
if not output_path.exists():
    raise Exception('output does not exist.')
