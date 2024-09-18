from rdflib import Graph, Namespace
from urllib.parse import unquote

TAG_NS = Namespace("https://sybille-reuter.de/tags/")

g = Graph()
g.parse("tags/tags.owl", format="xml")


def unquote_uri(uri):
    return unquote(str(uri).split("/")[-1].replace("_", " "))


def load_tags():
    query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT ?category ?subcategory ?tag
    WHERE {
        ?category a rdfs:Class .
        ?subcategory rdfs:subClassOf ?category .
        ?tag a ?subcategory .
    }
    """
    result = g.query(query)

    tags_dict = {}

    for row in result:
        category = unquote_uri(row.category)
        subcategory = unquote_uri(row.subcategory)
        tag = unquote_uri(row.tag)

        if category not in tags_dict:
            tags_dict[category] = {}

        if subcategory not in tags_dict[category]:
            tags_dict[category][subcategory] = []

        tags_dict[category][subcategory].append(tag)

    return tags_dict


def load_generic_tags():
    query = """
    PREFIX tag: <https://sybille-reuter.de/tags/>

    SELECT ?tag
    WHERE {
        ?tag a tag:Tag .
    }
    """
    result = g.query(query)

    generic_tags = [unquote_uri(row.tag) for row in result]
    return generic_tags


def load_categories():
    query = """
    PREFIX tag: <https://sybille-reuter.de/tags/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?category
    WHERE {
        ?category a tag:Category .
    }
    """
    result = g.query(query)

    categories = [unquote_uri(row.category) for row in result]
    return categories


tags_inventory = load_tags()
generic_tags = load_generic_tags()
categories = load_categories()

