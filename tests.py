import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

"""10 novos testes"""
def test_question_points_out_of_range():
    with pytest.raises(Exception, match="Points must be between 1 and 100"):
        Question(title='q1', points=0)
    with pytest.raises(Exception, match="Points must be between 1 and 100"):
        Question(title='q1', points=101)

def test_choice_id_generation_is_incremental():
    question = Question(title='q1')
    c1 = question.add_choice('A')
    c2 = question.add_choice('B')
    assert c1.id == 1
    assert c2.id == 2

def test_remove_choice_by_id():
    question = Question(title='q1')
    choice = question.add_choice('To be removed')
    question.remove_choice_by_id(choice.id)
    assert len(question.choices) == 0

def test_remove_choice_with_invalid_id():
    question = Question(title='q1')
    with pytest.raises(Exception, match="Invalid choice id 99"):
        question.remove_choice_by_id(99)

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('A')
    question.add_choice('B')
    question.remove_all_choices()
    assert len(question.choices) == 0

def test_set_correct_choices_updates_status():
    question = Question(title='q1')
    c1 = question.add_choice('A', is_correct=False)
    question.set_correct_choices([c1.id])
    assert c1.is_correct is True

def test_correct_selected_choices_returns_matches():
    question = Question(title='q1', max_selections=2)
    c1 = question.add_choice('Correct', is_correct=True)
    c2 = question.add_choice('Incorrect', is_correct=False)
    
    result = question.correct_selected_choices([c1.id, c2.id])
    assert result == [c1.id]

def test_correct_selected_choices_exceeds_max_selections():
    question = Question(title='q1', max_selections=1)
    c1 = question.add_choice('A')
    c2 = question.add_choice('B')
    with pytest.raises(Exception, match="Cannot select more than 1 choices"):
        question.correct_selected_choices([c1.id, c2.id])

def test_choice_text_constraints():
    question = Question(title='q1')
    with pytest.raises(Exception, match="Text cannot be empty"):
        question.add_choice('')
    with pytest.raises(Exception, match="Text cannot be longer than 100 characters"):
        question.add_choice('a' * 101)

def test_find_choice_by_id_internal_logic():
    question = Question(title='q1')
    choice = question.add_choice('Find me')
    question.remove_choice_by_id(choice.id)
    assert choice not in question.choices