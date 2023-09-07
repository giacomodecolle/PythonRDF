from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS

# Define namespaces
obo = Namespace("http://purl.obolibrary.org/obo/")
# Add more namespaces if needed

# Create an RDF graph
g = Graph()

# Load your OWL/Turtle file
file_path = "/home/giacomo/Downloads/REPOS 2/OccO-main/occoturtle.ttl"  # Replace with the actual file path
g.parse(file_path, format="ttl")

# Initialize a list to store non-compliant subjects
non_aristotelian_subjects = []

# Iterate through triples with obo:IAO_0000115 predicate
for subject, predicate, obj in g.triples((None, obo.IAO_0000115, None)):
    if not isinstance(obj, Literal):
        continue  # Skip if the object is not a literal

    definition = obj.value

    # Split the definition into words
    words = definition.split()

    # Check if the subject is a subclass of skill
    is_subclass_of_skill = (subject, RDFS.subClassOf, obo.OCCO_00000003) in g

    if not is_subclass_of_skill:
        continue  # Skip if the subject is not a subclass of skill

    # Find the parent class by checking the label of the class that is the object of rdf:type
    parent_class = None
    for class_obj in g.objects(subject, RDFS.subClassOf):
        for label in g.objects(class_obj, RDFS.label):
            if isinstance(label, Literal):
                parent_class = label.value
                break

    if parent_class is None:
        print(f"Parent class label not found for subject: {subject}")
        continue

    # Check if the parent class exists in the words list
    if parent_class not in words:
        non_aristotelian_subjects.append(subject)  # Store non-compliant subject
        # Modify the definition to prepend "A skill that is realized in" with the first letter lowercase
        modified_definition = f"A skill that is realized in {definition[0].lower()}{definition[1:]}"
        g.set((subject, obo.IAO_0000115, Literal(modified_definition)))

# Serialize the modified graph to a file (optional)
g.serialize("/home/giacomo/Downloads/REPOS 2/OccO-main/occoturtlemodified.ttl", format="ttl")
