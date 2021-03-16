from logical_statements import *


# UTIL
def is_junction(statement):
    if statement.connective is ValueFunctions.conjunction or \
            statement.connective is ValueFunctions.disjunction:
        return True
    else:
        return False


def junction_opposite(statement):
    if statement.connective is ValueFunctions.conjunction:
        return ValueFunctions.disjunction
    elif statement.connective is ValueFunctions.disjunction:
        return ValueFunctions.conjunction
    return None


def is_statement(statement):
    return True if statement.__class__ == Statement else False


def are_opposite_junctions(statement_1, statement_2):
    if not is_junction(statement_1) or not is_junction(statement_2):
        return False

    junction_2s_opposite = junction_opposite(statement_2)
    if statement_1.connective is junction_2s_opposite:
        return True
    return False


def is_tautology_or_contradiction(statement):
    if statement.connective is ValueFunctions.tautology or \
            statement.connective is ValueFunctions.contradiction:
        return True
    return False


def is_negation(statement):
    if statement.connective is ValueFunctions.negation:
        return True
    return False


def is_double_negative(statement):
    if is_negation(statement) and is_negation(statement.left_term):
        return True
    return False


class LawOfEquivalence(ABC):
    short_name: str

    @staticmethod
    @abstractmethod
    def eligible(statement: Statement):
        pass

    @staticmethod
    @abstractmethod
    def apply(statement: Statement):
        pass


class CommutativeLaw(LawOfEquivalence):
    short_name = 'Commut.'

    @staticmethod
    def eligible(statement: Statement):
        if is_junction(statement):
            return True
        return False

    @staticmethod
    def apply(statement: Statement):
        return Statement(statement.connective, statement.right_term, statement.left_term)


class AssociativeLaw(LawOfEquivalence):
    short_name = 'Assoc.'
    @staticmethod
    def eligible(statement: Statement):
        if is_junction(statement):
            if statement.left_term.connective == statement.connective:
                return True
        else:
            return False

    @staticmethod
    def apply(statement: Statement):
        """ Given (p AND q) AND r. Returns Returns p AND (q AND r) """
        new_left = statement.left_term.left_term  # p

        new_right = Statement(statement.connective,
                              statement.left_term.right_term,  # q
                              statement.right_term)  # r

        return Statement(statement.connective, new_left, new_right)


class ReverseAssociativeLaw(LawOfEquivalence):
    short_name = 'Rev. Assoc.'
    @staticmethod
    def eligible(statement: Statement):
        if is_junction(statement):
            if statement.right_term.__class__ == Statement:
                if statement.right_term.connective == statement.connective:
                    return True
        else:
            return False

    @staticmethod
    def apply(statement: Statement):
        """ Given p AND (q AND r). Returns (p AND q) AND r."""
        new_left = Statement(statement.connective,
                             statement.left_term,  # p
                             statement.right_term.left_term)  # q

        new_right = statement.right_term.right_term  # r

        return Statement(statement.connective, new_left, new_right)


class DistributiveLaw(LawOfEquivalence):
    short_name = 'Distr.'
    @staticmethod
    def eligible(statement: Statement):
        """ Returns the eligibility of statement for application of the Distributive Law. p ∧ (q ∨ r) """
        if is_junction(statement):
            # the statement is a junction
            if Util.is_atom(statement.left_term) and statement.right_term.__class__ == Statement:
                # the left statement is an atom and the right statement is another statement
                if statement.right_term.connective == junction_opposite(statement):
                    # the connective of the second statement is the opposite junction of the parameter statement
                    return True
        else:
            return False

    @staticmethod
    def apply(statement: Statement):
        new_left_side = Statement(statement.connective, statement.left_term,
                                  statement.right_term.left_term)
        new_right_side = Statement(statement.connective, statement.left_term,
                                   statement.right_term.right_term)

        return Statement(statement.right_term.connective, new_left_side, new_right_side)


