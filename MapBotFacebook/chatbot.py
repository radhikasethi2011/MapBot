from utilities import parse_sentence
from utilities import classify_model
from utilities import classify_sentence
from utilities import setup_database
from utilities import add_to_database
from utilities import get_chat_response
from utilities import get_question_response
from utilities import learn_question_response
from utilities import add_learnt_statement_to_database

def setup():
    clf = classify_model()
    setup_database()
    learn_response = 0
    return clf, learn_response

def message_to_bot(H,clf,learn_response):
    if H.lower() == "bye" or H.lower() == "bye." or H.lower() == "bye!":                                                                 #empty input
        B = "Bye! I'll miss you!"
        return B                                                                #exit loop
    #grammar parsing
    subj = set()
    obj = set()
    verb = set()
    triples,root = parse_sentence(H)
    triples = list(triples)
    for t in triples:
        if t[0][1][:2] == 'VB':
            verb.add(t[0][0])
        relation = t[1]
        if relation[-4:] == 'subj':
            subj.add(t[2][0])
        if relation[-3:] == 'obj':
            obj.add(t[2][0])
    #print("\t"+"Subject: "+str(subj)+"\n"+"\t"+"Object: "+str(obj)+"\n"+"\t"+"Topic: "+str(root)+"\n"+"\t"+"Verb: "+str(verb))
    subj = list(subj)
    obj = list(obj)
    verb = list(verb)
    proper_nouns = set()
    for t in triples:
        if t[0][1] == 'NNP':
            proper_nouns.add(t[0][0])
        if t[2][1] == 'NNP':
            proper_nouns.add(t[2][0])
    proper_nouns == list(proper_nouns)
    #print("\t"+"Proper Nouns: "+str(proper_nouns))
    #classification
    classification = classify_sentence(clf,H)
    #print(classification)
    if learn_response == 0:
        add_to_database(classification,subj,root,verb,H)
        if (classification == 'C'):
            B = get_chat_response()
        elif (classification == 'Q'):
            B,learn_response = get_question_response(subj,root,verb)
            if learn_response == 1:
                add_learnt_statement_to_database(subj,root,verb)
        else:
            B = "Oops! I'm not trained for this yet."
    else:
        B,learn_response = learn_question_response(H)
    return B,learn_response