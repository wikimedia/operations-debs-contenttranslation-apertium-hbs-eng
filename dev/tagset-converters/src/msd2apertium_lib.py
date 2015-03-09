# !coding=utf-8
'''
    Skripta koja učitava MSD tag i konvertira ga u CGPOS-ov tagset
    (Ili takvo nešto, sigurno sadrži funkcije koje to rade)
'''

import sys, logging
from lxml import etree

# Load the apertium verb lexicon
def loadApertiumVerbLexicon():
    '''
    Loads the apertium verb lexicon, if provided with this script.
    Returns a dictionary containing for each verb whether it's
        - transitive
        - intransitive
        - reflexive
        - perfective / imperfective
    '''
    apertium=dict()
    with open('apertium-sh-mk.vb.lexicon.txt','r') as f:
        ls=f.readlines()
        for l in ls:
            l=l.replace('\n','')
            i=l.split(',')
            if i[0] in apertium:
                for j in i[1:]: apertium[i[0]].add(j)
            else:
                apertium[i[0]]=set(i[1:])

    for i in apertium:
        if ('imperf' in apertium[i]) and ('perf' in apertium[i]):
            apertium[i].remove('imperf')
            apertium[i].remove('perf')
            apertium[i].add('dual')

    return apertium;

def loadCrovalex():
    '''
    Parses the CROVALLEX verb lexicon, if provided, returns the dictionary
    containing aspect, reflexivity and transitivity for each verb.

    '''
    korien=etree.parse(open('../crovallex/CROVALLEX.xml')).getroot()
    crovalex=dict()
    for es in korien.iter('word_entry'): # Za svaku riječ u CROVALLEX-u
        for lm in es.iter('headword_lemma'):

            l=lm.text.split()[0] # Nabrzaka izvući txt leme
            if not(l in crovalex):
                crovalex[l]=set()

            # Vid:
            if es.get('aspect')=='dual':
                crovalex[l].add('dual')
            elif es.get('aspect')=='inf':
                crovalex[l].add('imperf')
            elif es.get('aspect')=='fin':
                crovalex[l].add('perf')

            # Refleksivnost:
            if lm.get('reflexive')=='YES':
                if l in crovalex:
                    crovalex[l].add('ref')

            # Tranzitivnost: (kasnije čak možda valencija!)
            for fs in es.iter('frame_entry'):
                for fslots in fs.iter('frame_slots'):
                    for slot in fslots.iter('slot'):
                        if slot.get('functor')=='PAT':
                            for form in slot.iter('form'):
                                if form.get('type')=='direct_case' and form.get('case')=='4':
                                    crovalex[l].add('tv') # Ako se nađe neprijedložni akuzativ u ovom slotu dodaj oznaku za tranzitivnost
                                else:
                                    crovalex[l].add('iv') # Inače dodaj oznaku za intranzitivnost
                    # Ako ne postoji slot s funktorom 'PAT', onda dodaj intranzitivnost (Do toga će doći )
                    # (tj. ako nakon što je prošao sve slotove nema ni tv ni iv u dictionariju, onda je iv)
                    if not('tv' in crovalex[l]) and not('iv' in crovalex[l]):
                        crovalex[l].add('iv')

            return crovalex;

def enrichVerb(lm, tags, additionalVerbLexicons):
    """
        Funkcija uzima CGPOS tag, zajedno s lemom i dodaje tv/iv/rfx
            (prvo to pokušava iz CROVALLEX-a, a zatim iz apertium-sh-mk -a)

        input:
            lm - the words lemma
            tags - A set of apertium tags
            additionalVerbLexicons - an array of lexicons used to enric the verb entries

        output:
            Vraća tags (koji je nb promijenio)
    """

    # Skip non-verb entries:
    if not('vb' in tags) and not('vblex' in tags) and not('vbmod' in tags) and not('vbaux' in tags):
        return tags # Ako nije glagol u pitanju, onda vraća tags

    for lexicon in additionalVerbLexicons:
        if lm in lexicon:
            for attr in lexicon[lm]:
                tags.append(attr);
                logger.trace('Added tag ' + attr + 'to the lemma ' +lm);
    else:
        tags.append('tv?') # Inače dodaj ovu oznaku da 'valencija' nije poznata
        #print 'ne dodah ništa ni iz čega'

    return tags
