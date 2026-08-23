from project import Match, Analyzer
import pytest

def test_my_color():
    m1 = Match("fabri", "1-0", "fabri", "belen", "B01", "Scotch game")
    assert m1.my_color() == "white"
    m2 = Match("fabri", "1-0", "pirulo", "fabri", "B01", "Caro-Kann")
    assert m2.my_color() == "black"

def test_my_color_invalid_user():
    m = Match("wabeke", "1-0", "fabri", "ian", "B01", "Scandinavian Defense")
    with pytest.raises(ValueError):
        m.my_color()

def test_result_match():
    m1 = Match("fabri", "1-0", "fabri", "belen", "B01", "Italian game")
    assert m1.result_match() == "win"
    m2 = Match("fabri", "0-1", "fabri", "pirulo", "B01", "Pirc Defense")
    assert m2.result_match() == "lose"
    m3 = Match("fabri", "1/2-1/2", "fabri", "pachi", "B01", "Sicilian Defense")
    assert m3.result_match() == "draw"
    m4 = Match("fabri", "0-1", "wabeke", "fabri", "B01", "Philidor Defense")
    assert m4.result_match() == "win"
    m5 = Match("fabri", "1-0", "maxi", "fabri", "B01", "French Defense")
    assert m5.result_match() == "lose"
    m6 = Match("fabri", "1/2-1/2", "josema", "fabri", "B01", "Four Knights Game")
    assert m6.result_match() == "draw"

def test_result_match_invalid():
    m = Match("fabri", "2-0", "fabri", "mateo", "B01", "King's Pawn Opening")
    with pytest.raises(ValueError):
        m.result_match()

def test_calculate_rates():
    a = Analyzer("fabri")
    results1 = {"win": 5, "lose": 3, "draw": 2}
    assert a.calculate_rates(results1) == {
        "winrate": 50.0,
        "loserate": 30.0,
        "drawrate": 20.0
    }
    results2 = {"win": 0, "lose": 0, "draw": 0}
    assert a.calculate_rates(results2) == {
        "winrate": 0,
        "loserate": 0,
        "drawrate": 0
    }