from logical_statements import Create
import logical_equivalence as log_eq

## TEST VARS

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

class Node:
    def __init__(self, statement):
        self.statement = statement
        self.name = statement.symbol

        self._adjacent_nodes = None
        self._edges = None
        self._equivalent_statements_and_laws_used = None

    @property
    def equivalent_statements_and_laws_use(self):
        if not self._equivalent_statements_and_laws_used:
            statement_law_pairs = log_eq.all_one_step_equivalents_of(self.statement)
            self._equivalent_statements_and_laws_used = statement_law_pairs
        return self._equivalent_statements_and_laws_used

    @property
    def adjacent_nodes(self):
        if not self._adjacent_nodes:
            adjacent_nodes = [Node(stmt) for stmt, law in self.equivalent_statements_and_laws_use]
            self._adjacent_nodes = adjacent_nodes
        return self._adjacent_nodes

    @property
    def get_edges(self):
        edges = [Edge(self, Node(adj_stmt), law_used) for adj_stmt, law_used in self.equivalent_statements_and_laws_used]
        return edges

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if self.name == other.name:
            return True
        return False


class Edge:
    def __init__(self, n1, n2, law):
        self.n1 = n1
        self.n2 = n2
        self.law = law


def equivalence_graph_search(source_statement, searches: int = 5):
    source_node = Node(source_statement)
    all_nodes = [source_node]

    unsearched_nodes = [source_node]
    searches_remaining = searches
    while unsearched_nodes and searches_remaining > 0:
        print('####')
        print(f'{searches_remaining = }')
        print(f'{len(unsearched_nodes) = }')
        print(f'{len(all_nodes) = }')

        new_nodes_found_in_this_loop = []
        for node_to_search in unsearched_nodes:
            adjacent_nodes = node_to_search.adjacent_nodes

            new_nodes = [node for node in adjacent_nodes if node not in all_nodes]
            all_nodes.extend(new_nodes)
            new_nodes_found_in_this_loop.extend(new_nodes)

        searches_remaining -= 1
        unsearched_nodes = new_nodes_found_in_this_loop

    return all_nodes

n = equivalence_graph_search(Create.conjunction(p, not_of_p_or_q))
a = 1
