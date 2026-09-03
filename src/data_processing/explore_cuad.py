import json

json_path = "data/raw/CUAD_v1.json"

with open(json_path, "r", encoding="utf-8") as file:
    cuad = json.load(file)

contracts = cuad["data"]

print("=" * 60)
print("CUAD ANNOTATION EXPLORATION")
print("=" * 60)

print("\nNumber of contracts:", len(contracts))

# First contract
contract = contracts[0]

print("\nContract title:")
print(contract["title"])

# First paragraph
paragraphs = contract["paragraphs"]

print("\nNumber of paragraphs:", len(paragraphs))

paragraph = paragraphs[0]

print("\nParagraph keys:")
print(paragraph.keys())

print("\nParagraph text:")
print(paragraph["context"][:1000])

# Questions / annotations
qas = paragraph.get("qas", [])

print("\nNumber of annotations in this paragraph:")
print(len(qas))

if qas:

    first_question = qas[0]

    print("\nFirst annotation keys:")
    print(first_question.keys())

    print("\nClause category:")
    print(first_question.get("question"))

    print("\nAnnotation information:")
    print(first_question)