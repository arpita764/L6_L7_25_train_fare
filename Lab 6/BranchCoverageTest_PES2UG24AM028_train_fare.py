import pytest
from train_fare import base_fare, concession, tatkal_charge

# base_fare
def test_sleeper_fare():
    assert base_fare("SL", 500) == 500

def test_unknown_class():
    with pytest.raises(ValueError):
        base_fare("XX", 100)

def test_invalid_distance_zero():
    with pytest.raises(ValueError):
        base_fare("SL", 0)

def test_invalid_distance_negative():
    with pytest.raises(ValueError):
        base_fare("3A", -10)

def test_minimum_fare():
    assert base_fare("SL", 10) == 50

def test_fare_exactly_50():
    assert base_fare("SL", 50) == 50

def test_other_classes():
    assert base_fare("3A", 100) == 200
    assert base_fare("2A", 100) == 300
    assert base_fare("1A", 100) == 500

# concession
def test_adult_no_concession():
    assert concession(30, "M", False) == 0

def test_tatkal_no_concession():
    assert concession(3, "F", True) == 0

def test_infant():
    assert concession(3, "M", False) == 100

def test_age_5_is_child():
    assert concession(5, "M", False) == 50

def test_child():
    assert concession(10, "F", False) == 50

def test_age_12_is_child():
    assert concession(12, "M", False) == 50

def test_age_13_is_adult():
    assert concession(13, "M", False) == 0

def test_senior_female():
    assert concession(65, "F", False) == 50

def test_senior_male():
    assert concession(65, "M", False) == 40

def test_age_60_boundary():
    assert concession(60, "M", False) == 40

def test_age_59_no_concession():
    assert concession(59, "F", False) == 0

# tatkal_charge
def test_tatkal_sleeper_min():
    assert tatkal_charge("SL", 500) == 100

def test_tatkal_sleeper_normal():
    assert tatkal_charge("SL", 2000) == 200   # covers 36->38

def test_tatkal_ac_max():
    assert tatkal_charge("1A", 5000) == 400

def test_tatkal_ac_normal():
    assert tatkal_charge("3A", 1000) == 300

def test_tatkal_ac_min():
    assert tatkal_charge("2A", 200) == 100

def test_tatkal_exact_limits():
    assert tatkal_charge("SL", 4000) == 400
    assert tatkal_charge("SL", 1000) == 100