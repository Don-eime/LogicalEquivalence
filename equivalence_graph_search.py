from statement_atom_expression import *


p = Atom('p')
q = Atom('q')

not_q = Create.negation(q)
not_q_and_q = Create.conjunction(not_q, q)

to_explore = Create.disjunction(p, not_q_and_q)



