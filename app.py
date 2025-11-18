import streamlit as st
from dataclasses import dataclass
from typing import List, Literal, Optional

# =========================
#  Page + Styling
# =========================

st.set_page_config(page_title="MealSync", layout="wide")

st.markdown(
    """
<style>
/* Background and main container */
body {
    background: radial-gradient(circle at top, #1e293b 0, #020617 55%, #020617 100%) !important;
    color: #e5e7eb !important;
}

section.main > div.block-container {
    padding-top: 1.25rem !important;
    padding-bottom: 2rem !important;
}

/* Title */
.mealsync-title {
    font-size: 3rem;
    font-weight: 800;
    color: #60a5fa;
    text-align: center;
    margin-bottom: 0.25rem;
}
.mealsync-subtitle {
    text-align: center;
    color: #9ca3af;
    margin-bottom: 1.5rem;
}

/* Week buttons */
div.week-buttons > div.stButton > button {
    border-radius: 999px !important;
    padding: 0.4rem 1.2rem !important;
    font-size: 0.9rem !important;
    border: 1px solid rgba(148,163,184,0.6) !important;
    background: rgba(15,23,42,0.4) !important;
    color: #e5e7eb !important;
}
div.week-buttons > div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #2563eb, #a855f7) !important;
    border: 1px solid transparent !important;
}
div.week-buttons > div.stButton > button:hover {
    filter: brightness(1.15) !important;
}

/* Generic buttons */
div.stButton > button {
    border-radius: 999px !important;
    border: 1px solid rgba(148,163,184,0.5) !important;
    background-color: rgba(15,23,42,0.8) !important;
    color: #e5e7eb !important;
    font-size: 0.8rem !important;
    padding: 0.28rem 0.9rem !important;
}
div.stButton > button:hover {
    background-color: rgba(30,64,175,0.9) !important;
}

/* Card container */
.day-card, .budgets-card, .summary-card {
    background: rgba(15,23,42,0.9) !important;
    border-radius: 1rem !important;
    padding: 1rem 1rem 0.75rem !important;
    border: 1px solid rgba(148,163,184,0.45) !important;
    box-shadow: 0 18px 45px rgba(15,23,42,0.9) !important;
}

/* Day headers */
.day-header {
    font-weight: bold !important;
    font-size: 1.1rem !important;
    margin-bottom: 0.55rem !important;
    color: #38bdf8 !important;
}
.day-header.sunday {
    color: #fb7185 !important;
}

/* Meal labels */
.meal-label {
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    color: #9ca3af !important;
    margin-bottom: 0.15rem !important;
}

/* Selectbox styling */
div.stSelectbox > div > div {
    background-color: rgba(15,23,42,0.95) !important;
    border-radius: 0.6rem !important;
    border: 1px solid rgba(148,163,184,0.6) !important;
}

/* Number input styling */
div.stNumberInput > div > div {
    background-color: rgba(15,23,42,0.95) !important;
    border-radius: 0.6rem !important;
    border: 1px solid rgba(148,163,184,0.6) !important;
}

/* Budgets */
.budgets-card-title {
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    margin-bottom: 0.4rem !important;
}
.budget-label {
    font-size: 0.85rem !important;
    color: #e5e7eb !important;
}
.budget-diff-positive {
    color: #4ade80 !important;
}
.budget-diff-negative {
    color: #f87171 !important;
}

/* Summary */
.summary-card-title {
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    margin-bottom: 0.6rem !important;
}
.summary-row {
    display: flex !important;
    justify-content: space-between !important;
    margin-bottom: 0.35rem !important;
}
.summary-value {
    font-size: 1rem !important;
    font-weight: 700 !important;
    color: #93c5fd !important;
}
</style>
    """,
    unsafe_allow_html=True,
)

# =========================
#  Data Models
# =========================

MealType = Literal["breakfast", "lunch", "dinner"]

@dataclass
class Meal:
    id: str
    name: str
    price: float

breakfast_options = [
    Meal("medu", "Medu vada", 20),
    Meal("pongal", "Pongal", 25),
    Meal("sambar", "Sambar vada", 32),
    Meal("curd", "Curd vada", 32),
    Meal("pav", "Pav bhaji", 38),
    Meal("alu", "Alu paratha", 38),
    Meal("mac", "Macaroni", 38),
    Meal("daal", "Daal poori", 38),
]

lunch_options = [
    Meal("l1", "Mess Lunch", 60),
    Meal("l2", "Special Lunch", 80),
]

dinner_options = [
    Meal("d1", "Mess Dinner", 60),
    Meal("d2", "Special Dinner", 80),
]

