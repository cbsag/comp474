
import nltk
CFG_gram="""
    % start S
    S[SEM=(SELECT+?np + 'WHERE{ ?a rdfs:label'+ ?np +'.'+?vp+'.?a}')] -> NP[SEM=?np] VP[SEM=?vp]
    S[SEM=(SELECT+?np + 'WHERE{ ?a rdfs:label'+ ?np +'.'+?vp+'?a.}')] -> PP[SEM=?np] VP[SEM=?vp]


    NP[SEM=?np] -> Verb[] NP[SEM=?np]
    NP[SEM=?np] -> DT NP[SEM=?np]
    NP[SEM=?np] -> WDT NP[SEM=?np]
    NP[SEM=('"'+?l + ?r+'"')] -> NNP[SEM=?l] NP[SEM=?r]
    NP[SEM=('"'+?l + ?r+'"')] -> NN[SEM=?l] NP[SEM=?r]
    NP[SEM=?l] -> NN[SEM=?l]
    NP[SEM=?l] -> NNP[SEM=?l]

    VP[SEM=('?x rdfs:label '+ ?o+'.?x'+?p)] -> Verb[SEM=?p] PP[SEM=?o]
    VP[SEM=('?x rdfs:label '+ ?o+'.?x'+?p)] -> Verb[-VB] NP[SEM=?o] Verb[SEM=?p]
    PP[SEM=?o] -> IN NP[SEM=?o]
    




    Verb[-VB] -> 'List' | 'is'
    NN[SEM='?courses'] -> 'courses'
    Verb[SEM='belongs_to'] -> 'offered'
    Verb[SEM='covered_in'] -> 'discussed'
    DT -> 'all'
    WDT -> 'which'
    IN -> 'by' |'In'
    NNP[SEM='Concordia'] -> 'Concordia'
    NNP[SEM='University'] -> 'University'
    NN[SEM='Knowledge'] -> 'Knowledge'
    NN[SEM='graph'] ->   'graph'


"""

# # grammar=nltk.CFG.fromstring(CFG_gram)
# # # Create a parser
# # parser = nltk.ChartParser(grammar)

# # # Input text
# # sentence = "List all courses offered by Concordia university"

# # # Tokenize the input text
# # tokens = sentence.split()

# # # Parse the text
# # for tree in parser.parse(tokens):
# #     print(tree)
# #     tree.pretty_print()

# import nltk

# # CFG_gram="""
# # S[SEM=(?np + WHERE + ?vp)] -> NP[SEM=?np] VP[SEM=?vp]
# # NP[SEM=?np] -> Verb NP[SEM=?np]
# # NP[SEM=?np] -> DT Noun[SEM=?np]
# # NP[SEM=(?l + ?r)] -> NNP[SEM=?l] NP[SEM=?r]
# # NP[SEM=(?l] -> NNP[SEM=?l]
# # VP[SEM=(?p + ?o),+VB] -> Verb[SEM=?p] PP[SEM=?o,+VB]
# # PP[SEM=?o,+VB] -> IN NP[SEM=?o]

# # Verb -> 'List'
# # Noun[SEM='cour'] -> 'courses'
# # Verb[SEM=belongs_to] -> 'offered'
# # DT -> 'all'
# # IN -> 'by'
# # NNP[SEM='Concordia'] -> 'Concordia'
# # NNP[SEM='University'] -> 'University'
# # """

# grammar=nltk.grammar.FeatureGrammar.fromstring(CFG_gram)

# # Create a parser
# parser = nltk.parse.FeatureEarleyChartParser(grammar,trace=2)

# # Input text
# sentence = "List all courses offered by Concordia University"

# # Tokenize the input text
# tokens = sentence.split()

# # Parse the text
# for tree in parser.parse(tokens):
#     print("here")
#     print(tree)
#     tree.pretty_print()

# import nltk

# Define your feature-based grammar
# FCFG_gram="""
# S[SEM=(?np + 'WHERE' + ?vp)] -> NP[SEM=?np] VP[SEM=?vp]
# NP[SEM=?np] -> Verb NP[SEM=?np]
# NP[SEM=?np] -> DT Noun[SEM=?np]
# NP[SEM=(?l + ?r)] -> NNP[SEM=?l] NP[SEM=?r]
# NP[SEM=(?l)] -> NNP[SEM=?l]
# VP[SEM=(?p + ?o)] -> Verb[SEM=?p] PP[SEM=?o]
# PP[SEM=?o] -> IN NP[SEM=?o]

# Verb -> 'List'
# Noun[SEM=?courses] -> 'courses'
# Verb[SEM=belongs_to] -> 'offered'
# DT -> 'all'
# IN -> 'by'
# NNP[SEM='Concordia'] -> 'Concordia'
# NNP[SEM='University'] -> 'University'
# """
from nltk import load_parser
# Load the FCFG grammar
grammar = nltk.grammar.FeatureGrammar.fromstring(CFG_gram)

# Create a chart parser
parser = nltk.FeatureEarleyChartParser(grammar,trace=2)

# Input text
sentence = "In which courses is Knowledge graph discussed"

# Tokenize the input text
tokens = sentence.split(" ")

# Parse the text
for tree in parser.parse(tokens):
    print(tree)
    #tree.pretty_print()