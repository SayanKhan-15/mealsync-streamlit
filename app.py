import streamlit as st
from dataclasses import dataclass
from typing import List, Literal, Optional

# =========================
# Page + Styling
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
    background: rgba(15,23,42,0.95) !important;
    border-radius: 1rem !important;
    padding: 1rem 1rem 0.75rem !important;
    border: 1px solid rgba(148,163,184,0.45) !important;
    box-shadow: 0 18px 45px rgba(15,23,42,0.9) !important;
    margin-bottom: 0.8rem;
}

/* Day headers */
.day-header {
    font-weight: bold !important;
    font-size: 1.05rem !important;
    margin-bottom: 0.45rem !important;
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
    margin-bottom: 0.12rem !important;
}

/* Selectbox styling */
div.stSelectbox > div > div {
    background-color: rgba(15,23,42,0.95) !important;
    border-radius: 0.6rem !important;
    border: 1px solid rgba(148,163,184,0.6) !important;
}

/* Text input styling (for budgets/custom price) */
div.stTextInput > div > input[type="text"] {
    background-color: rgba(15,23,42,0.95) !important;
    border-radius: 0.6rem !important;
    border: 1px solid rgba(148,163,184,0.6) !important;
    padding: 0.45rem !important;
    color: #e5e7eb !important;
}

