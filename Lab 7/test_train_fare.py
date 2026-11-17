from hypothesis import given, strategies as st
from train_fare import parse_pnr, journey_distance, berth_type


# ---------- Fuzz tests: random/bad input must never crash ----------

@given(st.text() | st.none())
def test_parse_pnr_no_crash(s):
    try:
        parse_pnr(s)
    except Exception as e:
        assert False, f"parse_pnr crashed with: {e!r}"


@given(st.text() | st.none())
def test_journey_distance_no_crash(s):
    try:
        journey_distance(s)
    except Exception as e:
        assert False, f"journey_distance crashed with: {e!r}"


@given(st.text() | st.none())
def test_berth_type_no_crash(s):
    try:
        berth_type(s)
    except Exception as e:
        assert False, f"berth_type crashed with: {e!r}"


# ---------- Property tests: valid input must give the right answer ----------

@given(st.from_regex(r"[0-9]{10}", fullmatch=True))
def test_parse_pnr_valid(pnr):
    assert parse_pnr(pnr) == (int(pnr[0]), int(pnr[1:]))


@given(st.lists(st.integers(min_value=0, max_value=5000), min_size=1).map(sorted))
def test_journey_distance_valid(stations):
    csv = ",".join(str(d) for d in stations)
    assert journey_distance(csv) == stations[-1] - stations[0]


@given(st.from_regex(r"[A-Za-z][A-Za-z0-9]{0,2}", fullmatch=True),
       st.integers(min_value=1, max_value=72))
def test_berth_type_valid(coach, number):
    coach_out, berth = berth_type(f"{coach}-{number}")
    assert coach_out == coach.upper()
    assert berth in {"LB", "MB", "UB", "SL", "SU"}