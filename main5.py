# initialise the methods class

from  methods_main3 import *
from methods_main2 import *
import time
start = time.time()


crashIt = False
# open the dataClass
path ="C:\\userOne\\keyPhraseExtraction-master\\keyPhraseExtraction-master\\AutomaticKeyphraseExtraction-master\\data\\"
methods1 = processMethods()
methods = mainMethods(path)


# extract the file references
methods.extractFileNames(path)
# extract all file names associated with handles
methods.df['fileNames'] = methods.df.handle.apply(methods.extractFiles)
# extract the content
methods.df['files'] = methods.df.fileNames.apply(methods.extractContent)
# extract text
methods.df['sanitiseData'] = methods.df.files.apply(methods1.cleanData)
print("creating tfidf of terms")

tfidf_matrix, tfidf_vectoriser = methods.applyTFidfToCorpus(methods.df.sanitiseData, failSafe = crashIt)
# store as class variables
methods.tfidf_matrix = tfidf_matrix
methods.tfidf_vectoriser = tfidf_vectoriser
# creates a dictionary of every term in the corpus
methods.df['termsDict'] = methods.df.sanitiseData.apply(methods.termCountDictionaryMethod)
# creates and overall dictionary count
methods.df.termsDict.apply(methods.amalgamateAllDocTermDictionaries)
# extract the keywords
methods.df['keywords'] = methods.df.handle.apply(methods.extractKeyWordFiles)
methods.df['competition_terms'] = methods.df.handle.apply(methods.extractKeyWordFilesTerms)

# extract the tfidf and assign per document
df = methods.ExtractSalientTerms(methods.tfidf_vectoriser, methods.tfidf_matrix, title = "tfidf_.pkl",  failSafe = crashIt)
#df['idfTerms'] = methods.df.index.apply(extractIdfTermsDoc)
methods.allTermIDFList = df
methods.df['tfidf_list'] = methods.df.handle.apply(methods.extractIdfTermsDoc)

print(10*"===")

print(list(methods.df.tfidf_list[0].items())[:5])
print(methods.df.keywords[0])

methods.df.keywords.apply(methods.lemmatiseCompTerms)

list= methods.df.keywords[0]



print(10*"===")

print(10*"-*-")
print((time.time() - start)/60)
