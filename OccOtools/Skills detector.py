from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, OWL, RDFS

# Define namespaces
obo = Namespace("http://purl.obolibrary.org/obo/")
# Add more namespaces if needed

# Create an RDF graph
g = Graph()

# Load your OWL/Turtle file
file_path = ""  # Replace with the actual file path
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
    is_subclass_of_capability = (subject, RDFS.subClassOf, obo.OCCO_00000003) in g

    if not is_subclass_of_capability:
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

    # Check if the parent class exists in the list of words
    if parent_class not in words:
        non_aristotelian_subjects.append(subject)  # Store non-compliant subject
        continue

    # Check if the first word after the parent class is "that" or "who"
    index_of_parent_class = words.index(parent_class)
    if (
        index_of_parent_class + 1 < len(words)
        and words[index_of_parent_class + 1] in {"that", "who"}
    ):
        continue  # Definition is compliant with Aristotelian model

    non_aristotelian_subjects.append(subject)  # Store non-compliant subject

# Print non-compliant subjects
if non_aristotelian_subjects:
    print("Non-Aristotelian definitions detected for the following subjects:")
    for subject in non_aristotelian_subjects:
        print(subject)
else:
    print("All definitions are compliant with the Aristotelian model.")
