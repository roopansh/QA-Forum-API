from flask import Flask, jsonify, make_response, request, abort
from random import randint

app = Flask(__name__)

# For storing the Questions

'''
Questions contain the following fields :-
	id
	question
	answers(list)
		likes
		dislikes

	Example template :-
	{	
		'id' 		: question_ID,
		'question' 	: "What do you like?",
		'answers'	: [
						{
							'id'	 : answer_ID,
							'answer' : 'Answer1',
							'like'	 : like,
							'dislike': dislike
						},
						{
							'id'	 : answer_ID,
							'answer' : 'Answer2',
							'like'	 : like,
							'dislike': dislike
						},
					  ]
	}
'''
Questions = [ {	
				'id' 		: "z2VaRBy3",
				'question' 	: "What do you like?",
				'answers'	: [
								{
									'id'	 : 'Amangoes',
									'answer' : 'Mangoes',
									'like'	 : 0,
									'dislike': 1
								},
								{
									'id'	 : 'Aapples',
									'answer' : 'apples',
									'like'	 : 85,
									'dislike': 0
								},
							  ]
	} ]

'''
Polls contain the following fields :-

	TO DO

'''
Polls = []


def randomIDGen():
	'''
	Random ID generator
	'''

	# check if the ID is already present, 
	# to be implemented

	chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
	ID = "".join(random.choice(chars) for _ in range(8))
	return ID;

'''
Error Handling 404 : Resource not found
'''
@app.errorhandler(404)
def notFound(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def badRequest(error):
	return make_response(jsonify({'error': 'Bad request'}), 400)

'''
Check connection to the API
'''
@app.route('/', methods = ['GET'])
def homepage():
	return jsonify({"success": "true"})

'''
Get question and it's answer
INPUT : ID of the question
'''
@app.route('/question/get/<question_ID>', methods = ['GET'])
def getQuestion(question_ID):
	question = []
	question = [q for q in Questions if q['id'] == question_ID]
	if len(question) == 0:
		abort(404) 
	
	return jsonify({ 'result' : question[0]})

'''
Return a random question
'''
@app.route('/question/random/', methods = ['GET'])
def getRandomQuestion():
	if len(Questions) == 0:
		abort(404)
	# elif len(Questions) == 1:
		# return jsonify(Questions[0])
	question = Questions[randint(0,len(Questions)-1)]
	return jsonify(question)

'''
Return the answers to a particular question
INPUT : Question ID
'''
@app.route('/question/getanswer/<question_ID>', methods = ['GET'])
def getAnswersof(question_ID):
	question = [question for question in Questions if question['id'] == question_ID]

	if len(question) == 0:
		abort(404) 
	
	return jsonify(question[0])

'''
Add new question
'''
@app.route('/question/add/', methods = ['POST'])
def addQuestion():
	if not request.json or not 'question' in request.json:
		abort(400)
	ID = randomIDGen()
	question = { 'id' : ID, 
				 'question' : request.json['question'],
				 'answers' : []
			   }
	Questions.append(question)
	return jsonify({'question' : question})

'''
Answer to question
INPUT : Question ID
'''
@app.route('/question/answer/<question_ID>', methods = ['POST'])
def addAnswer(question_ID):
	question = [q for q in Questions if q['id'] == question_ID]
	
	if len(question) == 0:
		abort(404) 
	
	# if not request.json:
	# 	abort(400)

	answer_ID = 'A' + randomIDGen()
	answer = {  'id' : answer_ID,
				'answer' : request.json['answer'],
				'like' : 0,
				'dislike' : 0}
	question[0]['answers'].append(answer)

	return jsonify(question[0])

'''
Like a particular answer to a particular question
INPUT : Question ID, Answer_ID
'''
@app.route('/like/<question_ID>/<answer_ID>', methods = ['POST'])
def likeAnswer(question_ID, answer_ID):
	question = []
	for q in Questions:
		if q['id'] == question_ID:
			question.append(q)
			for answer in q['answers']:
				if answer['id'] == answer_ID:
					answer['like'] = answer['like'] + 1
					return jsonify({'success' : 'true'})
	abort(404)


'''
Dislike a particular answer to a particular question
INPUT : Question ID, Answer_ID
'''
@app.route('/dislike/<question_ID>/<answer_ID>', methods = ['POST'])
def disLikeAnswer(question_ID, answer_ID):
	question = []
	for q in Questions:
		if q['id'] == question_ID:
			question.append(q)
			for answer in q['answers']:
				if answer['id'] == answer_ID:
					answer['dislike'] = answer['dislike'] + 1
					return jsonify({'success' : 'true'})
	abort(404)

@app.route('/question/all')
def completeQuestionList():
	return jsonify({ 'result' : Questions})

if __name__ == '__main__':
	app.run(debug=True, use_reloader=True)