class IdentityLaw(LawOfEquivalence):
    short_name = 'Iden.'

    @staticmethod
    def eligible(statement: Statement):
        if is_junction(statement) and statement.right_term in [TAUTOLOGY, CONTRADICTION]:
            # the statement is a junction and the second statement is either tautology or contradiction
            return True
        else:
            return False

    @staticmethod
    def apply(statement: Statement):
        return statement.left_term


class ReverseDistributiveLaw(LawOfEquivalence):
    short_name = 'Rev. Distr.'
    @staticmethod
    def eligible(statement: Statement):
        """
            Eligible if:
                connective and both statements are junctions AND
                both statement connectives are the opposite junction to the central one
        :param statement:
        :return:
        """
        if is_junction(statement) and is_junction(statement.right_term) and is_junction(statement.left_term):
            if are_opposite_junctions(statement, statement.right_term):
                return True
        return False

    @staticmethod
    def apply(statement: Statement):
        new_left = statement.left_term.left_term
        new_right = Statement(statement.connective, statement.left_term.right_term,
                              statement.right_term.right_term)

        return Statement(statement.left_term.connective, new_left, new_right)


class NegationLaw(LawOfEquivalence):
    short_name = 'Neg.'
    @staticmethod
    def eligible(statement: Statement):
        if is_junction(statement) and statement.left_term == statement.right_term.left_term and\
                is_negation(statement.right_term):
            return True
        return False

    @staticmethod
    def apply(statement: Statement):
        if statement.connective == ValueFunctions.disjunction:
            return TAUTOLOGY
        elif statement.connective == ValueFunctions.conjunction:
            return CONTRADICTION


class DoubleNegativeLaw(LawOfEquivalence):
    short_name = 'Doub. Neg.'
    @staticmethod
    def eligible(statement: Statement):
        if is_negation(statement) and is_negation(statement.left_term):
            return True
        return False

    @staticmethod
    def apply(statement: Statement):
        return statement.left_term.left_term


class ReverseDoubleNegativeLaw(LawOfEquivalence):
    """ Gives ~(~(p)) from p. Likely unneeded."""

    short_name = 'Rev. Doub. Neg.'
    @staticmethod
    def eligible(statement: Statement):
        if not is_negation(statement):
            # everything except negations are eligible
            return True
        return False

    @staticmethod
    def apply(statement: Statement):
        return Statement(ValueFunctions.negation, Statement(ValueFunctions.negation, statement))


class IdempotentLaw(LawOfEquivalence):
    short_name = 'Idem.'
    @staticmethod
    def eligible(statement: Statement):
        if is_junction(statement) and statement.left_term == statement.right_term:
            return True
        return False

    @staticmethod
    def apply(statement: Statement):
        return statement.left_term


class UniversalBoundLaw(LawOfEquivalence):
    short_name = 'Uni. Boun.'
    @staticmethod
    def eligible(statement: Statement):
        if is_junction(statement) and is_tautology_or_contradiction(statement.right_term):
            return True
        return False

    @staticmethod
    def apply(statement: Statement):
        if statement.connective == ValueFunctions.disjunction:
            return TAUTOLOGY
        elif statement.connective == ValueFunctions.conjunction:
            return CONTRADICTION


class DeMorgansLaw(LawOfEquivalence):
    short_name = 'De Morg.'
    @staticmethod
    def eligible(statement: Statement):
        if is_negation(statement) and is_junction(statement.left_term):
            return True
        return False

    @staticmethod
    def apply(statement: Statement):
        negated_statement = statement.left_term
        new_left_side = Create.negation(negated_statement.left_term)
        new_right_side = Create.negation(negated_statement.right_term)

        new_connective = junction_opposite(negated_statement)

        de_morgans_product = Statement(new_connective, new_left_side, new_right_side)
        return de_morgans_product


