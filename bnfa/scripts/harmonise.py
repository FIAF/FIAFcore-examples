# replace elements to harmonise to shared vocabularies or entity authorities.

import pathlib
import pydash
import rdflib

graph_path = pathlib.Path.cwd() / 'bnfa' / 'rdf' / 'bnfa.ttl'
graph = rdflib.Graph().parse(graph_path)
print(len(graph))


country_transform = {
    rdflib.URIRef('http://example.org/EFG/country/BG'): rdflib.URIRef('https://fiafcore.org/ontology/Bulgaria')}

new_graph = rdflib.Graph()

country_property = rdflib.URIRef('https://fiafcore.org/ontology/hasCountry')
countries = pydash.uniq([o for s,p,o in graph.triples((None, country_property, None))])
print(countries) # all countries

for x in countries:
    if x not in country_transform.keys():
        raise Exception(x, 'transform not possible.')


for s,p,o in graph.triples((None, None, None)):
    if s in country_transform.keys():
        s = country_transform[s]
    if p in country_transform.keys():
        p = country_transform[p]
    if o in country_transform.keys():
        o = country_transform[o]



    new_graph.add((s,p,o))



output_path = pathlib.Path.cwd() / 'bnfa' / 'output' / 'bnfa.ttl'
output_path.parents[0].mkdir(exist_ok=True)
new_graph.serialize(destination=str(output_path), format="turtle")

