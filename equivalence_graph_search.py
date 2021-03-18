from logical_statements import Create
import logical_equivalence as log_eq
import pygraphviz as pgv

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
    def equivalent_statements_and_laws_used(self):
        if not self._equivalent_statements_and_laws_used:
            statement_law_pairs = log_eq.all_one_step_equivalents_of(self.statement)
            self._equivalent_statements_and_laws_used = statement_law_pairs
        return self._equivalent_statements_and_laws_used

    @property
    def adjacent_nodes(self):
        if not self._adjacent_nodes:
            adjacent_nodes = [Node(stmt) for stmt, law in self.equivalent_statements_and_laws_used]
            self._adjacent_nodes = adjacent_nodes
        return self._adjacent_nodes

    @property
    def get_edges(self):
        if not self._edges:
            self._edges = [Edge(self, Node(adj_stmt), law_used) for adj_stmt, law_used in
                           self.equivalent_statements_and_laws_used]
        return self._edges

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


class EquivalenceGraphSearch:
    def __init__(self, source_statement, search_limit=20):
        self.source_statement = source_statement
        self.search_limit = search_limit

        self._nodes = None
        self._edges = None

        self._pgz_G = None


    @property
    def nodes(self):
        if not self._nodes:
            self._nodes = explore_and_find_all_nodes_from(self.source_statement, self.search_limit)
        return self._nodes

    @property
    def edges(self):
        if not self._edges:
            edges = []
            for node in self.nodes:
                edges.extend(node.get_edges)
            self._edges = edges
        return self._edges


    @property
    def pgz_G(self):
        if not self._pgz_G:
            self._pgz_G = self.to_pgz_G()
        return self._pgz_G

    def to_svg(self, filename):
        self.pgz_G.layout(prog='dot')
        self.pgz_G.draw(filename, format='svg')

    def to_pgz_G(self):
        G = pgv.AGraph()
        for edge in self.edges:
            G.add_node(edge.n1.name, statement=edge.n1.statement)
            G.add_node(edge.n2.name, statement=edge.n2.statement)
            G.add_edge(edge.n1.name, edge.n2.name, law=edge.law, law_name=edge.law.short_name)
        G.layout(prog='dot')
        return G

def explore_and_find_all_nodes_from(source_statement, searches: int = 20):
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

test_statement = Create.conjunction(p, not_of_p_or_q)
n = explore_and_find_all_nodes_from(test_statement)

G = EquivalenceGraphSearch(test_statement)