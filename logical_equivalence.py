""" The goal of this project is to create a file that can solve logical equivalences. Showing the possible routes
    from one logical statement to another"""
import itertools
from typing import Callable, Type, Union

AND_SYMBOL = '∧'
NEGATION_SYMBOL = '~'
OR_SYMBOL = '∨'

negate: Callable[[bool], bool] = lambda statement_variable: not statement_variable.truth_value
conjoin: Callable[[bool], bool] = lambda statement_1, statement_2: statement_1.truth_value and statement_2.truth_value
inclusive_disjoin: Callable[[bool], bool] = lambda statement_1, statement_2: statement_1.truth_value \
                                                                             or statement_2.truth_value


# STATEMENT VARIABLE

class Atom():
    """ A statement variable, like p, ~p, q, p ∧ q, can either be True or False"""

    def __init__(self, symbol: str, value: bool = None):
        self.symbol = symbol
        self.truth_value: bool = value

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return '<StatementVariable: %s = %s>' % (self.symbol, self.truth_value)


# GENERAL LOGICAL EXPRESSION

class Expression:
    """ The parent class of all logical connectives. It holds one or more Statement Variables (class), and the child
            class is the logical connective component
    Any logical expression of one or more StatementVariable AND a logical connective.
            """

    def __init__(self, symbol, evaluation_function, variable_1, variable_2=None):
        """

        :param symbol: the symbolic representation of this expression
        :param evaluation_function: the function that is used to evalute the truth value of this expression
        :param variable_1: the first StatementVariable in this expression
        :param variable_2: the second StatementVariable in this expression. None in the case of the connective being
                            Negation
        """
        self.evaluate: Callable = evaluation_function
        self.variable_1 = variable_1
        self.variable_2 = variable_2



        # calculate the truth value of this expression iff all needed variables have a truth value
        if evaluation_function == negate:
            # negate is a special case where only one variable is passed into the evaluation function
            if variable_1:
                self.truth_value = evaluation_function(variable_1)
                print(self.truth_value)
        else:
            # for all other connectives, two variables are passed into the evaluation function
            if variable_1 and variable_2:
                self.truth_value = evaluation_function(variable_1, variable_2)

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return '<StatementVariable: %s = %s>' % (self.symbol, self.truth_value)

    @property
    def variables(self):
        return [self.variable_1, self.variable_2]

    def unique_atoms(self, statements=None):
        all_unique_atoms = set()
        to_search = self.variables if statements is None else statements
        for statement in to_search:
            if is_atomic(statement):
                all_unique_atoms.add(statement)
            else:
                all_unique_atoms.add(self.unique_atoms(statement))

        return all_unique_atoms


def flatten(object):
    gather = []
    for item in object:
        if isinstance(item, (list, tuple, set)):
            gather.extend(flatten(item))
        else:
            gather.append(item)
    return gather


def nested_atoms_in(expression):
    if is_atomic(expression):
        return [expression]
    else:
        return [nested_atoms_in(expression.variable_1)] + [nested_atoms_in(expression.variable_2)]


def unique_atoms_in(expression):
    nested_list_of_atoms = nested_atoms_in(expression)
    return set(flatten(nested_list_of_atoms))




def bool_to_int(boolean):
    return int(boolean is True)


def is_atomic(statement):
    return True if type(statement) == Atom else False


# Truth Tables
class TruthTable:
    def __init__(self, expression: Expression):
        self.expression = expression
        self.unique_atoms = unique_atoms_in(self.expression)
        self.atom_count = len(self.unique_atoms)
        self.permutations = self.truth_value_permutations(self.unique_atoms)
        self.truth_values = self.calculate_truth_values_for_all_permutations(self.permutations)

        self.rows = 2 ** self.atom_count





def truth_value_permutations(unique_atoms):
    atom_count = len(unique_atoms)
    rows = 2 ** atom_count

    columns = []
    row_number_divisor = 0.5
    atom_index = 0
    while atom_index <  atom_count - 1:
        row_values = [True] * int(rows * row_number_divisor) + [False] * int(rows * row_number_divisor)
        columns.append(row_values)
        row_number_divisor *= row_number_divisor
        atom_index += 1

    singleton_row = [True, False] * int(rows / 2)
    columns.append(singleton_row)
    return columns

def permutations_of_atom_values(atoms):
    """Given a set of atoms, returns a list with all possible combinations of their True/False values"""
    atom_count = len(atoms)

    unique_true_false_combinations = [[True]*i + [False]*(atom_count-i) for i in range(0,atom_count+1)]
    all_permutations = []
    for combination in unique_true_false_combinations:
        permutations = set(itertools.permutations(combination))
        all_permutations.extend(permutations)

    return all_permutations



class LogicalConnective(Expression):
    def __init__(self, symbol: str, evaluation_function: Callable, variable_1, variable_2=None):
        super().__init__(symbol, evaluation_function, variable_1, variable_2)



# LOGICAL CONNECTIVES

class Negation(Expression):
    def __init__(self, variable_1: Atom):
        eval_function = negate
        self.symbol = NEGATION_SYMBOL + variable_1.__str__()
        super().__init__(self.symbol, eval_function, variable_1)


