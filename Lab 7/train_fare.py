BERTHS = ["SU", "LB", "MB", "UB", "LB", "MB", "UB", "SL"]
MAX_SEAT = 72


def is_number(s):
    # isascii() blocks Unicode digits like '²' or '١' that int() rejects
    return isinstance(s, str) and s.isascii() and s.isdigit()


def parse_pnr(pnr):
    """Return (zone, number) for a 10-digit PNR, or None if invalid."""
    if not isinstance(pnr, str):
        return None
    pnr = pnr.strip()
    if len(pnr) != 10 or not is_number(pnr):
        return None
    return int(pnr[0]), int(pnr[1:])


def journey_distance(distances_csv):
    """Return last - first station distance, or None if invalid."""
    if not isinstance(distances_csv, str):
        return None
    parts = [p.strip() for p in distances_csv.split(',')]
    if not all(is_number(p) for p in parts):     # catches '', '1,,3', 'abc', '-5'
        return None
    distances = [int(p) for p in parts]
    if distances != sorted(distances):           # distances must not go backwards
        return None
    return distances[-1] - distances[0]


def berth_type(seat):
    """Return (coach, berth) for input like 'S3-45', or None if invalid."""
    if not isinstance(seat, str):
        return None
    parts = seat.strip().split('-')
    if len(parts) != 2:
        return None
    coach, number = parts[0].strip(), parts[1].strip()
    if not (coach.isascii() and coach.isalnum()) or not is_number(number):
        return None
    number = int(number)
    if not 1 <= number <= MAX_SEAT:
        return None
    return coach.upper(), BERTHS[number % 8]


def show(label, result):
    print(label, result if result is not None else "Invalid input")


def main():
    print("==== Running parse_pnr ====")
    user_input = input("Enter a 10 digit PNR (e.g. 4521367890): ")
    show("Zone and Number:", parse_pnr(user_input))

    print("\n==== Running journey_distance ====")
    user_input = input("Enter station distances as CSV (e.g. 0,120,340): ")
    show("Total Distance:", journey_distance(user_input))

    print("\n==== Running berth_type ====")
    user_input = input("Enter coach and seat (e.g. S3-45): ")
    show("Coach and Berth:", berth_type(user_input))


if __name__ == "__main__":
    main()