#!/usr/bin/python

from SPARQLWrapper import SPARQLWrapper, JSON
from Levenshtein import ratio
import math

sparql = SPARQLWrapper("http://94.23.12.201:3030/stcn/sparql")
sparql.setQuery("""
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX stcn: <http://stcn.data2semantics.org/vocab/>

SELECT DISTINCT ?title ?author ?publisher ?year ?s
FROM <http://knuttel.data2semantics.org>
WHERE {
?s dc:title ?title .
OPTIONAL {
?s foaf:name ?author ;
   dc:publisher ?publisher ;
   stcn:prohibitionYear ?year .
}
}
""")

sparql.setReturnFormat(JSON)
print 'Launching SPARQL query...'
resultsKnuttel = sparql.query().convert()
print 'Done.'

sparql.setQuery("""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX vocab: <http://stcn.data2semantics.org/vocab/resource/>

SELECT DISTINCT ?title ?author ?publisher ?year ?p
FROM <http://stcn.data2semantics.org> 
WHERE {
?p rdf:type vocab:Publicatie ;
            rdfs:label ?title .
OPTIONAL {
?publication vocab:first_author ?a ;
             vocab:drukker ?d ;
             vocab:jaar ?j .
?a rdfs:label ?author .
?d rdfs:label ?publisher .
?j rdfs:label ?year .
}
}
""")

sparql.setReturnFormat(JSON)
print 'Launching SPARQL query...'
resultsSTCN = sparql.query().convert()
print 'Done.'

# print 'Computing similarities, {} x {} pairs...'.format(resultsKnuttel, resultsSTCN)
for y in resultsKnuttel["results"]["bindings"]:
    max_r = 0
    close_title = ""
    for x in resultsSTCN["results"]["bindings"]:
        if "title" in y and "title" in x:
            r_title = ratio(x["title"]["value"],
                            y["title"]["value"])
            print x["title"]["value"], y["title"]["value"], r_title
            if r_title > max_r:
                max_r = r
                close_title = y["title"]["value"]
    print "Best match of", x["title"]["value"], "is", close_title
