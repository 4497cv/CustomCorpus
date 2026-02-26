# Importamos librerías
import json
import requests
import os
from os import makedirs
from os.path import join, exists
from datetime import date, timedelta
import ast
import workspace
import sys
from guardian import Guardian
import pandas as pd
import re
from numpy import dot
from numpy.linalg import norm
import numpy as np
import math

def euclidean_distance(vect_1, vect_2):
    """
    Calculation of Euclidean Distance

    Parameters:
        vect_1: document x
        vect_2: document y

    Return:
        Float
    """
    diff = np.array(vect_1) - np.array(vect_2)
    return np.sqrt(np.sum(diff**2))

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

def process_euclidean_distance_matrix(bow_df) -> None:
    """
    Generation of the Euclidean Distance Matrix

    Parameters:
        bow_df: Pandas DataFrame

    Return:
        None
    """
    # number of documents
    N = bow_df.shape[0]
    # initialize matrix with zeros
    eucl_matrix = np.zeros((N, N))
    # retrive vectorsvector values
    vectors = bow_df.values

    for i in range(N):
        for j in range(N):
            eucl_matrix[i, j] = euclidean_distance(vectors[i], vectors[j])

    documents_list = bow_df.index.tolist()
    eucl_df = pd.DataFrame(eucl_matrix, index=documents_list, columns=documents_list)

    output_path = os.path.join(workspace.get_workspace_path(), "output")
    os.makedirs(output_path, exist_ok=True)
    eucl_df.to_csv(os.path.join(workspace.get_workspace_path(), "output", "euclidean_dist_matrix.csv"), encoding="utf-8")

def process_cosine_distance_matrix(bow_df) -> None:
    """
    Generation of the Cosine Distance Matrix

    Parameters:
        bow_df: Pandas DataFrame

    Return:
        None
    """
    # number of documents
    N = bow_df.shape[0]
    # initialize matrix with zeros
    cos_mat = np.zeros((N, N))
    # retrive vector values
    vectors = bow_df.values

    for i in range(N):
        for j in range(N):
            cos_mat[i, j] = cosine_distance(vectors[i], vectors[j])

    documents_list = bow_df.index.tolist()
    eucl_df = pd.DataFrame(cos_mat, index=documents_list, columns=documents_list)

    output_path = os.path.join(workspace.get_workspace_path(), "output")
    os.makedirs(output_path, exist_ok=True)
    eucl_df.to_csv(os.path.join(workspace.get_workspace_path(), "output", "cosine_dist_matrix.csv"), encoding="utf-8")

def pre_process_word(word:str) -> str:
    """
    Preprocessing of the word before adding it to the vocabulary

    Parameters:
        word: str
    
    Return:
        new_word: str
    """
    word = word.replace(",", "")
    word = word.replace(".", "")
    word = word.replace(")", "")
    word = word.replace("(", "")
    word = word.replace(";", "")
    word = word.replace(":", "")
    word = word.replace("?", "")
    word = word.replace("\"", "")
    word = word.replace("<", "")
    word = word.replace(">", "")
    word = word.replace("“", "")
    word = word.replace("”", "")
    word = word.replace("’", "")
    word = word.replace("[", "")
    word = word.replace("]", "")
    # regex to remove characters with accents
    word = re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ]', '', word)
    # set word to lower case
    new_word = word.lower()

    return new_word

def process_vocabulary(vocab_lim = 500) -> set:
    """
    Function that obtains all the vocabulary from the stored articles from The Guardian. 

    Parameters:
        vocab_lim: maximum amount of words that are allowed in the vocabulary
    
    Return:
        Vocabulary: set
    """
    vocabulary = set()
    texts_path = workspace.get_texts_path()

    for folder in os.listdir(texts_path):
        tmp_path = os.path.join(texts_path,folder)

        # ignore path if it is not a folder
        if not os.path.isdir(tmp_path):
            continue

        if(os.path.exists(tmp_path)):
            for file in os.listdir(tmp_path):
                if file.endswith(".txt"):
                    file_path = os.path.join(tmp_path, file)
                    curr_art = open(file_path, "r",  encoding="utf-8")

                    for line in curr_art.readlines():
                        words = line.strip().split()
                        for word in words:
                            if(len(word) > 1):
                                word = pre_process_word(word)

                                if(len(vocabulary) >= vocab_lim):
                                    return vocabulary
                                else:
                                    if(word.isalpha() and (len(word) > 1)):
                                        vocabulary.add(word)
                    curr_art.close()

    return vocabulary