DEFAULTS = [
    {"week": 1, "day": 2, "meal_name": "Pav bhaji"},
    {"week": 3, "day": 3, "meal_name": "Pav bhaji"},
    {"week": 1, "day": 4, "meal_name": "Maggi"},   # Add Maggi to breakfast_options if you actually want it
    {"week": 1, "day": 6, "meal_name": "Alu paratha"},
    {"week": 4, "day": 4, "meal_name": "Alu paratha"},
    {"week": 2, "day": 4, "meal_name": "Macaroni"},
    {"week": 2, "day": 5, "meal_name": "Macaroni"},
    {"week": 4, "day": 6, "meal_name": "Daal poori"},
]

DEFAULT_BUDGETS = {
    "weekly": 840,
    "sunday": 2140,
    "weekdays": 3360,
    "grandTotal": 5500,
}

WEEK_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


# =========================
#  Helper Functions
# =========================

def get_meal_key(week: int, day: int) -> str:
    return f"w{week}-d{day}"

def find_breakfast_by_name(name: str) -> Optional[Meal]:
    for m in breakfast_options:
        if m.name.lower() == name.lower():
            return m
    return None

def get_default_meal(week: int, day: int) -> Optional[Meal]:
    real_day = day + 1
    for row in DEFAULTS:
        if row["week"] == week and row["day"] == real_day:
            return find_breakfast_by_name(row["meal_name"])
    return None

def get_breakfast_options(week: int, day: int) -> List[Meal]:
    main = get_default_meal(week, day)
    basics = [m for m in breakfast_options if m.name in ["Medu vada", "Pongal", "Sambar vada", "Curd vada"]]
    if main:
        return [main] + [x for x in basics if x.id != main.id]
    return basics

def get_meals(meal_type: MealType, week: int, day: int) -> List[Meal]:
    if meal_type == "breakfast":
        return get_breakfast_options(week, day)
    if meal_type == "lunch":
        return lunch_options
    if meal_type == "dinner":
        return dinner_options
    return []

def get_main_type(week: int, day: int) -> MealType:
    if day == 6:
        return "lunch"
    return st.session_state.day_meal_choice.get(get_meal_key(week, day), "breakfast")

def get_price(week: int, day: int, meal_type: MealType) -> float:
    sel_key = f"sel-{week}-{day}-{meal_type}"
    sel = st.session_state.get(sel_key, "skip")
    if sel == "skip":
        return 0.0
    if sel == "custom":
        price_key = f"price-{week}-{day}-{meal_type}"
        return float(st.session_state.get(price_key, 0.0) or 0.0)
    for m in get_meals(meal_type, week, day):
        if m.id == sel:
            return float(m.price)
    return 0.0

def weekly_cost(week: int) -> float:
    total = 0.0
    for d in range(6):
        total += get_price(week, d, get_main_type(week, d))
        total += get_price(week, d, "dinner")
    return total

def sunday_cost_all() -> float:
    return sum(get_price(w, 6, "lunch") + get_price(w, 6, "dinner") for w in range(1, 5))

def weekdays_cost_all() -> float:
    total = 0.0
    for w in range(1, 5):
        total += weekly_cost(w)
    return total

def format_diff(cost: float, budget: float) -> str:
    diff = budget - cost
    if abs(diff) < 1e-9:
        return ""
    sign = "+" if diff > 0 else ""
    color_class = "budget-diff-positive" if diff > 0 else "budget-diff-negative"
    return f"<span class='{color_class}'>({sign}{diff:.2f})</span>"


# =========================
#  Session State Init
# =========================

if "selected_week" not in st.session_state:
    st.session_state.selected_week = 1

if "day_meal_choice" not in st.session_state:
    st.session_state.day_meal_choice = {}

if "budgets_init" not in st.session_state:
    for k, v in DEFAULT_BUDGETS.items():
        st.session_state[f"budget-{k}"] = float(v)
    st.session_state.budgets_init = True


# =========================
#  Title
# =========================

st.markdown("<div class='mealsync-title'>MealSync</div>", unsafe_allow_html=True)
st.markdown("<div class='mealsync-subtitle'>Your weekly meal planning, simplified.</div>", unsafe_allow_html=True)


# =========================
#  Week Selector
# =========================

st.markdown("<div class='week-buttons'></div>", unsafe_allow_html=True)
week_cols = st.columns(4)
for i, col in enumerate(week_cols, start=1):
    with col:
        clicked = st.button(
            f"Week {i}",
            key=f"wk{i}",
            type=("primary" if st.session_state.selected_week == i else "secondary"),
        )
        if clicked:
            st.session_state.selected_week = i
            st.rerun()

week = st.session_state.selected_week
st.markdown("---")


# =========================
#  Main Day Grid
# =========================

day_cols = st.columns([1, 1, 1, 1, 1.2])

