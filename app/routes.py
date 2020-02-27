from app import app
from flask import Flask, request, jsonify, render_template, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user, login_required
import base64
from urllib.parse import unquote_plus

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"



@app.route('/target_upload', methods=['POST'])
def target_upload():
	print('test')
	args = request.args
	url_unquote = unquote_plus(args['file'])
	print(url_unquote)
	compress_file = str.encode(url_unquote)
	print(compress_file)
	decompress = base64.b64decode(compress_file)
	return(jsonify(decompress))
	#return(jsonify(args))
