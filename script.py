from kontroll.resources import AvvikResource

avvik_resource = AvvikResource()
dataset = avvik_resource.export()
dataset.csv
