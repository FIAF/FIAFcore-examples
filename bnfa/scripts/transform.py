# pull source input XML and convert to transformed XML via XSL.

import pathlib
import subprocess

saxon_path = pathlib.Path.cwd() / 'saxon' / 'saxon-he-12.3.jar'
if not saxon_path.exists():
    raise Exception('saxon does not exist.')

transform_path = pathlib.Path.cwd() / 'bnfa'  / '20230601_BNFA-RDF-XML_withoutComments.xsl'
if not transform_path.exists():
    raise Exception('transform does not exist.')

source_dir = pathlib.Path.cwd() / 'bnfa' / 'input'
source_files = [x for x in source_dir.iterdir() if x.suffix == '.xml']
for source_path in source_files:
    if not source_path.exists():
        raise Exception('source does not exist.')
    
    output_path = source_path.parents[1] / 'transform' / source_path.name
    subprocess.call(['java', '-jar', str(saxon_path), f'-s:{source_path}', f'-xsl:{transform_path}', f'-o:{output_path}'])
    if not output_path.exists():
        raise Exception('output does not exist.')
