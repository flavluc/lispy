import mock
import pytest

import lispy

@pytest.fixture
def atom():
    return lambda s: lispy.atom(lispy.tokenize(s)[0])

@pytest.fixture
def eval():
    return lambda p, e=lispy.standard_env(): lispy.eval(lispy.parse(p), e)


def test_tokenize():
    assert lispy.tokenize("(+ 1 2)") == ["(", "+", "1", "2", ")"]

def test_atoms(atom):
    assert atom("0") == 0
    assert atom("+") == lispy.Symbol("+")
    assert atom("true") == lispy.Symbol("true")

def test_parse():
    assert lispy.parse("(+ 0 1)") == lispy.List([lispy.Symbol("+"), 0, 1])

def test_eval_lit(eval):
    assert eval("0") == 0

def test_eval_expr(eval):
    assert eval("(< 0 1)") == True
    assert eval("(if (> 0 1) 1 2)") == 2
    assert eval("((lambda (a) (+ 1 a)) 2)") == 3

def test_standard_env(eval):
    assert eval("(length (list 1 2 3))") == 3

def test_updated_env(eval):
    env = lispy.standard_env()
    env.update({'foo': 'bar'})
    assert eval("foo", env) == lispy.Symbol('bar')

def test_lispstr(eval):
    exp = '(< 0 1)'
    list_exp = '(list 1 2 3 4)'

    assert 'True' == lispy.lispstr(eval(exp))
    assert '(1 2 3 4)' == lispy.lispstr(eval(list_exp))

@mock.patch('builtins.input')
@mock.patch('builtins.print')
def test_expr_repl(mock_print, mock_input):
    mock_input.side_effect = ['(< 0 1)', 'exit']
    lispy.repl()
    mock_print.assert_called_with('True')

@mock.patch('builtins.input')
@mock.patch('builtins.print')
def test_env_repl(mock_print, mock_input):
    mock_input.side_effect = ['(define fact (lambda (n) (if (<= n 1) 1 (* n (fact (- n 1))))))', '(fact 10)', 'exit']
    lispy.repl()
    mock_print.assert_called_with('3628800')
