#!/usr/bin/python2.7

from SPARQLWrapper import SPARQLWrapper, JSON
from Levenshtein import ratio
import math

print "@prefix owl: <http://www.w3.org/2002/07/owl#> ."

sparql = SPARQLWrapper("http://94.23.12.201:3030/stcn/sparql")
sparql.setQuery("""
PREFIX dc: <http://purl.org/dc/elements/1.1/>

SELECT DISTINCT ?title ?s
FROM <http://weekhout.data2semantics.org>
WHERE {
?s dc:title ?title .
}
""")

sparql.setReturnFormat(JSON)
# print 'Launching SPARQL query...'
resultsWeekhout = sparql.query().convert()
# print 'Done.'

sparql.setQuery("""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX vocab: <http://stcn.data2semantics.org/vocab/resource/>

SELECT DISTINCT ?title ?p
FROM <http://stcn.data2semantics.org> 
WHERE {
?p rdf:type vocab:Publicatie ;
            rdfs:label ?title .
}
""")

sparql.setReturnFormat(JSON)
# print 'Launching SPARQL query...'
resultsSTCN = sparql.query().convert()
# print 'Done.'

# print "Computing similarities"
for y in resultsWeekhout["results"]["bindings"]:
    max_r = 0
    weekhout_title = y["title"]["value"]
    weekhout_uri = y["s"]["value"]
    close_title = ""
    close_uri = ""
    for x in resultsSTCN["results"]["bindings"]:
        stcn_title = x["title"]["value"]
        stcn_uri = x["p"]["value"]
        r_title = ratio(weekhout_title,
                        stcn_title)
        # print weekhout_title, stcn_title, r_title
        if r_title > max_r:
            max_r = r_title
            close_title = stcn_title
            close_uri = stcn_uri
    # print "Best match of", weekhout_title, "is", close_title
    if max_r > 0.9:
        print "<{}> owl:sameAs <{}> .".format(weekhout_uri, close_uri)
