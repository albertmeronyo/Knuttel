from SPARQLWrapper import SPARQLWrapper, JSON
from Levenshtein import ratio
import math

print "@prefix owl: <http://www.w3.org/2002/07/owl#> ."

sparql = SPARQLWrapper("http://ops.few.vu.nl:8890/world")
sparql.setQuery("""
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX stcn: <http://stcn.data2semantics.org/vocab/>

SELECT ?title ?author ?publisher ?year ?s
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
# print 'Launching SPARQL query...'
resultsKnuttel = sparql.query().convert()
# print 'Done.'

sparql = SPARQLWrapper("http://ops.few.vu.nl:8890/world")
sparql.setQuery("""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX vocab: <http://stcn.data2semantics.org/vocab/resource/>

SELECT ?title ?author ?publisher ?year ?p
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
# print 'Launching SPARQL query...'
resultsSTCN = sparql.query().convert()
# print 'Done.'

# print 'Computing similarities, {} x {} pairs...'.format(resultsKnuttel, resultsSTCN)
for y in resultsKnuttel["results"]["bindings"]:
    for x in resultsSTCN["results"]["bindings"]:
        if "title" in x:
            x_title = x["title"]["value"].encode('utf8')
        else:
            x_title = ""
        if "author" in x:
            x_author = x["author"]["value"].encode('utf8')
        else:
            x_author = ""
        if "publisher" in x:
            x_publisher = "".join(x["publisher"]["value"].encode('utf8').split(',')[:-1])
        else:
            x_publisher = ""
        if "year" in x:
            try:
                x_year = int(x["year"]["value"].encode('utf8'))
            except ValueError:
                x_year = 0
        else:
            x_year = 0
        if "title" in y:
            y_title = y["title"]["value"].encode('utf8')
        else:
            y_title = ""
        if "author" in y:
            y_author = y["author"]["value"].encode('utf8')
        else:
            y_author = ""
        if "publisher" in y:
            y_publisher = y["publisher"]["value"].encode('utf8')
        else:
            y_author = ""
        if "year" in y:
            try:
                y_year = int(float(y["year"]["value"].encode('utf8')))
            except ValueError:
                y_year = 0
        else:
            y_year = 0
        if '(' in x["author"]["value"]:
            x_author = x["author"]["value"].encode('utf8').split('(')[0]
        if x_year == 0 or y_year == 0:
            r_year = 0
        else:
            diff_year = math.fabs(x_year - y_year)
            if diff_year < 5:
                r_year = 1
            else:
                r_year = 0
        r_title = ratio(x_title,
                        y_title)
        r_author = ratio(x_author,
                         y_author)
        r_publisher = ratio(x_publisher,
                            y_publisher)
        r = r_title + r_author + r_publisher + r_year
        if r > 1:
            #issue the mapping
            #print x_title, x_author, x_publisher, x_year
            #print y_title, y_author, y_publisher, y_year
            if "s" in x and "p" in y:
                print x["s"]["value"], "owl:sameAs", y["p"]["value"], "."
# print 'Done.'
