import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_lg")
matcher = Matcher(nlp.vocab)

patternDP = [{"TEXT": "DP"}]
matcher.add("DP", None, patternDP)

doc = nlp(u"[CP[TP I [VP SAW [DP A CAT]]]]")
matches = matcher(doc)
for match_id, start, end in matches:
    string_id = nlp.vocab.strings[match_id]  # Get string representation
    span = doc[start:end]  # The matched span
    addNode