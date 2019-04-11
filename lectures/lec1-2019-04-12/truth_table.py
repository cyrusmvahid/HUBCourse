# code copied from: https://codereview.stackexchange.com/questions/145465/creating-truth-table-from-a-logical-statement
import itertools
import re
from tabulate import tabulate
from collections import OrderedDict

symbols = {'∧', '∨', '→', '↔'} # Symbols for easy copying into logical statement

statement = '~(A ∧ B) ↔ (~A ∨ ~B)'


def parenthetic_contents(string):
    """
    From http://stackoverflow.com/questions/4284991/parsing-nested-parentheses-in-python-grab-content-by-level

    Generates parenthesized contents in string as pairs (level, contents).

    >>> list(parenthetic_contents('~(p ∨ q) ↔ (~p ∧ ~q)')
    [(0, 'p ∨ q'), (0, '~p ∧ ~q')]
    """
    stack = []
    for i, char in enumerate(string):
        if char == '(':
            stack.append(i)
        elif char == ')' and stack:
            start = stack.pop()
            yield (len(stack), string[start + 1: i])


def conditional(p, q):
    """Evaluates truth of conditional for boolean variables p and q."""
    return False if p and not q else True


def biconditional(p, q):
    """ Evaluates truth of biconditional for boolean variables p and q."""
    return (True if p and q
        else True if not p and not q 
        else False)


def and_func(p, q):
    """ Evaluates truth of AND operator for boolean variables p and q."""
    return p and q


def or_func(p, q):
    """ Evaluates truth of OR operator for boolean variables p and q."""
    return p or q

def negate(p):
    """ Evaluates truth of NOT operator for boolean variables p and q."""
    return not p

def apply_negations(string):
    """ 
    Applies the '~' operator when it appears directly before a binary number.

    >>> apply_negations('~1 ∧ 0')
    '0 ∧ 0'
    """
    new_string = string[:]
    for i, char in enumerate(string):
        if char == '~':
            try:
                next_char = string[i+1] # Character proceeding '~'
                num = int(next_char)
                negated = str(int(negate(num)))
                new_string = new_string.replace('~'+string[i+1], negated)
            except:
                # Character proceeding '~' is not a number
                pass
    return new_string


def eval_logic(string):
    """
    Returns the value of a simple logical statement with binary numbers.

    >>> eval_logic('1 ∧ 0')
    0
    """

    string = string.replace(' ', '') # Remove spaces
    string = apply_negations(string) # Switch ~0 to 1, ~1 to 0
    new_string = string[:]
    operators = {
        '∧': and_func,
        '∨': or_func,
        '→': conditional,
        '↔': biconditional,
        }
    for i, char in enumerate(string):
        if char in operators:
            logical_expression = string[i-1 : i+2]
            truth_value_1, truth_value_2 = int(string[i-1]), int(string[i+1])
            boolean = operators[char](truth_value_1, truth_value_2)
    try:
        return int(boolean) # Return boolean as 0 or 1
    except:
        # None of the logical operators were found in the string
        return int(string) # Return the value of the string itself


def get_variables(statement):
    """
    Finds all alphabetic characters in a logical statement string.
    Returns characters in a list.

    statement : str
        Statement containing variables and logical operators

    >>> get_variables('~(p ∨ q) ↔ (~p ∧ ~q)')
    ['p', 'q']
    """
    variables = {char for char in statement if char.isalpha()} # Identify variables
    variables = list(variables)
    variables.sort()
    return variables


def truth_combos(statement):
    """
    Returns a list of dictionaries, containing all possible values of the variables in a logical statement string.

    statement : str
        Statement containing variables and logical operators

    >>> truth_combos('(~(p ∨ q) ↔ (~p ∧ ~q))')
    [{'q': 1, 'p': 1}, {'q': 0, 'p': 1}, {'q': 1, 'p': 0}, {'q': 0, 'p': 0}]
    """
    variables = get_variables(statement)
    combo_list = []
    for booleans in itertools.product([True, False], repeat = len(variables)):
        int_bool = [int(x) for x in booleans] # Replace True with 1, False with 0
        combo_list.append(dict(zip(variables, int_bool)))
    return combo_list


def replace_variables(string, truth_values):
    """
    Replaces logical variables with truth values in a string.

    string : str
        Logical expression

    truth_values : dict
        Dictionary mapping variable letters to their current truth values (0/1)

    >>> replace_variables('Q ∨ R', {'Q': 1, 'R': 1, 'P': 1})
    '1 ∨ 1'
    """
    for variable in truth_values:
        bool_string = str(truth_values[variable])
        string = string.replace(variable, bool_string)
    return string


def simplify(valued_statement):
    """
    Simplifies a logical statement by evaluating the statements contained in the innermost parentheses.

    valued_statement : str
        Statement containing binary numbers and logical operators

    >>> simplify('(~(0 ∧ 0) ↔ (~0 ∨ ~0))')
    '(~0 ↔ 1)'
    """
    brackets_list = list(parenthetic_contents(valued_statement))
    if not brackets_list:
        # There are no brackets in the statement
        return str(eval_logic(valued_statement))
    deepest_level = max([i for (i,j) in brackets_list]) # Deepest level of nested brackets
    for level, string in brackets_list:
        if level == deepest_level:
            bool_string = str(eval_logic(string))
            valued_statement = valued_statement.replace('('+string+')', bool_string)
    return valued_statement


def solve(valued_statement):
    """ 
    Fully solves a logical statement. Returns answer as binary integer.

    valued_statement : str
        Statement containing binary numbers and logical operators

    >>> solve('(~(0 ∧ 0) ↔ (~0 ∨ ~0))')
    1
    """
    while len(valued_statement) > 1:
        valued_statement = simplify(valued_statement)
    return int(valued_statement)


def get_truth_table(statement):
    """ 

    Returns a truth table in the form of nested list.
    Also returns a boolean 'tautology' which is True if the logical statement is always true.

    statement : str
        Statement containing variables and logical operators

    >>> get_truth_table('~(A ∧ B) ↔ (~A ∨ ~B)')
    ([[1, 1, 1], [1, 0, 1], [0, 1, 1], [0, 0, 1]], True)
    """
    if statement[0] != '(':
        statement = '('+statement+')' # Add brackets to ends
    variables = get_variables(statement)
    combo_list = truth_combos(statement)
    truth_table_values = []
    tautology = True
    for truth_values in combo_list:
        valued_statement = replace_variables(statement, truth_values)
        ordered_truth_values = OrderedDict(sorted(truth_values.items()))
        answer = solve(valued_statement)
        truth_table_values.append(list(ordered_truth_values.values()) + [answer])
        if answer != 1:
            tautology = False
    return truth_table_values, tautology

def print_statement(statement):
    variables = get_variables(statement)
    truth_table_values, tautology = get_truth_table(statement)


    print(
    """ 
    Logical statement: 

    {}

    Truth Table: 

    {}

    Statement {} a tautology
    """.format(
        statement,
        tabulate(truth_table_values, headers=variables + ['Answer']),
        'is' if tautology else 'is not'
    ))  