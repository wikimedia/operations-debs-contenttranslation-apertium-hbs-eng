# !coding=utf-8

''' Tools and utils for parsing the conll format'''

import sys;

from msd2apertium_lib import msd2apertium, listToTags;

class Token:
    """
    Represents a conll token
        - token_id - the position inside the sentence (starting at 1)
        - form     - the surface form of the token
        - lemma    - the lemma of the token
        - cpostag  - course part of speech tag
        - postag   - fine grained part of speech tag
        - feats    - unordered set of features (w00t)
        - head     - dependency head of the current token (another token_id, or 0)
        - deprel   - dependency relation to the head
        - phead    - projective head (token_id, 0 or '_')
        - pdeprel  - dependency relation to the current projective head, or '_'
    """
    def __init__(self, token_id, form, lemma, cpostag, postag, feats, head, deprel, phead, pdeprel):
        self.token_id = token_id;
        self.form = form;
        self.lemma = lemma;
        self.cpostag = cpostag;
        self.postag = postag;
        self.feats = feats;
        self.head = head;
        self.deprel = deprel;
        self.phead = phead;
        self.pdeprel = pdeprel;

    @staticmethod
    def parse(line):
        """Parses a line, returns a token object"""
        tokenlist = line.split();
        if(len(tokenlist)<10): return None;

        token_id   = tokenlist[0];
        form       = tokenlist[1];
        lemma      = tokenlist[2];
        cpostag    = tokenlist[3];
        postag     = tokenlist[4];
        feats      = tokenlist[5];
        head       = tokenlist[6];
        deprel     = tokenlist[7];
        phead      = tokenlist[8];
        pdeprel    = tokenlist[9];

        return Token(token_id, form, lemma, cpostag, postag, feats, head, deprel, phead, pdeprel)

if(len(sys.argv) != 2):
    print
    print "Work in progress. Parse a CONLL file, and output something."
    print
    print "Usage:"
    print "\tpython " + sys.argv[0] + " a_conll_corpus_file"
    print
    sys.exit()

with open(sys.argv[1]) as f:
    for line in f:
        token = Token.parse(line.replace('\n', ''))
        if(token):
            print token.lemma + " " + listToTags(msd2apertium(token.postag))
