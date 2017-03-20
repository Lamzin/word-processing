import spacy
from spacy.symbols import nsubj, VERB


def main():
    'main'
    nlp = spacy.load('en')
    doc = nlp(u"Computer science is the newest area of science.")
    print retrieve_dependencies(doc)


def retrieve_dependencies(doc):
    'return list of all syntax dependencies in document'
    verbs = {token.head: 0 for token in doc if token.dep == nsubj and token.head.pos == VERB}

    i = 0
    dependencies = []
    queue = [k for k in verbs.keys()]
    while i < len(queue):
        for child in queue[i].children:
            queue.append(child)
            dependencies.append((queue[i], child.dep_, child))
        i += 1
    return dependencies


if __name__ == "__main__":
    main()
