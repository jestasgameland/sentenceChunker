#!C:\Users\Brendon\AppData\Local\Programs\Python\Python39\python.exe

#(The above code is so Apache (XAMPP) knows where Python is to run it)
# This Python Flask app gets a sentence from the HTML form via JS Ajax call
# Then uses NLTK to tokenize and get parts of speech
# Finally, uses render_template to display as HTML 

from flask import Flask, render_template, json, request      #import flask class

app = Flask(__name__)        #make an instance of the class, passing the name as an argument - __name__

import nltk, re, pprint, os

def preprocess(text):
	text = text.replace(",","")
	sentences = nltk.sent_tokenize(text)
	sentences = [nltk.word_tokenize(s) for s in sentences]
	# remove end punctuation:
	for i in range(0, len(sentences)): sentences[i] = sentences[i][0:len(sentences[i])-1]
	sentences = [nltk.pos_tag(s) for s in sentences]
	return sentences
	# a list of lists of tuples

# DEFINE GRAMMARS:
np_grammar = """
	NP: {<DT>?<JJ.?>*(<JJR><IN>)?<VBN>?<VBG>?<CD>?<NN>*}
		{<NNP>*}

"""  
vp_grammar = "VP: {<MD>?<RB>?<MD>?<VB.*>*<RB>?}"
pp_grammar = "PP: {<IN>*<DT>?<NN.?>?}"

np_chunker = nltk.RegexpParser(np_grammar)
vp_chunker = nltk.RegexpParser(vp_grammar)
pp_chunker = nltk.RegexpParser(pp_grammar)


#get the chunked sentence:
def getChunks(sentence):  
	result = vp_chunker.parse(  pp_chunker.parse(  np_chunker.parse(sentence)  ))
	return result

#Get chunks ready for display (take out the 'NP', 'VP', etc)
def cleanChunks(sentence): 
	finalChunks = []

	chunkedSentence = getChunks(sentence)

	for chunk in chunkedSentence:

		cleanChunk = []

		if isinstance(chunk, tuple):  # if it's not an NP, VP, or PP according to my grammars, it will be just a tuple of (word, pos)
			cleanChunk.append(chunk[0])
		else: 
			for word in chunk: # if it's an NP, PP, or VP, it may have multiple words, so we must loop
				cleanChunk.append(word[0])

		cleanChunk = "&nbsp;".join(cleanChunk)
			
		finalChunks.append(cleanChunk)

	return "&nbsp;&nbsp;/&nbsp;&nbsp;".join(finalChunks)

#----------------------------------------------------------------------------------

# App Routes:

@app.route("/")
def index():
	return render_template('index.html')


@app.route('/chunksentences', methods=['POST'])         
def chunkSentences():

	if request.method == 'POST':

		inputText = request.form.get('inputtext')
		sentences = preprocess(inputText)

		#make array of chunked sentences:
		chunkedSentences = [cleanChunks(sen) for sen in sentences]


		html = ""

		for sen in chunkedSentences: html += sen + "<br><br>"

		return html


if __name__ == "__main__":
    app.run()

# To run this, in Terminal, enter:
# set FLASK_ENV=development
# set FLASK_APP=application.py
# flask run