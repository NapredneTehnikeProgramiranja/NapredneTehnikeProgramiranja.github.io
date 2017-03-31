from textx.metamodel import metamodel_from_file

lets = []

mm = metamodel_from_file("plisp.tx")

def let_object_processor(let):
    lets.append(([b.name for b in let.bind_form],
                 mm.parser.pos_to_linecol(let._tx_position)))

mm.register_obj_processors({'LetExpression': let_object_processor})

m = mm.model_from_file("example.plisp")

def spot_lets():
    return lets

print(spot_lets())
# [(['a'], (2, 15)),
#  (['v'], (2, 4)),
#  (['s'], (17, 15)),
#  (['a', 'b'], (15, 9)),
#  (['m', 'n'], (24, 2))]
