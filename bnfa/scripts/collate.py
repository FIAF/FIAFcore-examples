# pull rdf fragments into single turtle file.

import pathlib
import rdflib

transform_dir = pathlib.Path.cwd() / 'bnfa' / 'transform'
transform_files = [x for x in transform_dir.iterdir() if x.suffix == '.xml']

graph = rdflib.Graph()        
for transform_path in transform_files:
    graph += rdflib.Graph().parse(transform_path)

collate_path = pathlib.Path.cwd() / 'bnfa' / 'rdf' / 'bnfa.ttl'
graph.serialize(destination=str(collate_path), format="turtle")
