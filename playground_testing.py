#%%

import logic_test_bed
from logical_equivalence import *
from logical_statements import *
import networkx as nx

#%%



#%%

p = Create.atom(symbol='p')
q = Create.atom(symbol='q')
r = Create.atom(symbol='r')

# general use negations
not_p = Create.negation(p)
not_q = Create.negation(q)
not_r = Create.negation(r)

# general use conjunctions
p_and_q = Create.conjunction(p, q)
q_and_p = Create.conjunction(q, p)
q_and_r = Create.conjunction(q, r)

# general use disjunctions
p_or_q = Create.disjunction(p, q)
q_or_p = Create.disjunction(q, p)
q_or_r = Create.disjunction(q, r)

# for de morgans tests
not_of_p_and_q = Create.negation(p_and_q)
not_p_or_not_q = Create.disjunction(not_p, not_q)

not_of_p_or_q = Create.negation(p_or_q)
not_p_and_not_q = Create.conjunction(not_p, not_q)

# for associative law

#%%

p_or_q_equivs = all_one_step_equivalents_of(p_or_q)
p_and_p_or_q = Create.conjunction(p, p_or_q)
p_and_p_or_q_equivs = all_one_step_equivalents_of(p_and_p_or_q)

#%%

print(4)
#%%

print(f'Original: {p_or_q.symbol}\n\n')

print('Equivalents found:')
for stmt, law in p_or_q_equivs:
    print(f'{stmt.symbol}    <--- {str(law)}')

#%%

print(f'Original: {p_and_p_or_q.symbol}\n\n')

print('Equivalents found:')
for stmt, law in p_and_p_or_q_equivs:
    print(f'{stmt.symbol}{" "* (20-len(stmt.symbol))}<--- {law}')

#%%

""" It appears to be working! I can get all the one step equivalents of the above 2 statements."""


#%%

# GRAPHING
# Nodes will be graph symbols. Statement object will be stored in node.
# Edges will be law names

def add_new_nodes_from(statement: Statement, G: nx.Graph):
    new_one_step_equivalents = all_one_step_equivalents_of(statement)

    for new_statement, law_used in new_one_step_equivalents:
        print(law_used.short_name)
        G.add_node(new_statement.symbol, object=new_statement)
        G.add_edge(statement.symbol, new_statement.symbol, law_object=law_used, law_name=law_used.short_name)

#%%

G = nx.Graph()
G.add_node(p_or_q.symbol, object=p_or_q)
add_new_nodes_from(p_or_q, G)

#%%

nx.draw(G)

#%%

nx.draw(G, with_labels=True)
pos= nx.spring_layout(G)
labels = nx.get_edge_attributes(G,'law_name')
print('s')
x = nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, label_pos=0.5, font_size=8)

#%%
""" I can get a one step graph and print it with node and edge labels being the statement symbol and
law used respectively"""


#%%
def add_statement_to(G: nx.Graph, statement: Statement):
    G.add_node(statement.symbol, object=statement)

def add_equivalent_statement_to(G: nx.Graph,
                                first: Statement, second: Statement,
                                law_used: LawOfEquivalence):
    G.add_edge(first.symbol, second.symbol, law_object=law_used, law_name=law_used.short_name)

#%%
def lazy_statement_equivalence_search(first: Statement, target: Statement):
    G = nx.Graph()
    add_statement_to(G, first)

    statements_to_search = [first]
    target_found = False

    while statements_to_search and not target_found:
        for search_statement in statements_to_search:
            print(search_statement)
            if not search_statement or search_statement.symbol in G:
                statements_to_search.remove(search_statement)
                continue
            equivalent_statements = all_one_step_equivalents_of(search_statement)
            for equivalent_statement, law_used in equivalent_statements:
                if equivalent_statement.symbol not in G:
                    statements_to_search.append(equivalent_statement)
                add_equivalent_statement_to(G, search_statement, equivalent_statement, law_used)

            if target.symbol in equivalent_statements:
                target_found = True

            statements_to_search.remove(search_statement)

    return G

#%%
#### TESTING LAZY EQUIVALENCE SEARCH

search_graph = lazy_statement_equivalence_search(p_or_q, p_or_q_equivs[2][0])


#%%
p_or_q_equivs

#%%