/* Budgets */
.budgets-card-title {
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    margin-bottom: 0.45rem !important;
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
    font-size: 1.05rem !important;
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
# Data models & options
# =========================

MealType = Literal["breakfast", "lunch", "dinner"]

@dataclass
class Meal:
    id: str
    name: str
    price: float

# Breakfast / lunch / dinner options (adjust prices / names if needed)
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

lunch_options: List[Meal] = [
    Meal("mess-lunch", "Mess Lunch", 60.0),
    Meal("special-lunch", "Special Lunch", 80.0),
]

dinner_options: List[Meal] = [
    Meal("mess-dinner", "Mess Dinner", 60.0),
    Meal("special-dinner", "Special Dinner", 80.0),
]

DEFAULTS = [
    {"week": 1, "day": 2, "meal_name": "Pav bhaji"},
    {"week": 3, "day": 3, "meal_name": "Pav bhaji"},
    {"week": 1, "day": 4, "meal_name": "Maggi"},        # add Maggi if you want to include it
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
# Helpers
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
    if default_meal:
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
    if day_index == 6:
        return "lunch"
    key = get_meal_key(week, day_index)
    return st.session_state.day_meal_choices.get(key, "breakfast")

def parse_float_safe(value: str, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default

def get_meal_price(week: int, day_index: int, meal_type: MealType) -> float:
    sel_key = f"sel-w{week}-d{day_index}-{meal_type}"
    sel = st.session_state.get(sel_key, "skip")
    if sel == "skip":
        return 0.0
    if sel == "custom":
        price_key = f"price-w{week}-d{day_index}-{meal_type}"
        return parse_float_safe(st.session_state.get(price_key, "0"))
    meals = get_options_for_meal_type(meal_type, week, day_index)
    for m in meals:
        if m.id == sel:
            return m.price
    return 0.0

def weekly_cost_for(week: int) -> float:
    total = 0.0
    for day_index in range(6):  # Mon–Sat
        main_type = get_main_meal_type(week, day_index)
        total += get_meal_price(week, day_index, main_type)
        total += get_meal_price(week, day_index, "dinner")
    return total

def sunday_total_cost_all_weeks() -> float:
    tot = 0.0
    for w in range(1,5):
        tot += get_meal_price(w, 6, "lunch")
        tot += get_meal_price(w, 6, "dinner")
    return tot

def weekdays_total_cost_all_weeks() -> float:
    tot = 0.0
    for w in range(1,5):
        tot += weekly_cost_for(w)
    return tot

def format_difference_html(cost: float, budget: float) -> str:
    diff = budget - cost
    if abs(diff) < 1e-9:
        return ""
    sign = "+" if diff > 0 else ""
    cls = "budget-diff-positive" if diff > 0 else "budget-diff-negative"
    return f" <span class='{cls}'>({sign}{diff:.2f})</span>"

# =========================
# Session state initialization
# =========================

if "selected_week" not in st.session_state:
    st.session_state.selected_week = 1

if "day_meal_choices" not in st.session_state:
    st.session_state.day_meal_choices = {}

# Budgets stored as strings so we can use text_input (no +/- spinner)
if "budgets_initialized" not in st.session_state:
    for k, v in DEFAULT_BUDGETS.items():
        st.session_state[f"budget-{k}"] = f"{float(v):.2f}"
    st.session_state.budgets_initialized = True

# =========================
# UI: Title + Week selector
# =========================

st.markdown("<div class='mealsync-title'>MealSync</div>", unsafe_allow_html=True)
st.markdown("<div class='mealsync-subtitle'>Your weekly meal planning, simplified.</div>", unsafe_allow_html=True)

st.markdown("<div class='week-buttons'></div>", unsafe_allow_html=True)
week_cols = st.columns(4)
for i, col in enumerate(week_cols, start=1):
    with col:
        clicked = st.button(
            f"Week {i}",
            key=f"week-btn-{i}",
            type=("primary" if st.session_state.selected_week == i else "secondary"),
        )
        if clicked:
            st.session_state.selected_week = i
            st.rerun()

selected_week = st.session_state.selected_week
st.markdown("---")

# =========================
# 2x4 Grid: first 7 are days, 8th is budgets
# =========================

rows = 2
cols_per_row = 4
cell_index = 0

for r in range(rows):
    cols = st.columns(cols_per_row, gap="small")
    for c_idx, col in enumerate(cols):
        with col:
            # If this cell is one of the first 7, show a day card
            if cell_index < 7:
                day_index = cell_index  # 0..6
                is_sunday = (day_index == 6)
                header_class = "day-header sunday" if is_sunday else "day-header"
                st.markdown(f"<div class='day-card'><div class='{header_class}'>{WEEK_DAYS[day_index]}</div>", unsafe_allow_html=True)

                # Toggle (Mon–Sat) between breakfast & lunch
                if not is_sunday:
                    key = get_meal_key(selected_week, day_index)
                    current_choice = st.session_state.day_meal_choices.get(key, "breakfast")
                    icon = "☕" if current_choice == "breakfast" else "🍛"
                    toggle_label = (
                        f"{icon} Breakfast — click to show Lunch"
                        if current_choice == "breakfast"
                        else f"{icon} Lunch — click to show Breakfast"
                    )
                    if st.button(toggle_label, key=f"toggle-{selected_week}-{day_index}"):
                        st.session_state.day_meal_choices[key] = "lunch" if current_choice == "breakfast" else "breakfast"
                        st.rerun()

                # Which meal types to show
                if is_sunday:
                    main_meal_types: List[MealType] = ["lunch", "dinner"]
                else:
                    main_meal_types = [get_main_meal_type(selected_week, day_index), "dinner"]

                for mt in main_meal_types:
                    pretty = mt.capitalize()
                    icon = "☕" if mt == "breakfast" else ("☀️" if mt == "lunch" else "🌙")
                    st.markdown(f"<div class='meal-label'>{icon} {pretty}</div>", unsafe_allow_html=True)

                    # Option list: skip + options + custom
                    options_meals = get_options_for_meal_type(mt, selected_week, day_index)
                    option_values = ["skip"] + [m.id for m in options_meals] + ["custom"]
                    labels = {"skip": "Skip this meal", "custom": "Custom price (type Rs.)"}
                    for m in options_meals:
                        labels[m.id] = f"{m.name} (Rs. {m.price:.2f})"

                    select_key = f"sel-w{selected_week}-d{day_index}-{mt}"
                    if select_key not in st.session_state:
                        default_val = "skip"
                        if mt == "breakfast":
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

                    # Custom price: use text_input (no +/-). store as string.
                    if choice == "custom":
                        price_key = f"price-w{selected_week}-d{day_index}-{mt}"
                        if price_key not in st.session_state:
                            st.session_state[price_key] = "0"
                        st.text_input(
                            "Custom price (Rs.)",
                            key=price_key,
                            label_visibility="collapsed",
                        )

                st.markdown("</div>", unsafe_allow_html=True)

            else:
                # 8th cell --> Budgets card
                st.markdown("<div class='budgets-card'>", unsafe_allow_html=True)
                st.markdown("<div class='budgets-card-title'>Budgets</div>", unsafe_allow_html=True)

                budget_labels = {
                    "weekly": "Week Total",
                    "sunday": "Sunday Total (all 4 weeks)",
                    "weekdays": "Weekdays Total (all 4 weeks)",
                    "grandTotal": "Grand Total",
                }

                # We'll place a small reset button first then the text input so setting happens safely
                for key, label in budget_labels.items():
                    # Button column + input column
                    b_col, i_col = st.columns([1, 3])
                    with b_col:
                        if st.button("Default", key=f"reset-{key}"):
                            st.session_state[f"budget-{key}"] = f"{float(DEFAULT_BUDGETS[key]):.2f}"
                            st.rerun()
                    with i_col:
                        # Ensure key exists (string)
                        if f"budget-{key}" not in st.session_state:
                            st.session_state[f"budget-{key}"] = f"{float(DEFAULT_BUDGETS[key]):.2f}"
                        # text_input (no +/-)
                        st.markdown(f"<div class='budget-label'>{label}</div>", unsafe_allow_html=True)
                        st.text_input(
                            "Budget (Rs.)",
                            key=f"budget-{key}",
                            label_visibility="collapsed",
                        )

                st.markdown("</div>", unsafe_allow_html=True)

        cell_index += 1

# =========================
# Cost summary (below grid)
# =========================

# Read budgets (parse strings safely)
budgets = {}
for k in DEFAULT_BUDGETS.keys():
    raw = st.session_state.get(f"budget-{k}", f"{DEFAULT_BUDGETS[k]:.2f}")
    budgets[k] = parse_float_safe(raw, DEFAULT_BUDGETS[k])

weekly_cost = weekly_cost_for(selected_week)
sunday_cost = sunday_total_cost_all_weeks()
weekdays_cost = weekdays_total_cost_all_weeks()
grand_total_cost = sunday_cost + weekdays_cost

st.markdown("")  # spacing
st.markdown("<div class='summary-card'>", unsafe_allow_html=True)
st.markdown("<div class='summary-card-title'>Cost Summary</div>", unsafe_allow_html=True)

def render_row(label: str, value: float, budget_key: str):
    diff_html = format_difference_html(value, budgets[budget_key])
    st.markdown(
        f"<div class='summary-row'><span>{label}</span>"
        f"<span class='summary-value'>Rs. {value:.2f}{diff_html}</span></div>",
        unsafe_allow_html=True,
    )

render_row("Current Week Total:", weekly_cost, "weekly")
render_row("Sunday Total:", sunday_cost, "sunday")
st.markdown("<hr/>", unsafe_allow_html=True)
render_row("Weekdays Total:", weekdays_cost, "weekdays")
render_row("Grand Total:", grand_total_cost, "grandTotal")

st.markdown("</div>", unsafe_allow_html=True)
