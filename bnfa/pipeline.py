# pull source input XML and convert to harmonised turtle via RDF/XML.

import json
import pathlib
import pydash
import rdflib
import subprocess

def check_transform(prop_value, transform_key):

    ''' Check transformation of entities will be possible. '''

    predicate = rdflib.URIRef(f'https://fiafcore.org/ontology/{prop_value}')
    vocab = pydash.uniq([o for s,p,o in graph.triples((None, predicate, None))])
    for x in vocab:
        if str(x) not in transform[transform_key].keys():
            raise Exception(str(x), 'transform not possible.')

saxon_path = pathlib.Path.cwd() / 'saxon' / 'saxon-he-12.3.jar'
if not saxon_path.exists():
    raise Exception('saxon does not exist.')

transform_path = pathlib.Path.cwd() / 'bnfa'  / '20230601_BNFA-RDF-XML_withoutComments.xsl'
if not transform_path.exists():
    raise Exception('transform does not exist.')

source_dir = pathlib.Path.cwd() / 'bnfa' / 'source'
source_files = [x for x in source_dir.iterdir() if x.suffix == '.xml']

# use saxon to process XML and combine into graph.

graph = rdflib.Graph() 
output_path = pathlib.Path.cwd() / 'bnfa' / 'bnfa-rdf.xml'
for source_path in source_files:
    subprocess.call(['java', '-jar', str(saxon_path), f'-s:{source_path}', f'-xsl:{transform_path}', f'-o:{output_path}'])
    graph += rdflib.Graph().parse(output_path)

# specifically parse enrichment data.

enrich = pathlib.Path.cwd() / 'bnfa' / 'source' / 'BNFA_Agents_enrichment.xml'
graph += rdflib.Graph().parse(enrich)

# load transformations.

with open(pathlib.Path.cwd() / 'bnfa' / 'reconcile.json') as transform:
    transform = json.load(transform)

# check transformations

check_transform('hasCountry', 'country')
check_transform('hasForm', 'form')  

# flatten and convert to URIRef.

flat_transform =  {rdflib.URIRef(k): rdflib.URIRef(v) for d in transform for k, v in transform[d].items()}

# find and replace transforms.

new_graph = rdflib.Graph()

for s,p,o in graph.triples((None, None, None)):
    if s in flat_transform.keys():
        s = flat_transform[s]
    if p in flat_transform.keys():
        p = flat_transform[p]
    if o in flat_transform.keys():
        o = flat_transform[o]
    new_graph.add((s,p,o))

# save harmonised graph.

output_path = pathlib.Path.cwd() / 'bnfa' / 'bnfa-processed.ttl'
new_graph.serialize(destination=str(output_path), format="turtle")