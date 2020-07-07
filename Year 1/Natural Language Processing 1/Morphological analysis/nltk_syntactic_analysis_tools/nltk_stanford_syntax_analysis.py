import os
from nltk.parse.stanford import StanfordParser
from nltk.parse.stanford import StanfordDependencyParser
from nltk.tokenize import word_tokenize, sent_tokenize

cale_parser = '.\stanford-parser-full-2018-10-17\stanford-parser.jar'
cale_modele = '.\stanford-parser-full-2018-10-17\stanford-parser-3.9.2-models.jar'
os.environ['JAVAHOME'] = "C:/Program Files/Java/jdk-11.0.1/bin"
os.environ['STANFORD_PARSER'] = cale_parser
os.environ['STANFORD_MODELS'] = cale_modele

parser = StanfordParser(model_path=".\stanford-parser-full-2018-10-17\englishPCFG.ser.gz")
dependency_parser = StanfordDependencyParser(path_to_jar=cale_parser, path_to_models_jar=cale_modele)

info = 'The sequence of DNA that encodes the sequence of the amino acids in a protein, is transcribed into a messenger RNA chain. Ribosomes bind to messenger RNAs and use its sequence for determining the correct sequence of amino acids to generate a given protein. Amino acids are selected and carried to the ribosome by transfer RNA (tRNA) molecules, which enter the ribosome and bind to the messenger RNA chain via an anti-codon stem loop. For each coding triplet in the messenger RNA, there is a transfer RNA that matches and carries the correct amino acid for incorporating into a growing polypeptide chain. Once the protein is produced, it can then fold to produce a functional three-dimensional structure.'
props = sent_tokenize(info)

f = open("./nltk_stanford_syntax_analysis.txt", "w")


for i, prop in enumerate(props):
    #print('Sentence - number ' + str(i+1))
    f.write('Sentence - number ' + str(i+1) + '\n')
    #print(prop)
    f.write(prop)
    f.write('\n')
    const_pars = parser.raw_parse(prop)
    dep_pars = dependency_parser.raw_parse(prop)
    for con in const_pars:
        #print(list(con))
        f.write(str(list(con)))
    f.write('\n')
    for dep in dep_pars:
        #print(list(dep.triples()))
        f.write(str(list(dep.triples())))
    f.write('\n')
    #print('--------------------------------')
    f.write('--------------------------------\n')

f.close()