for day in range(7):
    col_index = day if day < 4 else day - 4
    col = day_cols[col_index]

    with col:
        st.markdown(
            f"<div class='day-card'><div class='day-header {'sunday' if day == 6 else ''}'>{WEEK_DAYS[day]}</div>",
            unsafe_allow_html=True,
        )

        # Breakfast/Lunch toggle for Mon–Sat
        if day != 6:
            key = get_meal_key(week, day)
            current = st.session_state.day_meal_choice.get(key, "breakfast")
            icon = "☕" if current == "breakfast" else "🍛"
            label = (
                f"{icon} Breakfast → switch to Lunch"
                if current == "breakfast"
                else f"{icon} Lunch → switch to Breakfast"
            )
            if st.button(label, key=f"tgl-{week}-{day}"):
                st.session_state.day_meal_choice[key] = "lunch" if current == "breakfast" else "breakfast"
                st.rerun()

        meal_types: List[MealType] = ["lunch", "dinner"] if day == 6 else [get_main_type(week, day), "dinner"]

        for mt in meal_types:
            icon = "☕" if mt == "breakfast" else ("☀️" if mt == "lunch" else "🌙")
            st.markdown(
                f"<div class='meal-label'>{icon} {mt.capitalize()}</div>",
                unsafe_allow_html=True,
            )

            sel_key = f"sel-{week}-{day}-{mt}"
            # Initial default selection
            if sel_key not in st.session_state:
                default = "skip"
                if mt == "breakfast":
                    d = get_default_meal(week, day)
                    if d:
                        default = d.id
                st.session_state[sel_key] = default

            options = ["skip"] + [m.id for m in get_meals(mt, week, day)] + ["custom"]
            labels = {
                "skip": "Skip meal",
                "custom": "Custom price",
            }
            for m in get_meals(mt, week, day):
                labels[m.id] = f"{m.name} (Rs. {m.price})"

            choice = st.selectbox(
                "",
                options,
                key=sel_key,
                format_func=lambda x: labels[x],
            )

            if choice == "custom":
                price_key = f"price-{week}-{day}-{mt}"
                if price_key not in st.session_state:
                    st.session_state[price_key] = 0.0
                st.number_input(
                    "Custom price",
                    min_value=0.0,
                    key=price_key,
                    label_visibility="collapsed",
                )

        st.markdown("</div>", unsafe_allow_html=True)


# =========================
#  Budgets Card
# =========================

with day_cols[-1]:
    st.markdown("<div class='budgets-card'>", unsafe_allow_html=True)
    st.markdown("<div class='budgets-card-title'>Budgets</div>", unsafe_allow_html=True)

    labels = {
        "weekly": "Week Total",
        "sunday": "Sunday Total",
        "weekdays": "Weekdays Total",
        "grandTotal": "Grand Total",
    }

    for key, label in labels.items():
        c1, c2 = st.columns([2, 1])

        # IMPORTANT: Button FIRST (updates session_state),
        # then number_input reads the updated value.
        with c2:
            if st.button("Default", key=f"reset-{key}"):
                st.session_state[f"budget-{key}"] = float(DEFAULT_BUDGETS[key])
                st.rerun()

        with c1:
            st.markdown(
                f"<div class='budget-label'>{label}</div>",
                unsafe_allow_html=True,
            )
            st.number_input(
                "Budget (Rs.)",
                min_value=0.0,
                step=10.0,
                key=f"budget-{key}",
                label_visibility="collapsed",
            )

    st.markdown("</div>", unsafe_allow_html=True)


# =========================
#  Summary Card
# =========================

bud = {k: float(st.session_state[f"budget-{k}"]) for k in DEFAULT_BUDGETS}

wk_cost = weekly_cost(week)
sun_cost = sunday_cost_all()
wd_cost = weekdays_cost_all()
grand_cost = sun_cost + wd_cost

st.markdown("")
st.markdown("<div class='summary-card'>", unsafe_allow_html=True)
st.markdown("<div class='summary-card-title'>Cost Summary</div>", unsafe_allow_html=True)

def row(lbl: str, val: float, budget_key: str):
    diff_html = format_diff(val, bud[budget_key])
    st.markdown(
        f"<div class='summary-row'><span>{lbl}</span>"
        f"<span class='summary-value'>Rs. {val:.2f} {diff_html}</span></div>",
        unsafe_allow_html=True,
    )

row("Current Week Total:", wk_cost, "weekly")
row("Sunday Total:", sun_cost, "sunday")
st.markdown("<hr/>", unsafe_allow_html=True)
row("Weekdays Total:", wd_cost, "weekdays")
row("Grand Total:", grand_cost, "grandTotal")

st.markdown("</div>", unsafe_allow_html=True)