class ReverseDeMorgansLaw(LawOfEquivalence):
    short_name = 'Rev. De Morg.'

    @staticmethod
    def eligible(statement: Statement):
        if is_junction(statement) and is_negation(statement.left_term) and is_negation(statement.right_term):
            return True

        return False

    @staticmethod
    def apply(statement: Statement):
        new_connective = junction_opposite(statement)

        new_junction = Statement(new_connective, statement.left_term.left_term,
                                 statement.right_term.left_term)

        return Create.negation(new_junction)


class AbsorptionLaw(LawOfEquivalence):
    short_name = 'Abs'
    @staticmethod
    def eligible(statement: Statement):
        if is_junction(statement):
            # must be junction
            if are_opposite_junctions(statement, statement.right_term):
                # right statement must also be a junction, and junction opposite to statement
                if statement.right_term.left_term != statement.right_term.right_term:
                    # the right junction cannot be between the same to Atoms (so that this law doesn't apply 2 laws)
                    if statement.right_term.left_term == statement.left_term:
                        # the left statement of right statement must be the same as
                        # the left statement of parent statement
                        return True
        return False

    @staticmethod
    def apply(statement: Statement):
        return statement.left_term


class ContradictionNegationLaw(LawOfEquivalence):
    short_name = 'Contr. Neg.'
    @staticmethod
    def eligible(statement: Statement):
        if is_negation(statement) and statement.left_term == CONTRADICTION:
            return True
        return False

    @staticmethod
    def apply(statement: Statement):
        return TAUTOLOGY


class TautologyNegationLaw(LawOfEquivalence):
    short_name = 'Taut. Neg.'
    @staticmethod
    def eligible(statement: Statement):
        if is_negation(statement) and statement.left_term == TAUTOLOGY:
            return True
        return False

    @staticmethod
    def apply(statement: Statement):
        return CONTRADICTION


def all_simple_equivalents(statement: Statement):
    if not statement:
        return []
    eligible_laws = [law for law in ALL_EQUIVALENCE_LAWS if law.eligible(statement)]

    return [(law.apply(statement), law) for law in eligible_laws]


def equivalents_in_which_left_statement_changes(statement: Statement):
    if not statement:
        return []

    left_statement = statement.left_term

    left_equivalents = all_simple_equivalents(left_statement)

    equivalent_statements = [
        (statement.copy(new_left_term=left_equivalent, law_used_in_creation=law_used_in_creation), law_used_in_creation)
        for left_equivalent, law_used_in_creation in left_equivalents]

    return equivalent_statements


def equivalents_in_which_right_statement_changes(statement: Statement):
    if not statement:
        return []
    right_statement = statement.right_term

    right_equivalents = all_simple_equivalents(right_statement)

    equivalent_statements = [(
                             statement.copy(new_right_term=right_equivalent, law_used_in_creation=law_used_in_creation),
                             law_used_in_creation)
                             for right_equivalent, law_used_in_creation in right_equivalents]
    return equivalent_statements


def all_one_step_equivalents_of(statement: Statement):
    if statement is None:
        return []
    # get the simple equivalents
    simple_equivalents = all_simple_equivalents(statement)

    # base case is where statement is an atom, tautology or contradiction
    # return just the simple equivalents
    if Util.is_atom(statement) or Util.is_general_tautology(statement) or Util.is_general_contradiction(statement):
        return simple_equivalents

    # otherwise it is a more complex statement that cone have complex equivalents as well as simple equivalents
    # complex equivalents are where everything is the same except

    equivs_in_which_left_term_changes = equivalents_in_which_left_statement_changes(statement)
    equivs_in_which_right_term_changes = equivalents_in_which_right_statement_changes(statement)

    return simple_equivalents + equivs_in_which_left_term_changes + equivs_in_which_right_term_changes


ALL_EQUIVALENCE_LAWS = LawOfEquivalence.__subclasses__()

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

p_or_q_equivs = all_one_step_equivalents_of(p_or_q)
p_and_p_or_q = Create.conjunction(p, p_or_q)
p_and_p_or_q_equivs = all_one_step_equivalents_of(p_and_p_or_q)
