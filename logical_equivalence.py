""" The goal of this project is to create a file that can solve logical equivalences. Showing the possible routes
    from one logical statement to another"""

from typing import Callable


class StatementVariable():
    """ A statement variable, like p or q, can either be True or False"""

    def __init__(self, symbol: str, value: bool = None):
        self.symbol = symbol
        self.truth_value: bool = value


class Expression():
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
        else:
            # for all other connectives, two variables are passed into the evaluation function
            if variable_1 and variable_2:
                self.truth_value = evaluation_function(variable_1, variable_2)



class LogicalConnective(Expression):
    def __init__(self, symbol: str, evaluation_function: Callable, variable_1, variable_2=None):
        super().__init__(symbol, evaluation_function, variable_1, variable_2)


class Negation(Expression):
    def __init__(self, variable_1):
        eval_function = negate
        self.symbol = '~' + variable_1
        super().__init__(self., eval_function, variable_1)


# LOGICAL CONNECTIVE FUNCTIONS
def negation(statement_variable: StatementVariable) -> bool:
    return not statement_variable.truth_value


negate: Callable = negation
