import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
import base64
from urllib.parse import quote_plus
import requests
import imageio

def main():

    finder_file = 'm31.jpg'
    target_file = 'm31.avro'
    schema = avro.schema.parse(open("mmt_target.avsc", "rb").read())
    writer = DataFileWriter(open(target_file, "wb"), DatumWriter(), schema)
    writer.append({
        "ObjectID": "m3100",
        "RA":42,
        "DEC":42,
        "RAPM":0.0,
        "DECPM":0.0,
        "MAG":4.3,
        "PA":180.0,
        "EQUINOX":"J2000",
        "FinderFile":finder_file
    })
    writer.close()

    with open(target_file, 'rb') as tf:
        contents = tf.read()

    with open(finder_file, 'rb') as ff:
        finder = ff.read()

    json = {
                "file": quote_plus(base64.b64encode(contents)),
                "finder":quote_plus(base64.b64encode(finder)),
                "fmt":"jpg",
                "finder_filename":finder_file
            }

    r = requests.post('http://127.0.0.1:5000/target_upload', json=json)
    print(r.text)

main()
