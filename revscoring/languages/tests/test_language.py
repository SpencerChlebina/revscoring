import pickle

from nose.tools import assert_not_equal, eq_, raises

from ...dependent import DependencyError, solve
from ..language import Language, LanguageUtility, is_badword, is_stopword


def process_is_badword():
    def is_badword(word):
        return word == "badword"
    return is_badword

my_is_badword = LanguageUtility("is_badword", process_is_badword)

def test_language_utility():
    eq_(is_badword == is_badword, True)
    eq_(is_badword != is_badword, False)


def test_language():

    l = Language('revscoring.languages.test', [my_is_badword])

    assert is_badword in l.context()
    eq_(l.context()[is_badword]()("badword"), True)

    recovered_l = pickle.loads(pickle.dumps(l))
    eq_(recovered_l, l)
    eq_(l == 5678, False)
    eq_(l != 5678, True)
    recovered_context = recovered_l.context()

    assert is_badword in recovered_context
    eq_(recovered_context[is_badword]()("badword"), True)

@raises(DependencyError)
def test_not_implemented():

    l = Language('revscoring.languages.test', [])
    solve(is_stopword, context=l.context())
