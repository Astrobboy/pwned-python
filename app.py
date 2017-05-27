#!flask/bin/python
import sys
import logging
import os
import base64
import uuid
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def root_path():
  response = {
    "status": "ok",
    "info": "root_path"
  }
  return jsonify(response)

@app.route('/healthz', methods=['GET'])
def healthz():
  response = {
    "status": "ok",
    "hostname": "ignored me"#os.environ["HOSTNAME"]
  }

  return jsonify(response)

@app.route('/question', methods=['POST'])
def question():
  """equest.get_json()
  Recibe una pregunta
  crea un nuevo elemento en el API firebase
  utiliza el resultado anterior y envia al API language
  """
  response = {}
  question_payload = {}
  try:
      json_data = request.get_json()
      question_payload['path'] = '/question'
      question_payload['method'] = 'push'
      question_payload['data'] = jsonify(json_data)
      firebase_url = "%s/publish" % os.environ['FIREBASE']
      post_question_request = requests.post(firebase_url, data = jsonify(question_payload))
      if post_question_request.status_code == '201':
        post_request_payload = post_question_request.json()
        language_question_url = "%s/question" % os.environ['LANGUAGE']
        post_language_request = requests.post(language_question_url, data = jsonify(post_request_payload))
        response = post_language_request
        
  except Exception as e:
      print('Error: {}'.format(e))

  return jsonify(response)

@app.route('/upload', methods=['POST'])
def upload():
  """json_datae del archivo anterior para subir al firebase
  utiliza el resultado anterio y lo envia al API vision
  debe retornar un json con el contenido del firebase
  """
  response = {}
  try:
      json_data = request.get_json()
      filename = '{}.jpg'.format(str(uuid.uuid4()))
      image = base64.b64decode(json_data['file'])
      with open(os.path.join(os.environ['DOWNLOADS_LOCATION'], filename), 'wb') as f:
         f.write(image)
      response['status'] = 'succesful'
      response['message'] = 'The file is writed to filesystem'
  except Exception as e:
      response['status'] = 'failed'
      response['message'] = e

  return jsonify(response)

@app.route('/message', methods=['POST'])
def message():
  """
  Recibe un message
  crea un nuevo elemento en el API firebase
  utiliza el resultado anterior y envia al API language
  """
  response = {}
  message_payload = {}
  try:
      json_data = request.get_json()
      message_payload['path'] = '/message'
      message_payload['method'] = 'push'
      message_payload['data'] = jsonify(json_data)
      firebase_url = "%s/publish" % os.environ['FIREBASE']
      post_message_request = requests.post(firebase_url,, data = jsonify(message_payload))
      if post_message_request.status_code == '201':
          post_request_payload = post_message_request.json()
          language_message_url = "%s/message" % os.environ['LANGUAGE']
          post_language_request = requests.post(os.path.join(language_message_url, 'message'), data = jsonify(post_request_payload))
          response = post_language_request

  except Exception as e:
      print('Error: {}'.format(e))

  return jsonify(response)


if __name__ == "__main__":
  app.run(host="0.0.0.0", port="8080")
