
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import collections
import re
from nltk.corpus import stopwords
import sys
import time

## this function will return the unique sentences in the review file for a given restaurant
#######################################################################################
def UniqueReviews(filepath):
        
#read the input 
    try:
        f=open(filepath)
    except IOError:
        print ("Could not read file:", filename)
        sys.exit()
    text=f.read().strip()
    f.close()
    
    #split sentences
    sentences=sent_tokenize(text)
    adj_sentence = set()
    
    #check for unique  sentences in the reviews 
    counter = 0
    for sentence in sentences:
        counter += 1
        adj_sentence.add(sentence)
        
    #    print(counter)
    adj_sentence=list(adj_sentence)     
    #    print(len(adj_sentence))  
    print("The following tips are generated from {} unique sentences".format(len(adj_sentence)))              
    return(adj_sentence)

#######################################################################################
def tokenize(string):
    filtered_words = [word for word in re.findall(r'\w+', string.lower()) if word not in stopwords.words('english')]
    return filtered_words

#######################################################################################

def count_ngrams(lines, min_length=2, max_length=4):
  
    lengths = range(min_length, max_length + 1)
    ngrams = {length: collections.Counter() for length in lengths}
    queue   = collections.deque(maxlen=max_length)

    # Helper function to add n-grams at start of current queue to dict
    def add_queue():
        current = tuple(queue)
        for length in lengths:
            if len(current) >= length:
                ngrams[length][current[:length]] += 1

    # Loop through all lines and words and add n-grams to dict
    for line in lines:
        for word in tokenize(line):
            queue.append(word)
            if len(queue) >= max_length:
                add_queue()

    # Make sure we get the n-grams at the tail end of the queue
    while len(queue) > min_length:
        queue.popleft()
        add_queue()

    return (ngrams)

#######################################################################################    
def loadwords(fname):
    newLex=set()
    try:
        lex_conn=open(fname)
    except IOError:
        print ("Could not read file:", filename)
        sys.exit()
    for line in lex_conn:
        line = line.lower()
        newLex.add(line.strip())
    lex_conn.close()

    return newLex 

#######################################################################################  
def list_of_ngrams(ngrams, num=20):
    """Print num most common n-grams of each length in n-grams dict."""
    list_of_ngrams = set()
    for n in sorted(ngrams):
        for gram, count in ngrams[n].most_common(num):
            list_of_ngrams.add(' '.join(gram))
    return list(list_of_ngrams)
#######################################################################################  
def print_most_frequent(ngrams, num=20):
    """Print num most common n-grams of each length in n-grams dict."""
    print("\nLogic behind our tips prediction:-")
    for n in sorted(ngrams):
        print('----- {} most common {}-grams -----'.format(num, n))
        for gram, count in ngrams[n].most_common(num):
            print('{0}: {1}'.format(' '.join(gram), count))
        print('')  
        
####################################################################################### 
def run(path,filename):
    dishes = loadwords('/Users/utkarsh/Desktop/BIA_project/dishes.txt') 
    recommender_list = loadwords('/Users/utkarsh/Desktop/BIA_project/List.txt') 
    unique_sentences = UniqueReviews(path)
    time.sleep(1)
    print('\nExtracted from the restaurant: {}'.format(filename)) 
    ngrams = count_ngrams(unique_sentences)
    print_most_frequent(ngrams)
    time.sleep(4)
    ngrams_list=list_of_ngrams(ngrams)
    ngrams_sent = dict()
    
   
    for grams in ngrams_list:
        for sentence in unique_sentences:
            if grams in sentence:
                ngrams_sent.setdefault(grams,[]).append(str(sentence))
                
             
    for grams,sentences in ngrams_sent.items():
        if grams in dishes:
            print("\nYou can try dish: {}".format(grams))
            print("------------------------------------------------")
            max_sentence = len(max(sentences))
            count = 0
            for sentence in sentences:
                count += 1
                words = sent_tokenize(sentence)
                for word in words:
                    if (len(sentence)== max_sentence or word in recommender_list):
                        sentence= sentence.replace(grams,'**'+str(grams)+'**')
                        print("Sample review  : {}".format(sentence))
            print("Also the tip appears in another {} reviews.".format(count))
                
         

dirpath = '/Users/utkarsh/Desktop/BIA_project/Restaurants/'
filename = '2.TheMasalaWala.txt'
path = dirpath+filename      
run(path,filename)


            
            
    
        
        
