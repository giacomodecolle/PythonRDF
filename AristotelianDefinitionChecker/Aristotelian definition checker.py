from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS

# Define namespaces
obo = Namespace("http://purl.obolibrary.org/obo/")
# Add more namespaces if needed

# Create an RDF graph
g = Graph()

# Load your OWL/Turtle file
file_path = ""  # Replace with the actual file path, in .ttl format
g.parse(file_path, format="ttl")

# Initialize a list to store non-compliant subjects
non_aristotelian_subjects = []

# Iterate through triples with the designated definition predicate. In this file, I used obo.IAO_0000115,but you can substitute it with skos:definiton or whatever your ontology is using.
for subject, predicate, obj in g.triples((None, obo.IAO_0000115, None)):
    if not isinstance(obj, Literal):
        continue  # Skip if the object is not a literal

    definition = obj.value

    # Split the definition into words
    words = definition.split()

    # Find the parent class by checking the rdfs:label of the class that is the object of rdfs:subclass. You can also change this to use skos:prefLabel, etc.
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
        non_aristotelian_subjects.append((subject, parent_class, definition))  # Store non-compliant subject
        continue

    # Check if the first word after the parent class is "that" or "who" or "where"
    index_of_parent_class = words.index(parent_class)
    if (
        index_of_parent_class + 1 < len(words)
        and words[index_of_parent_class + 1] in {"that", "who", "where}
    ):
        continue  # Definition is compliant with Aristotelian model

    non_aristotelian_subjects.append((subject, parent_class, definition))  # Store non-compliant subject

# Create or open a Markdown file to write the list of non-compliant subjects. Substitute the three dots with desired path.
with open(".../non_compliant_subjects.md", "w") as md_file:
    if non_aristotelian_subjects:
        md_file.write("Non-Aristotelian definitions detected for the following subjects:\n")
        for subject, label, definition in non_aristotelian_subjects:
            md_file.write(f"- IRI: {subject}\n")
            md_file.write(f"  Label: {g.value(subject, RDFS.label)}\n")  # Get the label of the subject
            md_file.write(f"  Definition: {definition}\n")
    else:
        md_file.write("All definitions are compliant with the Aristotelian model.\n")

# Print a message indicating where the Markdown file is saved
print("Non-compliant subjects list saved to non_compliant_subjects.md")
