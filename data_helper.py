import time
import sys
import re
import logging
import numpy as np
import pandas as pd
from collections import Counter
from collections import defaultdict

from stop_words import get_stop_words

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.snowball import FrenchStemmer

from nltk.corpus import wordnet as wn
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import FrenchStemmer


tag_map = defaultdict(lambda : wn.NOUN)
tag_map['J'] = wn.ADJ
tag_map['V'] = wn.VERB
tag_map['R'] = wn.ADV

stop_words = get_stop_words('french')
ps = FrenchStemmer()

chk_count = {
	"i" : 0,
	"n" : 835
}

#data_pre_process_param = {
#	"modele" : "stemm"
#	"choices" : ["stemm", "lemm"]
#}


def update_progress(progress):
    barLength = 40 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()


def clean_str_EN(s):
	"""Clean sentence"""
	s = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", s)
	s = re.sub(r"\'s", " \'s", s)
	s = re.sub(r"\'ve", " \'ve", s)
	s = re.sub(r"n\'t", " n\'t", s)
	s = re.sub(r"\'re", " \'re", s)
	s = re.sub(r"\'d", " \'d", s)
	s = re.sub(r"\'ll", " \'ll", s)
	s = re.sub(r",", " , ", s)
	s = re.sub(r"!", " ! ", s)
	s = re.sub(r"\(", " \( ", s)
	s = re.sub(r"\)", " \) ", s)
	s = re.sub(r"\?", " \? ", s)
	s = re.sub(r"\s{2,}", " ", s)
	s = re.sub(r'\S*(x{2,}|X{2,})\S*',"xxx", s)
	s = re.sub(r'[^\x00-\x7F]+', "", s)
	return s.strip().lower()



def progress_X() :
	update_progress(chk_count['i'] / chk_count['n'])
	chk_count['i']=chk_count['i']+1
	return

def stematize_texte(texte):
	""" returns the text from any file """
	texte = texte.lower();
	# remove punctuation
	texte = re.sub(r'[^\w\s]',' ',texte)
	example_words = word_tokenize(texte)
	output_texte = ""
	progress_X()
	for word in example_words:
		if word not in stop_words and word.isalpha():
			#print("-> "+word+" NOT in stop_words")
			if output_texte != "" :
				output_texte += " "
			output_texte += ps.stem(word)
	return output_texte


# stopwords.words('french')
def lemmatisation_texte(texte) :
	words = texte.lower();
	output_texte = ""
	word_Lemmatized = WordNetLemmatizer()
	Final_words = []
	for entry in word_tokenize(words):
		for word, tag in pos_tag([entry]):
			if word not in stop_words and word.isalpha():
				word_Final = word_Lemmatized.lemmatize(word,tag_map[tag[0]])
				Final_words.append(word_Final)
	output_texte = ' '.join(Final_words)
	progress_X()
	return output_texte




def clean_str(s):
	"""Clean sentence"""

	# supprime ponctuaation
	s = re.sub(r'\\n','',s)
	s = re.sub(r'[^\w\s]',' ',s)
	s = re.sub(' +', ' ', s)

	if data_pre_process_param["modele"] == "lemm":
		s = lemmatisation_texte(s)
	else :
		s = stematize_texte(s)

    #example_words = word_tokenize(s)
	return s.strip().lower()

ATTRIBUTE_TO_PREDICT = 'CL31_0'

def load_data_and_labels(filename):
	"""Load sentences and labels"""
	df = pd.read_csv(filename, compression='zip', dtype={'faits': object}, encoding = 'utf8')
	selected = [ATTRIBUTE_TO_PREDICT, 'faits']
	non_selected = list(set(df.columns) - set(selected))

	df = df.drop(non_selected, axis=1) # Drop non selected columns
	df = df.dropna(axis=0, how='any', subset=selected) # Drop null rows
	df = df.reindex(np.random.permutation(df.index)) # Shuffle the dataframe

	# Map the actual labels to one hot labels
	labels = sorted(list(set(df[selected[0]].tolist())))

	one_hot = np.zeros((len(labels), len(labels)), int)
	np.fill_diagonal(one_hot, 1)
	label_dict = dict(zip(labels, one_hot))

	chk_count['n'] = len(df[selected[1]])

	x_raw = df[selected[1]].apply(lambda x: clean_str(x)).tolist()
	y_raw = df[selected[0]].apply(lambda y: label_dict[y]).tolist()
	return x_raw, y_raw, df, labels

def batch_iter(data, batch_size, num_epochs, shuffle=True):
	"""Iterate the data batch by batch"""
	data = np.array(data)
	data_size = len(data)
	num_batches_per_epoch = int(data_size / batch_size) + 1

	for epoch in range(num_epochs):
		if shuffle:
			shuffle_indices = np.random.permutation(np.arange(data_size))
			shuffled_data = data[shuffle_indices]
		else:
			shuffled_data = data

		for batch_num in range(num_batches_per_epoch):
			start_index = batch_num * batch_size
			end_index = min((batch_num + 1) * batch_size, data_size)
			yield shuffled_data[start_index:end_index]

if __name__ == '__main__':
	input_file = './data/consumer_complaints.csv.zip'
	x, y, df, labels= load_data_and_labels(input_file)
	print(labels)
	print(x[0])
	print(y[0])
