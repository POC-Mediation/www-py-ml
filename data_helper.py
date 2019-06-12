import time
import sys
import re
import logging
import numpy as np
import pandas as pd
#from collections import Counter
#from collections import defaultdict

#from stop_words import get_stop_words

#from nltk.tokenize import sent_tokenize, word_tokenize
#from nltk import pos_tag
#from nltk.corpus import stopwords
#from nltk.corpus import wordnet as wn
#from nltk.stem import WordNetLemmatizer
#from nltk.stem.snowball import FrenchStemmer


if __name__ == '__main__':
	input_file = './data/consumer_complaints.csv.zip'
	x, y, df, labels= load_data_and_labels(input_file)
	print(labels)
	print(x[0])
	print(y[0])
