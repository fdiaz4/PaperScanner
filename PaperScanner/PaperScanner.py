import json
from utils import *

def get_keywords(text, keywords):

    file_contents = text
    file_contents = file_contents.split()

    #converts everything to lowercase, and cleans up punctuation around words.
    file_contents = clean_text(file_contents)

    frequencies = get_frequencies(file_contents, keywords)
    indices = get_indices(file_contents, keywords)

    uninteresting_keys = [] # to hold keys we don't care about
    for key in frequencies.keys():
        if key not in keywords:
            uninteresting_keys.append(key)
    
    # delete all uninteresting results
    for key in uninteresting_keys:
        del frequencies[key]
    
    
    distances = get_distances(indices)
    
    averages = get_averages(distances)

    total = 0
    for word in frequencies.keys():
        if frequencies[word] > 1:
            total += frequencies[word]/averages[word]
    
    

    return get_report(frequencies, averages, keywords, total)


if (__name__ == '__main__'):
    filename = input("> Enter the PDF's path or filename: ")
    keywords = input("> Enter the keywords (space separated): ").split()

    for i in range(0, len(keywords)):
        keywords[i] = keywords[i].replace('~', ' ')

    txt = pdf_to_txt(filename)

    results = get_keywords(txt, keywords)

    print(results)