class Disjunction(Expression):
    def __init__(self, variable_1: Atom, variable_2: Atom):
        eval_function = inclusive_disjoin
        self.symbol = f'({variable_1.__str__()} {OR_SYMBOL} {variable_2.__str__()})'
        super().__init__(self.symbol, eval_function, variable_1, variable_2)


class Conjunction(Expression):
    def __init__(self, variable_1: Atom, variable_2: Atom):
        eval_function = conjoin
        self.symbol = f'({variable_1.__str__()} {AND_SYMBOL} {variable_2.__str__()})'

        super().__init__(self.symbol, eval_function, variable_1, variable_2)


class LawOfLogicalEquivalence:
    def __init__(self, input_expresion: Expression):
        pass


class Commutative(LawOfLogicalEquivalence):
    def __init__(self, input_expression: Union[Type[Conjunction], Type[Disjunction]]):
        if type(input_expression) not in [Disjunction, Conjunction]:
            raise Exception('A Commutative equivalence of something not a disjunction or conjunction was attempted')


def commutation_equivalent(expression: Union[Type[Conjunction], Type[Disjunction]]):
    if type(expression) not in [Disjunction, Conjunction]:
        raise Exception('A Commutative equivalence of something not a disjunction or conjunction was attempted')

    return expression.__class__(expression.variable_2, expression.variable_1)

# LAWS OF LOGICAL EQUIVALENCE

# LAWS OF LOGICAL EQUIVALENCE
def junction_opposite(junction: Union[Conjunction, Disjunction]):
    if junction == Conjunction:
        return Disjunction
    elif junction == Disjunction:
        return Conjunction
    else:
        raise ValueError('junction_opposite() must be passed either a conjunction or disjunction')


def association_equivalent(expression):
    """ Returns p AND (q AND r) given (p AND q) AND r"""

    expression_class = expression.__class__

    assert expression_class == expression.variable_1.__class__

    #                                       p                                           q                       AND    r
    return expression_class(expression.variable_1.variable_1,
                            expression_class(expression.variable_1.variable_2, expression.variable_2))


def distributive_equivalent(expression):
    assert type(expression.variable_1) == Atom

    expression_type = type(expression)
    variable_2_type = type(expression.variable_2)

    left_side = expression_type(expression.variable_1, expression.variable_2.variable_1)
    right_side = expression_type(expression.variable_1, expression.variable_2.variable_2)

    distributed_expression = variable_2_type(left_side, right_side)
    return distributed_expression


def reverse_distributive_equivalent(expression):
    left_side = expression.variable_1
    right_side = expression.variable_2

    left_side_type = type(left_side)
    right_side_type = type(right_side)
    assert left_side_type == right_side_type

    common_atom = left_side.variable_1

    reverse_distributed_expression = left_side_type(common_atom,
                                                    type(expression)(left_side.variable_2, right_side.variable_2))
    return reverse_distributed_expression


def convert_to_tautology(expression):
    pass


def convert_to_contradiciton(expression):
    pass


def identity_equivalent(expression):
    pass


def negation_law_equivalent(expression):
    pass


def double_negative_law_equivalent(expression):
    pass


def idempotent_equivalent(expression):
    pass


def universal_bound_law_equivalent(expression):
    pass


def de_morgan_equivalent(expression):
    pass


def absorption(expression):
    pass


def negation_of_tautology(expression):
    pass


def negation_of_contradiction(expression):
    pass


def eligibility(expression):
    eligible_laws = []

    expression_type = type(expression)
    variable_1_type = type(expression.variable_1)
    variable_2_type = type(expression.variable_2)
    # Laws involving Disjunction and Conjunction
    if expression_type in [Disjunction, Conjunction]:
        # commutative laws
        eligible_laws.append(commutation_equivalent)

        # associative laws: first statement variable is itself the same as the parent statemeny type (OR, AND)

        if variable_1_type == expression_type:
            eligible_laws.append(association_equivalent)

    return eligible_laws


TRUE_STATEMENT_p = Atom('p', True)
FALSE_STATEMENT_q = Atom('q', False)
TRUE_r = Atom('r', True)
conjunction_TF = Conjunction(TRUE_STATEMENT_p, FALSE_STATEMENT_q)
conjunction_FF = Conjunction(FALSE_STATEMENT_q, FALSE_STATEMENT_q)

to_distribute = Disjunction(TRUE_r, conjunction_TF)
distributed = distributive_equivalent(to_distribute)
reverse_distributive_equivalent(distributed)

p_and_q = unique_atoms_in(conjunction_TF)

TT_of_pq = truth_value_permutations(p_and_q)


def walk_down_expression_evaluation(expression):
    unique_atoms = unique_atoms_in(expression)

    all_permutations_of_truth_values = permutations_of_atom_values(unique_atoms)

    all_permutations_of_atom_values = []
    for truth_value_permutation in all_permutations_of_truth_values:
        atom_values = {}
        for i, atom in enumerate(unique_atoms):
            atom_values[atom] = truth_value_permutation[i]
        all_permutations_of_atom_values.append(atom_values) # ok

    #for atom_value_permutations
        # evalue the expression but set each atom value to the matching bool in the diction
        # this seems fucking clunky. Maybe I build up a function as the expression is created that can take params
        # for each unique atom. That seems like a better way. So expression.evaluation is a nested function type deal.
walk_down_expression_evaluation(to_distribute)