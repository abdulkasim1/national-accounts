import rdflib
import json
from rdflib import URIRef, Literal
from rdflib.namespace import RDF, RDFS
import click

def generate_turtle_from_json_file(json_file_path, output_file):
    # Create an RDF graph
    g = rdflib.Graph()

    # Define namespaces
    skos = rdflib.Namespace("http://www.w3.org/2004/02/skos/core#")
    rdfs = rdflib.Namespace("http://www.w3.org/2000/01/rdf-schema#")
    rdf = rdflib.Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    owl = rdflib.Namespace("http://www.w3.org/2002/07/owl#")
    cl = rdflib.Namespace("https://example.org/productclassification#")
    xkos = rdflib.Namespace("http://rdf-vocabulary.ddialliance.org/xkos#")

    # Add prefixes to the graph
    g.bind("skos", skos)
    g.bind("rdfs", rdfs)
    g.bind("rdf", rdf)
    g.bind("owl", owl)
    g.bind("cl", cl)
    g.bind("xkos", xkos)

    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

        # Extract concepts from the "concepts" array
        concepts = json_data.get("concepts", [])
        code_list_title = json_data["title"].lower().replace(" ", "")

        for concept_data in concepts:
            # Create the ConceptScheme for each concept
            concept_scheme = URIRef(f"example.org/{code_list_title}")
            g.add((concept_scheme, rdfs.label, Literal(json_data["title"], lang="en")))
            g.add((concept_scheme, RDF.type, skos.ConceptScheme))
            
            concept = URIRef(f"{cl}{concept_data['notation']}")
            g.add((concept, RDF.type, skos.Concept))
            g.add((concept, skos.prefLabel, Literal(concept_data["label"])))
            g.add((concept, skos.inScheme, concept_scheme))

            if "children" in concept_data:
                # Create Concepts and add them to the graph
                for child in concept_data["children"]:
                    concept = URIRef(f"{cl}{child['notation']}")
                    g.add((concept, RDF.type, skos.Concept))
                    g.add((concept, skos.prefLabel, Literal(child["label"])))
                    g.add((concept, skos.inScheme, concept_scheme))
    
                # Create xkos:hasPart and owl:unionOf relationships
                has_part = cl[concept_data["notation"]]
                for child in concept_data["children"]:
                    g.add((has_part, xkos.hasPart, cl[child["notation"]]))

                """union_of = cl[concept_data["notation"]]
                for child in concept_data["children"]:
                    g.add((union_of, owl.unionOf, cl[child["notation"]]))"""

    # Serialize the graph to the specified output file
    g.serialize(output_file, format="turtle")

    print(f"RDF data has been serialized to {code_list_title}.ttl")

# Specify the path to your JSON file and the output file
json_file_path = "/Users/abdulkasim/Documents/data_ingestion_projects/national-accounts/codelists/product_classification.json"
output_turtle_file = "/Users/abdulkasim/Documents/data_ingestion_projects/national-accounts/rdf/product_classification.ttl"

# Generate Turtle file from the JSON file
generate_turtle_from_json_file(json_file_path, output_turtle_file)

