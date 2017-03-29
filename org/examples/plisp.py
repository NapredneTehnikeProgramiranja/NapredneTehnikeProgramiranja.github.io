from textx.metamodel import metamodel_from_file

mm = metamodel_from_file("plisp.tx")
m = mm.model_from_file("example.plisp")
