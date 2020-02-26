import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter


def main():
	schema = avro.schema.parse(open("mmt_avro2.avsc", "rb").read())
	writer = DataFileWriter(open("targets.avro", "wb"), DatumWriter(), schema)
	writer.append(
		{
			"ObjectID": "m31", 
		})
	writer.close()

	targets = DataFileReader(open("targets.avro", "rb"), DatumReader())
	for t in targets:
		print(t)

main()
