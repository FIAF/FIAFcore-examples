# replace elements to harmonise to shared vocabularies or entity authorities.

import json
import pathlib
import pydash
import rdflib

def check_transform(prop_value, transform_key):

    ''' Check transformation of entities will be possible. '''

    predicate = rdflib.URIRef(f'https://fiafcore.org/ontology/{prop_value}')
    vocab = pydash.uniq([o for s,p,o in graph.triples((None, predicate, None))])
    for x in vocab:
        if str(x) not in transform[transform_key].keys():
            raise Exception(str(x), 'transform not possible.')

# load transformations.

with open(pathlib.Path.cwd() / 'bnfa' / 'reconcile.json') as transform:
    transform = json.load(transform)
    
# load existing graph.

graph_path = pathlib.Path.cwd() / 'bnfa' / 'rdf' / 'bnfa.ttl'
graph = rdflib.Graph().parse(graph_path)

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

output_path = pathlib.Path.cwd() / 'bnfa' / 'output' / 'bnfa.ttl'
output_path.parents[0].mkdir(exist_ok=True)
new_graph.serialize(destination=str(output_path), format="turtle")