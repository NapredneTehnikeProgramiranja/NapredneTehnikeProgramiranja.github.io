from textx.metamodel import metamodel_from_file

mm = metamodel_from_file("plisp.tx")
m = mm.model_from_file("example.plisp")

def gn_Program(e): return e.expressions
def gn_Basic_Expression(e): return None
def gn_S_Expression(e): return e.exp
def gn_BindForm(e): return e.exp

gn_options = {mm._current_namespace['Basic_Expression']: gn_Basic_Expression,
              mm._current_namespace['S_Expression']: gn_S_Expression}

def gn_LetExpression(e):
    bfs = [gn_BindForm(bf) for bf in e.bind_form]
    exs = [gn_options[type(ex)](ex) for ex in e.exp]
    return bfs + exs

def gn_PrintExpression(e): return e.to_print
def gn_DefExpression(e): return e.body
def gn_ApplyExp(e): return e.f_params
def gn_Sum(e): return e.exp
def gn_Product(e): return e.exp

gn_options.update({mm._current_namespace['Program']:          gn_Program,
                   mm._current_namespace['LetExpression']:    gn_LetExpression,
                   mm._current_namespace['BindForm']:         gn_BindForm,
                   mm._current_namespace['PrintExpression']:  gn_PrintExpression,
                   mm._current_namespace['DefExpression']:    gn_DefExpression,
                   mm._current_namespace['ApplyExp']:         gn_ApplyExp,
                   mm._current_namespace['Sum']:              gn_Sum,
                   mm._current_namespace['Product']:          gn_Product})

def get_next_exprs(e):
    """Return all successor expressions of a given expression."""
    return gn_options[type(e)](e)

def is_let(exp):
    return mm._current_namespace['LetExpression'] == type(exp)

def get_all_let_bindings(l):
    """Extract all bindings from let."""
    return [b.name for b in l.bind_form]

def spot_lets(e, lets=[]):
    """Spot all the let expressions. Returning list of tuple
       (bind_variables, position_of_let_expression)."""

    if not e: return lets

    if is_let(e):
        pos =  mm.parser.pos_to_linecol(e._tx_position)
        spot_lets(get_next_expressions(e), \
                  lets.append((get_all_let_bindings(e), pos)))
    else:
        spot_lets(get_next_expressions(e), lets)

l = m.expressions[4].exp.f_params[0].exp
