from textx.metamodel import metamodel_from_file
from collections import Iterable
from functools import reduce

mm = metamodel_from_file("plisp.tx")
m = mm.model_from_file("example.plisp")

def gn_Program(e): return e.expressions
def gn_Basic_Expression(e): return None
def gn_S_Expression(e): return e.exp
def gn_BindForm(e): return e.exp

gn_options = {'Basic_Expression': gn_Basic_Expression,
              'S_Expression':     gn_S_Expression}

def gn_LetExpression(e):
    bfs = [gn_BindForm(bf) for bf in e.bind_form]
    exs = [gn_options[ex.__class__.__name__](ex) for ex in e.exp]
    return bfs + exs

def gn_PrintExpression(e): return e.to_print
def gn_DefExpression(e): return e.body
def gn_ApplyExp(e): return e.f_params
def gn_Sum(e): return e.exp
def gn_Product(e): return e.exp

gn_options.update({'Program':          gn_Program,
                   'LetExpression':    gn_LetExpression,
                   'BindForm':         gn_BindForm,
                   'PrintExpression':  gn_PrintExpression,
                   'DefExpression':    gn_DefExpression,
                   'ApplyExp':         gn_ApplyExp,
                   'Sum':              gn_Sum,
                   'Product':          gn_Product})

def get_next_exps(e):
    """Return all successor expressions of a given expression."""
    return gn_options[e.__class__.__name__](e)

def is_let(exp):
    return exp.__class__.__name__ == 'LetExpression'

def get_all_let_bindings(l):
    """Extract all bindings from let."""
    return [b.name for b in l.bind_form]

def spot_lets_single_exp(e, lets=[]):

    if not e: return lets

    if is_let(e):
        pos =  mm.parser.pos_to_linecol(e._tx_position)
        return spot_lets(get_next_exps(e), \
                         lets + [(get_all_let_bindings(e), pos)])
    else:
        return spot_lets(get_next_exps(e), lets)

def spot_lets(e, lets=[]):
    """Spot all the let expressions in the program. Return list of tuples
       ([bind_variable+], position_of_let_expression). """

    def reducer(ls, ex):
        return ls + (spot_lets_single_exp(ex) or [])

    if isinstance(e, Iterable):
        return reduce(reducer, e, lets)
    else:
        return spot_lets_single_exp(e, lets)
