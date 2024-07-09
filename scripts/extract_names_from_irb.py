import spacy

# Load the English spaCy model
nlp = spacy.load("en_core_web_lg")

# Your text here
text = """
Name
Financial Interests
Jiayi Smith, BA, MD
none
Christopher Johnson, BS, MD
none
"""

# Process the text using spaCy to extract names
doc = nlp(text)

# Print each unique name found by spaCy, excluding "MD" and "CCRC"
names_found = set()
for ent in doc.ents:
    if ent.label_ == "PERSON" and "MD" not in ent.text and "CCRC" not in ent.text:
        if ent.text not in names_found:
            print(ent.text)
            names_found.add(ent.text)