def process_bag_of_words(vocabulary: set, type="binary") -> None:
    """
    Function to generate a bag of words from all the articles retreived from the Guardian, and 
    stores it in a CSV file.

    Parameters:
        vocabulary: it is a set containing all the words from all the articles.
        type: it is the kind of bow that will be processed ("binary" or "count").
    
    Return:
        None
    """
    texts_path = workspace.get_texts_path()
    vocab_list = sorted(list(vocabulary))
    bow_matrix = []
    doc_names = []

    for folder in os.listdir(texts_path):
        tmp_path = os.path.join(texts_path,folder)

        # ignore path if it is not a folder
        if not os.path.isdir(tmp_path):
            continue

        if(os.path.exists(tmp_path)):
            for file in os.listdir(tmp_path):
                if((True == file.endswith(".txt"))):
                    print("processing %s" % file)
                    file_path = os.path.join(tmp_path, file)
                    bow = {word: 0 for word in vocabulary}

                    curr_art = open(file_path, "r",  encoding="utf-8")

                    for line in curr_art.readlines():
                        words = line.strip().split()
                        for word in words:
                            if(len(word) > 1):
                                word = pre_process_word(word)
                                if word in bow:
                                    if("binary" == type):
                                        bow[word] = 1
                                    elif("count" == type):
                                        bow[word] += 1
                                    else:
                                        # set binary as default
                                        bow[word] = 1

                    curr_art.close()
                    bow_matrix.append([bow[w] for w in vocabulary])
                    doc_names.append(file)

    bag_of_words_df = pd.DataFrame(bow_matrix, columns=vocab_list, index=doc_names)
    output_path = os.path.join(workspace.get_workspace_path(), "output")
    os.makedirs(output_path, exist_ok=True)
    bag_of_words_df.to_csv(os.path.join(workspace.get_workspace_path(), "output", "bow_matrix_"+ type + ".csv"), encoding="utf-8")

def process_tf_idf(bow_df):
    """
    Function to generates the TF IDF matrix.
    It takes the bag of words data frame, calculates the TF IDF matrix and stores it in a CSV file.

    Parameters:
        bow_df: pandas data frame
    
    Return:
        None
    """
    # inverse document frequency dict
    idf = {}
    # matrix to store TF IDF Matrix
    tfidf_matrix = []
    # number of documents in corpus
    N = bow_df.shape[0]
    # document frequency
    df = (bow_df > 0).sum(axis=0)
    # IDF calculation
    for word in bow_df.columns:
        idf[word] = math.log(N / (1 + df[word]))

    for _, row in bow_df.iterrows():
        tfidf_row = []
        # calculate the total words used
        total_words = row.sum()
        
        for word in bow_df.columns:
            if(total_words > 0):
                # calculate term frequency in document
                tf = row[word] / total_words
            else:
                # word is not used
                tf = 0

            # calculate tfidf
            tfidf_row.append(tf * idf[word])
        
        # save resulting calculation for the current document
        tfidf_matrix.append(tfidf_row)

    bag_of_words_df = pd.DataFrame(tfidf_matrix, index=bow_df.index, columns=bow_df.columns)
    output_path = os.path.join(workspace.get_workspace_path(), "output")
    os.makedirs(output_path, exist_ok=True)
    bag_of_words_df.to_csv(os.path.join(workspace.get_workspace_path(), "output", "tf_idf_matrix.csv"), encoding="utf-8")

def __main__():
    os.chdir("..")
    # retrieve the workspace path
    workspace.set_workspace_path(os.getcwd())

    #start_date = date(2026,1,1)
    #end_date = date(2026,1,1)
    # create object for the Guardian API
    #g = Guardian(start_date, end_date)
    # retrieve articles from the start date to the end date
    #g.fetch_articles()

    # obtain vocabulary from the Guardian articles
    vocabulary = process_vocabulary(vocab_lim=100000)

    # Binary Bag of Words
    process_bag_of_words(vocabulary, "binary")
    bow_b_df = pd.read_csv(os.path.join(workspace.get_workspace_path(), "output", "bow_matrix_binary.csv"), index_col=0)

    # Bag of Words
    process_bag_of_words(vocabulary, "count")
    bow_c_df = pd.read_csv(os.path.join(workspace.get_workspace_path(), "output", "bow_matrix_count.csv"), index_col=0)

    # Generate the TF IDF Matrix
    process_tf_idf(bow_c_df)

    # Generate Cosine Distance Matrix for all the Articles
    process_cosine_distance_matrix(bow_b_df)

    # Generate Euclidean Distance Matrix for all the Articles
    process_euclidean_distance_matrix(bow_b_df)
    
__main__()