import streamlit as st
from dataclasses import dataclass
from typing import List, Literal, Optional

# =========================
#  Page + global styling
# =========================

st.set_page_config(page_title="MealSync", layout="wide")

# Custom CSS to mimic the dark, card-based UI
st.markdown(
    """
<style>
/* Background + overall layout */
body {
    background: radial-gradient(circle at top, #1e293b 0, #020617 45%, #020617 100%) !important;
    color: #e5e7eb !important;
}

section.main > div.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* Main title */
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

/* Week buttons (pill style) */
div.week-buttons > div.stButton > button {
    border-radius: 999px;
    padding: 0.35rem 1.2rem;
    font-size: 0.9rem;
    border: 1px solid rgba(148,163,184,0.6);
    background: transparent;
    color: #e5e7eb;
    transition: all 0.15s ease;
}
div.week-buttons > div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #2563eb, #a855f7);
    border-color: transparent;
}
div.week-buttons > div.stButton > button:hover {
    filter: brightness(1.05);
}

/* Generic primary buttons (toggle, defaults, etc.) */
div.stButton > button {
    border-radius: 999px;
    border: 1px solid rgba(148,163,184,0.5);
    background-color: rgba(15,23,42,0.8);
    color: #e5e7eb;
    font-size: 0.8rem;
    padding: 0.3rem 0.9rem;
}
div.stButton > button:hover {
    background-color: rgba(30,64,175,0.9);
}

/* Card containers */
.day-card, .budgets-card, .summary-card {
    background: rgba(15,23,42,0.9);
    border-radius: 1rem;
    padding: 1rem 1rem 0.75rem;
    border: 1px solid rgba(148,163,184,0.45);
    box-shadow: 0 18px 45px rgba(15,23,42,0.9);
}

/* Day header */
.day-header {
    font-weight: 700;
    font-size: 1.05rem;
    margin-bottom: 0.4rem;
    color: #38bdf8;
}
.day-header.sunday {
    color: #fb7185;
}

/* Meal label */
.meal-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #9ca3af;
    margin-bottom: 0.15rem;
}

/* Select boxes */
div.stSelectbox label {
    font-size: 0.7rem;
    color: #94a3b8;
}
div.stSelectbox > div > div {
    background-color: rgba(15,23,42,0.95);
    border-radius: 0.6rem;
    border: 1px solid rgba(148,163,184,0.6);
}

/* Number inputs (custom price + budgets) */
div.stNumberInput > div > div {
    background-color: rgba(15,23,42,0.95);
    border-radius: 0.6rem;
    border: 1px solid rgba(148,163,184,0.6);
}

/* Budgets */
.budgets-card-title {
    font-size: 1.05rem;
    font-weight: 600;
    margin-bottom: 0.4rem;
}
.budget-label {
    font-size: 0.85rem;
    color: #e5e7eb;
}
.budget-diff-positive {
    color: #4ade80;
    font-size: 0.8rem;
}
.budget-diff-negative {
    color: #f97373;
    font-size: 0.8rem;
}

/* Cost summary */
.summary-card-title {
    font-size: 1.05rem;
    font-weight: 600;
    margin-bottom: 0.6rem;
}
.summary-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.4rem;
}
.summary-label {
    font-size: 0.9rem;
}
.summary-value {
    font-size: 1rem;
    font-weight: 700;
    color: #e5e7eb;
}
.summary-accent {
    color: #38bdf8;
}

/* Shrink top label spaces */
.stMarkdown {
    margin-bottom: 0.05rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================
#  Data models & options
# =========================

MealType = Literal["breakfast", "lunch", "dinner"]

@dataclass
class Meal:
    id: str
    name: str
    price: float

# Breakfast options (adapt prices if needed)
breakfast_options: List[Meal] = [
    Meal("medu-vada", "Medu vada", 20.0),
    Meal("pongal", "Pongal", 25.0),
    Meal("sambar-vada", "Sambar vada", 32.0),
    Meal("curd-vada", "Curd vada", 32.0),
    Meal("pav-bhaji", "Pav bhaji", 38.0),
    Meal("alu-paratha", "Alu paratha", 38.0),
    Meal("macaroni", "Macaroni", 38.0),
    Meal("daal-poori", "Daal poori", 38.0),
]

# Simple placeholders for lunch/dinner
lunch_options: List[Meal] = [
    Meal("mess-lunch", "Mess Lunch", 60.0),
    Meal("special-lunch", "Special Lunch", 80.0),
]

dinner_options: List[Meal] = [
    Meal("mess-dinner", "Mess Dinner", 60.0),
    Meal("special-dinner", "Special Dinner", 80.0),
]

# Defaults copied from your React logic
DEFAULTS = [
    {"week": 1, "day": 2, "meal_name": "Pav bhaji"},
    {"week": 3, "day": 3, "meal_name": "Pav bhaji"},
    {"week": 1, "day": 4, "meal_name": "Maggi"},       # add Maggi to options if you want it
    {"week": 1, "day": 6, "meal_name": "Alu paratha"},
    {"week": 4, "day": 4, "meal_name": "Alu paratha"},
    {"week": 2, "day": 4, "meal_name": "Macaroni"},
    {"week": 2, "day": 5, "meal_name": "Macaroni"},
    {"week": 4, "day": 6, "meal_name": "Daal poori"},
]

DEFAULT_BUDGETS = {
    "weekly": 840.0,
    "sunday": 2140.0,
    "weekdays": 3360.0,
    "grandTotal": 5500.0,
}

WEEK_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


# =========================
#  Helper functions
# =========================

def get_meal_key(week: int, day_index: int) -> str:
    return f"w{week}-d{day_index}"


def find_breakfast_by_name(name: str) -> Optional[Meal]:
    for m in breakfast_options:
        if m.name.lower() == name.lower():
            return m
    return None


def get_default_meal_for(week: int, day_index: int) -> Optional[Meal]:
    day_of_week = day_index + 1
    for item in DEFAULTS:
        if item["week"] == week and item["day"] == day_of_week:
            return find_breakfast_by_name(item["meal_name"])
    return None


def get_breakfast_options_for(week: int, day_index: int) -> List[Meal]:
    specific_names = {"Medu vada", "Pongal", "Sambar vada", "Curd vada"}
    specific = [m for m in breakfast_options if m.name in specific_names]

    default_meal = get_default_meal_for(week, day_index)
    if default_meal and default_meal in breakfast_options:
        rest = [m for m in specific if m.id != default_meal.id]
        return [default_meal] + rest
    return specific


def get_options_for_meal_type(meal_type: MealType, week: int, day_index: int) -> List[Meal]:
    if meal_type == "breakfast":
        return get_breakfast_options_for(week, day_index)
    if meal_type == "lunch":
        return lunch_options
    if meal_type == "dinner":
        return dinner_options
    return []


def get_main_meal_type(week: int, day_index: int) -> MealType:
    if day_index == 6:  # Sunday
        return "lunch"
    key = get_meal_key(week, day_index)
    return st.session_state.day_meal_choices.get(key, "breakfast")


def get_meal_price(week: int, day_index: int, meal_type: MealType) -> float:
    select_key = f"sel-w{week}-d{day_index}-{meal_type}"
    choice = st.session_state.get(select_key, "skip")
    if choice == "skip":
        return 0.0
    if choice == "custom":
        price_key = f"price-w{week}-d{day_index}-{meal_type}"
        return float(st.session_state.get(price_key, 0.0) or 0.0)
    meals = get_options_for_meal_type(meal_type, week, day_index)
    for m in meals:
        if m.id == choice:
            return m.price
    return 0.0


def weekly_cost_for(week: int) -> float:
    total = 0.0
    for day_index in range(6):  # Mon–Sat
        main_type = get_main_meal_type(week, day_index)
        total += get_meal_price(week, day_index, main_type)
        total += get_meal_price(week, day_index, "dinner")
    return total


def sunday_cost_for(week: int) -> float:
    return get_meal_price(week, 6, "lunch") + get_meal_price(week, 6, "dinner")


def format_difference(cost: float, budget: float) -> str:
    diff = budget - cost
    if abs(diff) < 1e-9:
        return ""
    sign = "+" if diff > 0 else ""
    word = "under" if diff > 0 else "over"
    return f"{sign}{diff:.2f} {word} budget"


# =========================
#  Session state init
# =========================

if "selected_week" not in st.session_state:
    st.session_state.selected_week = 1

if "day_meal_choices" not in st.session_state:
    st.session_state.day_meal_choices = {}

if "budgets_initialized" not in st.session_state:
    for k, v in DEFAULT_BUDGETS.items():
        st.session_state[f"budget-{k}"] = float(v)
    st.session_state.budgets_initialized = True

# =========================
#  Top title
# =========================

st.markdown("<div class='mealsync-title'>MealSync</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='mealsync-subtitle'>Your weekly meal planning, simplified.</div>",
    unsafe_allow_html=True,
)

# =========================
#  Week selector row
# =========================

week_row = st.container()
with week_row:
    cols = st.columns(4, gap="small")
    st.markdown("<div class='week-buttons'></div>", unsafe_allow_html=True)
    for i, col in enumerate(cols, start=1):
        with col:
            kind = "primary" if st.session_state.selected_week == i else "secondary"
            if st.button(
                f"Week {i}",
                key=f"week-btn-{i}",
                type=kind,
            ):
                st.session_state.selected_week = i
                st.rerun()

selected_week = st.session_state.selected_week

st.markdown("---")

# =========================
#  Day cards
# =========================

day_cols = st.columns([1, 1, 1, 1, 1.2])  # last column for budgets card

for day_index in range(7):
    col_index = day_index if day_index < 4 else day_index - 4
    col = day_cols[col_index]

    is_sunday = (day_index == 6)
    icon_day = ""  # you can add a small icon to header if you want
    day_label = WEEK_DAYS[day_index]

    with col:
        # Open card
        header_class = "day-header sunday" if is_sunday else "day-header"
        st.markdown(
            f"<div class='day-card'>"
            f"<div class='{header_class}'>{day_label}</div>",
            unsafe_allow_html=True,
        )

        # Breakfast/lunch toggle (Mon–Sat)
        if not is_sunday:
            key = get_meal_key(selected_week, day_index)
            current_choice: MealType = st.session_state.day_meal_choices.get(
                key, "breakfast"
            )
            icon = "☕" if current_choice == "breakfast" else "🍛"
            toggle_label = (
                f"{icon}  Breakfast → tap to show Lunch"
                if current_choice == "breakfast"
                else f"{icon}  Lunch → tap to show Breakfast"
            )
            if st.button(
                toggle_label,
                key=f"toggle-{selected_week}-{day_index}",
            ):
                new_choice = "lunch" if current_choice == "breakfast" else "breakfast"
                st.session_state.day_meal_choices[key] = new_choice
                st.rerun()

        # Meal select boxes
        if is_sunday:
            main_meal_types: List[MealType] = ["lunch", "dinner"]
        else:
            main_meal_types = [get_main_meal_type(selected_week, day_index), "dinner"]

        for meal_type in main_meal_types:
            pretty = meal_type.capitalize()
            icon = "☕" if meal_type == "breakfast" else ("☀️" if meal_type == "lunch" else "🌙")
            st.markdown(
                f"<div class='meal-label'>{icon} {pretty}</div>",
                unsafe_allow_html=True,
            )

            options_meals = get_options_for_meal_type(
                meal_type, selected_week, day_index
            )

            option_values = ["skip"] + [m.id for m in options_meals] + ["custom"]
            labels = {
                "skip": "Skip this meal",
                "custom": "Custom meal (enter price)",
            }
            for m in options_meals:
                labels[m.id] = f"{m.name} (Rs. {m.price:.2f})"

            select_key = f"sel-w{selected_week}-d{day_index}-{meal_type}"

            # Initial default
            if select_key not in st.session_state:
                default_val = "skip"
                if meal_type == "breakfast":
                    default_meal = get_default_meal_for(selected_week, day_index)
                    if default_meal:
                        default_val = default_meal.id
                st.session_state[select_key] = default_val

            choice = st.selectbox(
                " ",
                option_values,
                key=select_key,
                format_func=lambda v: labels[v],
                label_visibility="collapsed",
            )

            if choice == "custom":
                price_key = f"price-w{selected_week}-d{day_index}-{meal_type}"
                if price_key not in st.session_state:
                    st.session_state[price_key] = 0.0
                st.number_input(
                    "Custom price (Rs.)",
                    min_value=0.0,
                    step=1.0,
                    key=price_key,
                    label_visibility="collapsed",
                )

        # Close card
        st.markdown("</div>", unsafe_allow_html=True)

# =========================
#  Budgets card (right-most column)
# =========================

with day_cols[-1]:
    st.markdown("<div class='budgets-card'>", unsafe_allow_html=True)
    st.markdown("<div class='budgets-card-title'>Budgets</div>", unsafe_allow_html=True)

    budget_labels = {
        "weekly": "Week Total",
        "sunday": "Sunday Total",
        "weekdays": "Weekdays Total",
        "grandTotal": "Grand Total",
    }

    for key, label in budget_labels.items():
        budget_value = st.session_state.get(f"budget-{key}", DEFAULT_BUDGETS[key])
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown(f"<div class='budget-label'>{label}</div>", unsafe_allow_html=True)
            st.number_input(
                "Budget (Rs.)",
                min_value=0.0,
                step=10.0,
                key=f"budget-{key}",
                value=float(budget_value),
                label_visibility="collapsed",
            )
        with c2:
            if st.button("Default", key=f"reset-{key}"):
                st.session_state[f"budget-{key}"] = DEFAULT_BUDGETS[key]
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
#  Cost summary card
# =========================

budgets = {
    k: float(st.session_state[f"budget-{k}"])
    for k in DEFAULT_BUDGETS.keys()
}

weekly_cost = weekly_cost_for(selected_week)
sunday_total = sum(sunday_cost_for(week) for week in range(1, 5))
weekdays_total = sum(weekly_cost_for(week) for week in range(1, 5))
grand_total = sunday_total + weekdays_total

st.markdown("")
summary_col = st.container()
with summary_col:
    st.markdown("<div class='summary-card'>", unsafe_allow_html=True)
    st.markdown("<div class='summary-card-title'>Cost Summary</div>", unsafe_allow_html=True)

    def row(label, value, budget_key):
        diff_text = format_difference(value, budgets[budget_key])
        diff_class = ""
        if diff_text != "":
            diff_class = (
                "budget-diff-positive"
                if "under" in diff_text
                else "budget-diff-negative"
            )
        st.markdown(
            f"<div class='summary-row'>"
            f"<span class='summary-label'>{label}</span>"
            f"<span class='summary-value summary-accent'>Rs. {value:.2f}"
            f"{'' if diff_text == '' else f' <span class=\"{diff_class}\">({diff_text})</span>'}"
            f"</span></div>",
            unsafe_allow_html=True,
        )

    row("Current Week Total:", weekly_cost, "weekly")
    row("Sunday Total:", sunday_total, "sunday")
    st.markdown("<hr/>", unsafe_allow_html=True)
    row("Weekdays Total:", weekdays_total, "weekdays")
    row("Grand Total:", grand_total, "grandTotal")

    st.markdown("</div>", unsafe_allow_html=True)
