# # import datetime

# # SUITS = ["Cups", "Swords", "Wands", "Pentacles"]
# # NUMBERS = ["Two", "Three", "Four", "Five", "Six", "Sezeven", "Eight", "Nine", "Ten"]
# # NUMERIC_CARDS = [f"{n} of {s}" for s in SUITS for n in NUMBERS]  # 36 cards
# # COURT_RANKS = ["Page", "Knight", "Queen", "King"]
# # COURT_CARDS = [f"{r} of {s}" for s in SUITS for r in COURT_RANKS]  # 16 cards
# # MAJOR_ARCANA = [
# # "The Fool", "The Magician", "The High Priestess", "The Empress",
# # "The Emperor", "The Hierophant", "The Lovers", "The Chariot",
# # "Strength", "The Hermit", "Wheel of Fortune", "Justice",
# # "The Hanged Man", "Death", "Temperance", "The Devil",
# # "The Tower", "The Star", "The Moon", "The Sun",
# # "Judgement", "The World"
# # ]  # 22 cards

# # FULL_DECK = MAJOR_ARCANA + NUMERIC_CARDS + COURT_CARDS  # total 78
# # NEGATIVE_CARDS = [
# # "The Tower", "Five of Cups", "Three of Swords", "Ten of Swords"
# # ]
# # POLARITY = {card: ("negative" if card in NEGATIVE_CARDS else "positive") for card in FULL_DECK}

# # DATE_RANGES = {}
# # year = datetime.date.today().year
# # start_date = datetime.date(year, 1, 1)
# # for idx, card in enumerate(NUMERIC_CARDS):
# #     dr_start = start_date + datetime.timedelta(days=idx * 10)
# #     dr_end = dr_start + datetime.timedelta(days=9)
# #     DATE_RANGES[card] = (dr_start, dr_end)

# import datetime

# SUITS = ["Cups", "Swords", "Wands", "Pentacles"]
# NUMBERS = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"]
# COURTS = ["Page", "Knight", "Queen", "King"]

# MINOR_ARCANA = [f"{num} of {suit}" for suit in SUITS for num in NUMBERS + COURTS]

# MAJOR_ARCANA = [
#     "The Fool", "The Magician", "The High Priestess", "The Empress",
#     "The Emperor", "The Hierophant", "The Lovers", "The Chariot",
#     "Strength", "The Hermit", "Wheel of Fortune", "Justice",
#     "The Hanged Man", "Death", "Temperance", "The Devil",
#     "The Tower", "The Star", "The Moon", "The Sun",
#     "Judgement", "The World"
# ]

# FULL_DECK = MINOR_ARCANA + MAJOR_ARCANA

# # Numeric cards for timing
# NUMERIC_CARDS = [f"{num} of {suit}" for suit in SUITS for num in NUMBERS[1:]]

# def generate_date_ranges():
#     ranges = {}
#     year_start = datetime.date(datetime.date.today().year, 1, 1)
#     for i, card in enumerate(NUMERIC_CARDS):
#         start = year_start + datetime.timedelta(days=i*10)
#         end = start + datetime.timedelta(days=9)
#         ranges[card] = (start, end)
#     return ranges

# DATE_RANGES = generate_date_ranges()
# #whenprint(DATE_RANGES)
import datetime

SUITS = ["Cups", "Swords", "Wands", "Pentacles"]
NUMBERS = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"]
COURTS = ["Page", "Knight", "Queen", "King"]

MINOR_ARCANA = [f"{num} of {suit}" for suit in SUITS for num in NUMBERS + COURTS]

MAJOR_ARCANA = [
    "The Fool", "The Magician", "The High Priestess", "The Empress",
    "The Emperor", "The Hierophant", "The Lovers", "The Chariot",
    "Strength", "The Hermit", "Wheel of Fortune", "Justice",
    "The Hanged Man", "Death", "Temperance", "The Devil",
    "The Tower", "The Star", "The Moon", "The Sun",
    "Judgement", "The World"
]

FULL_DECK = MINOR_ARCANA + MAJOR_ARCANA
NUMERIC_CARDS = [f"{num} of {suit}" for suit in SUITS for num in NUMBERS[1:]]

def generate_date_ranges():
    today = datetime.date.today()
    current_year = today.year
    ranges = {}

    SEASONS = {
        "Cups": datetime.date(current_year, 3, 20),   # Spring
        "Wands": datetime.date(current_year, 6, 21),  # Summer
        "Swords": datetime.date(current_year, 9, 22), # Autumn
        "Pentacles": datetime.date(current_year, 12, 21), # Winter
    }

    for suit in SUITS:
        season_start = SEASONS[suit]
        for i, num in enumerate(NUMBERS[1:]):
            card = f"{num} of {suit}"
            start = season_start + datetime.timedelta(days=i * 10)
            end = start + datetime.timedelta(days=9)

            # Push to next year if needed
            if end < today:
                start = start.replace(year=current_year + 1)
                end = end.replace(year=current_year + 1)

            ranges[card] = (start, end)

    return ranges

DATE_RANGES = generate_date_ranges()

