#importamos las librerías
import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import os

#nltk.download("wordnet")
#nltk.download('punkt_tab')
#nltk.download('averaged_perceptron_tagger_eng')
#nltk.download('omw-1.4')
#Creamos los objetos para usarlos más adelante
porter = PorterStemmer()
lancaster = LancasterStemmer()
snowball = SnowballStemmer('english')

def cosine_similarity(vect_1, vect_2):
    """
    Calculation of Cosine Similarity

    Parameters:
        vect_1: document x
        vect_2: document y

    Return:
        Float
    """
    return dot(vect_1, vect_2) / (norm(vect_1) * norm(vect_2))

def cosine_distance(vect_1, vect_2):
    """
    Calculation of Cosine Distance

    Parameters:
        vect_1: document x
        vect_2: document y

    Return:
        Float
    """
    return 1 - cosine_similarity(vect_1, vect_2)

def wordnet_test():
    #el método synsets nos permite encontrar los sninónimos de alguna palabra
    #print(wn.synsets("dog"))
    #podemos especificar el POS al buscar los sinónimos
    # valores posibles VERB, NOUN, ADJ, ADV
    #print(wn.synsets("dog",pos=wn.VERB))
    #print(wn.synset('dog.n.01').definition())

    word="jumping"
    print(word," ===> ",porter.stem(word))

    word="history"
    print(word," ===> ",porter.stem(word))

    words = ["program", "programming", "programmer", "programs","programmed"]

    example_sentence = "Python programmers often tend like programming in python because it's like english. We call people who program in python pythonistas."

    other_words = nltk.word_tokenize(example_sentence)

    print("Porter Stemmer -------------------------------")

    print("{0:20}{1:20}".format("Word","PorterStemmer"))
    for word in other_words:
        print("{0:20}{1:20}".format(word, porter.stem(word)))

    print("Lancaster Stemmer -------------------------------")
    print("{0:20}{1:20}".format("Word","Lancaster Stemmer"))
    for word in other_words:
        print("{0:20}{1:20}".format(word,lancaster.stem(word)))

    print("Snowball Stemmer -------------------------------")
    print("{0:20}{1:20}".format("Word","Snowball Stemmer"))
    for word in other_words:
        print("{0:20}{1:20}".format(word,snowball.stem(word)))


    words = ['bunnies','organization','polarize','jaguar','stabilize','destabilize','kingdoms','dramatic','favorable']
    print("{0:20}{1:20}{2:20}{3:20}".format("Word", "Porter Stem", "Lancaster Stem", "Snowball Stem"))

    for word in words:
        print("{0:20}{1:20}{2:20}{3:20}".format(word, porter.stem(word),lancaster.stem(word),snowball.stem(word)))


def Corpus_DataAugmentation(article_path, file_name):

    nouns_list = []
    path = os.path.join(article_path, file_name)

    with open(path, "r", encoding="UTF-8") as f:
        article_text = f.read()
        tokens = word_tokenize(article_text)
        pos_tags = pos_tag(tokens)

        for tags in pos_tags:
            current_word = tags[0]
            word_tag = tags[1]

            if(("NN" in word_tag) and (len(word_tag) == 2) and (len(current_word) > 1)):
                nouns_list.append(current_word)
        
        new_noun = ""
        i = 0
        for token in tokens:
            for noun in nouns_list:
                
                if((noun in token) and (len(noun) == len(token))):
                    new_lemmas = []
                    synsets = wn.synsets(noun, pos=wn.NOUN)
                    
                    if(synsets):
                        first_synset = synsets[0]

                        for lemma in first_synset.lemmas():
                            new_lemmas.append(lemma.name())

                        for word in new_lemmas:
                            if(word not in noun):
                                new_noun = word
                            else:
                                new_noun = noun
            
                    if(new_noun != token):
                        print("replacing %s -> %s" % (token, new_noun))
                        tokens[i] = new_noun
            i = i + 1

    new_file = os.path.join(article_path, "augmented_{}.txt".format(file_name))

    with open(new_file, "w", encoding = "UTF-8") as f2:
        for token in tokens:
            f2.write(token)
            f2.write(" ")
        
art_path = r"C:\Users\ie707560\Documents\git\CustomCorpus\temp\guardian\texts\artanddesign"
file_name = "article69.txt"
file_name_augmented = file_name.replace(".txt", "_augmented.txt")

Corpus_DataAugmentation(art_path, "article69.txt")

f1 = open(os.path.join(art_path, file_name) , "r", encoding="UTF-8").read()
f2 = open(os.path.join(art_path, file_name_augmented) , "r", encoding="UTF-8").read()

print(cosine_distance(f1, f2))