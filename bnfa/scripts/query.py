# load graph and run some example sparql queries.

import pathlib
import rdflib

graph_path = pathlib.Path.cwd() / 'bnfa' / 'output' / 'bnfa.ttl'
graph = rdflib.Graph().parse(graph_path)

print('\n*** Example queries ***\n')

# 1. Find all documentaries. 
# Documentaries are not currently valid "forms", use Shorts instead

print('1. Find all short films.')
query = '''
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix fiaf: <https://fiafcore.org/ontology/>
    prefix efg_form: <http://example.org/EFG/form/>
    
    select distinct ?work ?work_label where {
        ?work a fiaf:WorkVariant .
        ?work fiaf:hasForm fiaf:Short .
        ?work rdfs:label ?work_label
        } '''

for x in graph.query(query):
    print(f"{x['work_label']} ({x['work']})")

print('\n2. Find all works where Vasil Gendov is credited.')

query = '''
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix fiaf: <https://fiafcore.org/ontology/>
     select distinct ?work ?work_label where {
        ?work a fiaf:WorkVariant .
        ?work rdfs:label ?work_label .
        ?work fiaf:hasEvent ?event .
        ?event  fiaf:hasActivity ?activity .
        ?activity fiaf:hasAgent <http://example.org/EFG/BNFA_person_c23e8010ec939b9649ceebc36798d890> .
        } '''

for x in graph.query(query):
    print(f"{x['work_label']} ({x['work']})")

print('\n3. Find all works from before 1930, where a 35mm copy exists.')

query = '''
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix fiaf: <https://fiafcore.org/ontology/>
    prefix xsd: <http://www.w3.org/2001/XMLSchema#>
    
    select distinct ?work ?work_label where {
        ?work	fiaf:hasEvent ?event .
        ?work rdfs:label ?work_label .
        ?event fiaf:hasEventDate ?date .
        filter(xsd:integer(?date) < 1930) .
        ?work fiaf:hasManifestation ?manifestation .
        ?manifestation fiaf:hasFormat fiaf:35mmFilm .
        ?manifestation fiaf:hasItem ?item .
        } '''

for x in graph.query(query):
    print(f"{x['work_label']} ({x['work']})")

print('\n# 4. Find all works shorter than 15 minutes.')

query = '''
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix fiaf: <https://fiafcore.org/ontology/>
    prefix xsd: <http://www.w3.org/2001/XMLSchema#>
    
    select distinct ?work  ?manifestation ?extent_type ?extent_value where {
        ?work fiaf:hasManifestation ?manifestation .
        ?manifestation fiaf:hasExtent ?extent .
        ?extent a ?extent_type .
        ?extent fiaf:hasExtentValue ?extent_value .
        filter(xsd:time(?extent_value) < xsd:time("00:15:00"))
        } '''

for x in graph.query(query):
    print(f"{x['work']} {x['manifestation']} {x['extent_value']}")

print('\n')

