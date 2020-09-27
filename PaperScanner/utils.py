import PyPDF4

# makes all words lowercase and removes any punctuation next to words
def clean_text(text):
    text = [word.lower() for word in text]
    text = [word.replace('.', '') for word in text]
    text = [word.replace(',', '') for word in text]
    text = [word.replace('\'', '') for word in text]
    text = [word.replace('\"', '') for word in text]

    return text

# returns a pdf file as one long string, all lowercase
def pdf_to_txt(pdf_file):
    text = ''
    pdf = PyPDF4.PdfFileReader(open(pdf_file, "rb"))
    for page in pdf.pages:
        text += page.extractText()
    return text

# get the position of each word
def get_indices(contents, keywords):
    indices = {}
    for words in contents:
        position = 0
        if words in keywords:
            i = contents.index(words)
            indices[i] =  words
            contents.remove(words)
    return indices

# get the frequency for each word
def get_frequencies(contents, keywords):
    freq = {}
    for word in contents:
        if word in keywords:
            frequencies = contents.count(word)
            freq[word] = frequencies
    return freq

# get the distances between each pair of keywords
def get_distances(indices):
    distances = {}
    for index , word in indices.items():
        pair = indices.items()
        for i, w in pair:
            if w == word and (i - index) > 0:
                distances[i - index] = w
                break
    return distances

# get the average of the distances for each word
def get_averages(distances):
    averages = {}
    for distance , word in distances.items():
        total = 0
        n = 0
        pairs = distances.items()
        for d, w in pairs:
            if w == word:
                n+=1
                total+=d
        average = total/n
        averages[word] = average
    return averages

# tabulate results
def get_report(frequencies, averages, keywords, total_freq):
    result_str = ''
    result_str += "FREQUENCIES: \n"
    for word, freq in frequencies.items():
        result_str += "WORD: {:15}  COUNT: {:5}\n".format(word, freq)
    result_str += "\nAVERAGE SPREAD (between mentions): \n"

    for word, avg in averages.items():
        result_str += "WORD: {:15}  AVG:     {:4.0f} words\n".format(word, avg)
    result_str += "\nRELATIVE RELEVANCE:\n"

    for word in frequencies.keys():
        if frequencies[word] > 1:
           result_str += "WORD: {:15}  REL:      {:5.2f}\n".format(word, 
                        (frequencies[word]/averages[word])/total_freq*100)
    result_str += "\nNOT FOUND: \n"
    n = 0 # to keep track of how many were not found
    for word in keywords:
        if word not in frequencies.keys():
            result_str += word + '\n'
            n+=1
    if n == 0:
        result_str += "(all words were found)\n"
    return result_str