#==================================================================
def msd2apertium(tag):
    """
        Uzima MSD tag i pretvara ga u oznake koje se koriste u CGPOS-u za Hrvatski

        Input: MSD tag

        Output: tags kao set s običnim tagovima
    """
    tags = list() # Output set
    maxAttr=12 # max. indeks MSD atributa

    #print '[msd2apertium]',tag

    if len(tag)<maxAttr+1:
        for i in range(maxAttr+1-len(tag)):
            tag=tag+''.join(['-' for i in range(maxAttr+1-len(tag))])

    # Kvazi stejt mašina za obradu:

    # Noun:
    if tag[0]=='N':
        tags.append('n') # Noun
        #if tag[1]=='c': tags.append('com') # Common
        if tag[1]=='p': tags.append('prp') # Proper

        if tag[2]=='m':
            if len(tag)<=8: # If the animacy tag exists
                if tag[7]=='y': tags.append('ma') # Masculine animate
                elif tag[7]=='n': tags.append('mi') # Masculine inanimate
                else:
                    tags.append('m') # Just Masculine
            else:
                tags.append('m') # Just Masculine
        if tag[2]=='f': tags.append('f') # Feminine
        if tag[2]=='n': tags.append('nt') # Neuter

        if tag[3]=='s': tags.append('sg') # Singular
        if tag[3]=='p': tags.append('pl') # Plural

        if tag[4]=='n': tags.append('nom') # Nominative
        if tag[4]=='g': tags.append('gen') # Genitive
        if tag[4]=='d': tags.append('dat') # Dative
        if tag[4]=='a': tags.append('acc') # Accusative
        if tag[4]=='v': tags.append('voc') # Vocative
        if tag[4]=='l': tags.append('loc') # Locative
        if tag[4]=='i': tags.append('ins') # Instrumental
    # Verb:
    if tag[0]=='V':
        if tag[1]=='m': tags.append('vblex') # Lexical (main)
        elif tag[1]=='a': tags.append('vbaux') # Auxilliary
        elif tag[1]=='o': tags.append('vbmod') # Modal
        elif tag[1]=='c': tags.append('vbcop') # Coupla (vbser in apertum)
        else: tags.append('vb') # Verb

        #if tag[2]=='i': tags.append('Indicative') # Indicative is default
        if tag[2]=='m': tags.append('imp') # Imperative
        if tag[2]=='c': tags.append('cnd') # Conditional
        if tag[2]=='n': tags.append('inf') # Infinitive
        if tag[2]=='p': tags.append('pp') # Participle

        if tag[3]=='p': tags.append('pres') # Present
        if tag[3]=='i': tags.append('ipf') # Imperfect
        if tag[3]=='f': tags.append('futI') # Future
        if tag[3]=='s': tags.append('pst') # Past
        if tag[3]=='l': tags.append('pqp') # Pluperfect
        if tag[3]=='a': tags.append('aor') # Aorist

        if tag[4]=='1': tags.append('p1') # 1st person
        if tag[4]=='2': tags.append('p2') # 2nd person
        if tag[4]=='3': tags.append('p3') # 3rd person

        if tag[5]=='s': tags.append('sg') # Singular
        if tag[5]=='p': tags.append('pl') # Plural

        # The animacy tag makes no sence for verbs
        if tag[6]=='m': tags.append('m') # Just Masculine
        if tag[6]=='f': tags.append('f') # Feminine
        if tag[6]=='n': tags.append('nt') # Neuter

        if tag[7]=='a': tags.append('act') # Active
        if tag[7]=='p': tags.append('psv') # Passive

        # Some symbols here are shorthands (i.e. lp, l-participle which is pp+pst+act)
        if ('pp' in tags) and ('pst' in tags) and('act' in tags):

            tags.remove('pp')
            tags.remove('pst')
            tags.remove('act')

            tags.append('lp') # Shorthand for pp + pst + act (past active participle, the l-participle)

        if ('pp' in tags) and ('pst' in tags) and('psv' in tags):

            tags.remove('pp')
            tags.remove('pst')
            tags.remove('psv')

            tags.append('ppsv') # Shorthand for pp + pst + act (past passive participle, the verbal passive adjective)

    # Adjective
    if tag[0]=='A':
        tags.append('adj') # Adjective
        # if tag[1]=='f': tags.append('Qualificative') # The qualificative meaning is default
        if tag[1]=='s': tags.append('pos') # Possesive

        # if tag[2]=='p': tags.append('Positive') # The positive meaning is default
        if tag[2]=='c': tags.append('comp') # Comparative
        if tag[2]=='s': tags.append('sup') # Superlative

        if tag[3]=='m':
            if len(tag)<=9:
                if tag[8]=='y': tags.append('ma') # Masculine animate
                elif tag[8]=='n': tags.append('mi') # Masculine inanimate
                else:
                    tags.append('m') # Just Masculine
            else:
                tags.append('m') # Just Masculine
        if tag[3]=='f': tags.append('f') # Feminine
        if tag[3]=='n': tags.append('nt') # Neuter

        if tag[4]=='s': tags.append('sg') # Singular
        if tag[4]=='p': tags.append('pl') # Plural

        if tag[5]=='n': tags.append('nom') # Nominative
        if tag[5]=='g': tags.append('gen') # Genitive
        if tag[5]=='d': tags.append('dat') # Dative
        if tag[5]=='a': tags.append('acc') # Accusative
        if tag[5]=='v': tags.append('voc') # Vocative
        if tag[5]=='l': tags.append('loc') # Locative
        if tag[5]=='i': tags.append('ins') # Instrumental

        if tag[6]=='y': tags.append('def') # Definite
        # if tag[6]=='n': tags.append('Indefinite') # The indefinite meaning is default
    # Pronoun
    if tag[0]=='P':
        tags.append('prn') # Pronoun
        if tag[1]=='p': tags.append('pers') # Personal
        if tag[1]=='d': tags.append('dem') # Demonstrative
        if tag[1]=='i': tags.append('ind') # Indefinite
        if tag[1]=='s': tags.append('pos') # Possesive
        if tag[1]=='q': tags.append('int') # Interrogative
        if tag[1]=='r': tags.append('rel') # Relative
        if tag[1]=='x': tags.append('rfx') # Reflexive

        if tag[2]=='1': tags.append('p1') # 1st person
        if tag[2]=='2': tags.append('p2') # 2nd person
        if tag[2]=='3': tags.append('p3') # 3rd person

        if tag[3]=='m':
            if len(tag)<=13:
                if(tag[12]=='y'):tags.append('ma') # Masculine animate
                elif(tag[12]=='n'):tags.append('mi') # Masculine inanimate
                else:
                    tags.append('m') # Just Masculine
            else:
                tags.append('m') # Just Masculine
        if tag[3]=='f': tags.append('f') # Feminine
        if tag[3]=='n': tags.append('nt') # Neuter

        if tag[4]=='s': tags.append('sg') # Singular
        if tag[4]=='p': tags.append('pl') # Plural

        if tag[5]=='n': tags.append('nom') # Nominative
        if tag[5]=='g': tags.append('gen') # Genitive
        if tag[5]=='d': tags.append('dat') # Dative
        if tag[5]=='a': tags.append('acc') # Accusative
        if tag[5]=='v': tags.append('voc') # Vocative
        if tag[5]=='l': tags.append('loc') # Locative
        if tag[5]=='i': tags.append('ins') # Instrumental

        if tag[6]=='s': tags.append('osg') # Owner Singular
        if tag[6]=='p': tags.append('opl') # Owner Plural

        if tag[7]=='m': tags.append('om')# Owner Masculine
        if tag[7]=='f': tags.append('of')# Owner Masculine
        if tag[7]=='n': tags.append('ont')# Owner Masculine

        if tag[8]=='y': tags.append('clt') # Clitic
        #if tag[8]=='n': tags.append('Non-clitic')# Non-clitic is default

        if tag[9]=='p': tags.append('refpers') # Referent personal
        if tag[9]=='s': tags.append('refpos') # Referent personal

        # if tag[10]=='n': tags.append('Nominal') # Nominal is default
        if tag[10]=='a': tags.append('adj') # Adjectival
    # Adverb
    if tag[0]=='R':
        tags.append('adv') # Adverb
        # if tag[1]=='g': tags.append('General') # There is no other type defined besides general. Implementation specific

        # if tag[2]=='p': tags.append('Positive') # The positive meaning is default
        if tag[2]=='c': tags.append('comp') # Comparative
        if tag[2]=='s': tags.append('sup') # Superlative
        # TODO: For the adverbs which can also be analysed as adjectives either add a an adv adj analysis or just merge them in the CG
    # Adposition
    if tag[0]=='S':
        #tags.append('Adposition') # Adposition

        if tag[1]=='p': tags.append('pr') # Preposition

        # if tag[2]=='s': tags.append('Simple') # Simple is default
        if tag[2]=='c': tags.append('cpx') # Compound

        if tag[3]=='g': tags.append('gen') # Genitive
        if tag[3]=='d': tags.append('dat') # Dative
        if tag[3]=='a': tags.append('acc') # Accusative
        if tag[3]=='l': tags.append('loc') # Locative
        if tag[3]=='i': tags.append('ins') # Instrumental

    # Conjunction
    if tag[0]=='C':
        tags.append('cnj') # Conjunction

        # TODO: Perhaps turn those two tags back to cnjcoo and cnjsub, perhaps not
        if tag[1]=='c': tags.append('coo') # Coordinating
        if tag[1]=='s': tags.append('sub') # Subordinating

        # if tag[2]=='s': tags.append('Simple') # Simple is default
        if tag[2]=='c': tags.append('cpx') # Compound

    # Numeral
    if tag[0]=='M':
        tags.append('num') # Numeral

        if tag[1]=='c': tags.append('crd') # Cardinal
        if tag[1]=='o': tags.append('ord') # Ordinal
        if tag[1]=='m': tags.append('mlt') # Multiple
        if tag[1]=='s': tags.append('spc') # Special

        if tag[2]=='m':
            if len(tag)<=10:
                if(tag[9]=='y'):tags.append('ma') # Masculine animate
                elif(tag[9]=='n'):tags.append('mi') # Masculine inanimate
                else:
                    tags.append('m') # Just Masculine
            else:
                tags.append('m') # Just Masculine
        if tag[2]=='f': tags.append('f') # Feminine
        if tag[2]=='n': tags.append('nt') # Neuter

        if tag[3]=='s': tags.append('sg') # Singular
        if tag[3]=='p': tags.append('pl') # Plural

        if tag[4]=='n': tags.append('nom') # Nominative
        if tag[4]=='g': tags.append('gen') # Genitive
        if tag[4]=='d': tags.append('dat') # Dative
        if tag[4]=='a': tags.append('acc') # Accusative
        if tag[4]=='v': tags.append('voc') # Vocative
        if tag[4]=='l': tags.append('loc') # Locative
        if tag[4]=='i': tags.append('ins') # Instrumental

        # if tag[5]=='d': tags.append('dgt') # Digit is default
        if tag[5]=='r': tags.append('rom') # Roman
        if tag[5]=='l': tags.append('ltr') # Letter # This does not seem to be implemented in HML
    # Particle
    if tag[0]=='Q':
        tags.append('part') # Particle
        if tag[1]=='z': tags.append('neg') # Negative
        if tag[1]=='q': tags.append('itg') # Interrogative
        if tag[1]=='o': tags.append('mod') # Modal
        if tag[1]=='r': tags.append('aff') # Affirmative
    # Interjection
    if tag[0]=='I':
        tags.append('ij') # Interjection

        # if tag[1]=='s': tags.append('Simple') # Simple is default
        if tag[1]=='c': tags.append('cpx') # Compound
    # Abbreviation
    if tag[0]=='Y':
        tags.append('abbr') # Abbreviation

        if tag[1]=='n': tags.append('nom') # Nominal
        if tag[1]=='r': tags.append('adv') # Adverbial

        if tag[3]=='m': tags.append('m') # Just Masculine
        if tag[2]=='f': tags.append('f') # Feminine
        if tag[2]=='n': tags.append('nt') # Neuter

        if tag[3]=='s': tags.append('sg') # Singular
        if tag[3]=='p': tags.append('pl') # Plural

        if tag[4]=='n': tags.append('nom') # Nominative
        if tag[4]=='g': tags.append('gen') # Genitive
        if tag[4]=='d': tags.append('dat') # Dative
        if tag[4]=='a': tags.append('acc') # Accusative
        if tag[4]=='v': tags.append('voc') # Vocative
        if tag[4]=='l': tags.append('loc') # Locative
        if tag[4]=='i': tags.append('ins') # Instrumental
    # Residual
    if tag[0]=='tags':
        tags.append('res') # Residual

    ##print "Ovako izgleda cijeli tag: ", tag

    return tags

def listToTags(taglist):
    joined = "><".join(taglist)
    return "<" + joined + ">"

