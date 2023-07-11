# replace elements to harmonise to shared vocabularies or entity authorities.

import pathlib
import pydash
import rdflib

graph_path = pathlib.Path.cwd() / 'bnfa' / 'rdf' / 'bnfa.ttl'
graph = rdflib.Graph().parse(graph_path)
print(len(graph))

country_property = rdflib.URIRef('https://fiafcore.org/ontology/hasCountry')
countries = pydash.uniq([o for s,p,o in graph.triples((None, country_property, None))])
print(countries)

output_path = pathlib.Path.cwd() / 'bnfa' / 'output' / 'bnfa.ttl'
graph.serialize(destination=str(output_path), format="turtle")

