#!/usr/bin/python2.7

from SPARQLWrapper import SPARQLWrapper, JSON
from Levenshtein import ratio
import math
import argparse

def restricted_float(x):
    x = float(x)
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 1.0]"%(x,))
    return x

parser = argparse.ArgumentParser()
parser.add_argument('-t', 
                    '--threshold', 
                    nargs=1, 
                    dest='t',
                    type=restricted_float,
                    default=[0.9], 
                    help='Levenshtein ratio threshold (0.9 if not specified)')
parser.add_argument('-e',
                    '--endpoint',
                    nargs=1,
                    dest='e',
                    required=True,
                    help='URL address of the SPARQL endpoint to query')
args = parser.parse_args()

print "@prefix owl: <http://www.w3.org/2002/07/owl#> ."

sparql = SPARQLWrapper(args.e[0])

sparql.setQuery("""
SELECT DISTINCT ?title ?s
FROM <http://knuttel.data2semantics.org>
WHERE {
?s <http://purl.org/dc/elements/1.1/title> ?title .
}
""")

sparql.setReturnFormat(JSON)
# print 'Launching SPARQL query...'
resultsKnuttel = sparql.query().convert()
# print 'Done.'

sparql.setQuery("""
SELECT DISTINCT ?title ?p
FROM <http://stcn.data2semantics.org> 
WHERE {
?p <http://www.w3.org/2000/01/rdf-schema#label> ?title .
}
""")

sparql.setReturnFormat(JSON)
# print 'Launching SPARQL query...'
resultsSTCN = sparql.query().convert()
# print 'Done.'

# print "Computing similarities"
for y in resultsKnuttel["results"]["bindings"]:
    max_r = 0
    knuttel_title = y["title"]["value"]
    knuttel_uri = y["s"]["value"]
    close_title = ""
    close_uri = ""
    for x in resultsSTCN["results"]["bindings"]:
        stcn_title = x["title"]["value"]
        stcn_uri = x["p"]["value"]
        r_title = ratio(knuttel_title,
                        stcn_title)
        # print knuttel_title, stcn_title, r_title
        if r_title > max_r:
            max_r = r_title
            close_title = stcn_title
            close_uri = stcn_uri
    # print "Best match of", knuttel_title, "is", close_title
    if max_r > args.t[0]:
        print "<{}> owl:sameAs <{}> .".format(knuttel_uri, close_uri)
