from app import app
from flask import Flask, request, jsonify, render_template, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user, login_required
import base64
from urllib.parse import unquote_plus
import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
import io
import os
import binascii
from PIL import Image

UPLOAD_DIRECTORY = os.getcwd()+'/app/static'

@app.route('/')
@app.route('/index')
def index():
    upload_avros = [x for x in os.listdir(UPLOAD_DIRECTORY) if '.avro' in x]
    return render_template('index.html', uploads=upload_avros)

@app.route('/upload')
def target():

    args = request.args
    avrofile = args.get('file')

    targets = DataFileReader(open(UPLOAD_DIRECTORY+'/'+avrofile, "rb"), DatumReader())
    
    tts = [{
        'ObjectID':x['ObjectID'],
        'RA': x['RA'],
        'DEC': x['DEC'],
        'RAPM': x['RAPM'],
        'DECPM': x['DECPM'],
        'MAG': x['MAG'],
        'EQUINOX': x['EQUINOX'],
        'FinderFile': str(x['FinderFile'])
    } for x in targets]

    return render_template('upload.html', targets=tts)
    

@app.route('/target_upload', methods=['POST'])
def target_upload():

    json_args = request.get_json()

    avro_file = base64.b64decode(str.encode(unquote_plus(json_args['file'])))
    of = io.BytesIO(avro_file) 

    targets = DataFileReader(of, DatumReader())
    
    schema = avro.schema.parse(open('mmt_target.avsc', 'rb').read())
    writer = DataFileWriter(open(UPLOAD_DIRECTORY+'/test_avro.avro', 'wb'), DatumWriter(), schema)
    for t in targets:
        writer.append(t)
    writer.close()

    tts = DataFileReader(open(UPLOAD_DIRECTORY+'/test_avro.avro', 'rb'), DatumReader())
    for t in tts:
        print(t)

    finder_bytes = base64.b64decode(str.encode(unquote_plus(json_args['finder'])))
    stream = io.BytesIO(finder_bytes)
    img = Image.open(stream)
    img.save(UPLOAD_DIRECTORY+"/"+json_args['finder_filename'])

    return(jsonify('success'))

@app.route('/targets', methods=['GET'])
def targets():
    pass
