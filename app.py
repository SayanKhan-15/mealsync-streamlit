import streamlit as st
from dataclasses import dataclass
from typing import List, Literal, Optional

# -------------------------
# Page config & CSS
# -------------------------
st.set_page_config(page_title="MealSync", layout="wide")

st.markdown(
    """
<style>
/* Page background */
body {
  background: radial-gradient(circle at top left, rgba(15,23,42,1) 0%, rgba(2,6,23,1) 65%);
  color: #e5e7eb;
}

/* Container padding */
section.main > div.block-container {
  padding-top: 0.75rem;
  padding-bottom: 1.25rem;
}

/* Title */
.mealsync-title {
  font-size: 2.4rem;
  font-weight: 800;
  color: #7dd3fc;
  text-align: center;
  margin-bottom: 0.15rem;
}
.mealsync-subtitle {
  text-align: center;
  color: #9ca3af;
  margin-bottom: 0.75rem;
}

/* Week buttons row */
div.week-buttons > div.stButton > button {
  border-radius: 999px !important;
  padding: 0.32rem 0.9rem !important;
  font-size: 0.84rem !important;
  border: 1px solid rgba(148,163,184,0.5) !important;
  background: rgba(15,23,42,0.7) !important;
  color: #e5e7eb !important;
  white-space: nowrap !important;
}
div.week-buttons > div.stButton > button[kind="primary"] {
  background: linear-gradient(135deg,#2563eb,#7c3aed) !important;
  color: #ffffff !important;
  border: none !important;
}

/* All buttons: single line, subtle */
div.stButton > button {
  white-space: nowrap;
  min-width: 76px;
  border-radius: 999px;
  padding: 4px 10px;
  background-color: rgba(15,23,42,0.9);
  color: #e5e7eb;
  border: 1px solid rgba(148,163,184,0.4);
  font-size: 0.8rem;
}

/* Rectangular frame for cards (days + budgets) */
.card {
  background-color: rgba(15,23,42,0.9);
  border-radius: 6px;
  border: 1px solid rgba(148,163,184,0.55);
  padding: 8px 10px 8px 10px;
  margin: 2px 0;           /* very small vertical margin */
  box-shadow: none;        /* no heavy glow */
}

/* Remove extra top gap from first markdown inside card */
.card > .stMarkdown {
  margin-top: 0 !important;
}

/* Day header inside card */
.card .day-header {
  font-weight: 700;
  font-size: 1.0rem;
  margin: 0 0 4px 0;
  color: #e0f2fe;
}
.card .day-header.sunday {
  color: #fecaca;
}

/* Meal label */
.meal-label {
  font-size: 0.72rem;
  color: #9ca3af;
  margin: 6px 0 3px 0;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

/* Selectbox rounded */
div.stSelectbox > div > div {
  border-radius: 6px;
  background-color: rgba(15,23,42,1);
  border: 1px solid rgba(148,163,184,0.45);
  color: #e5e7eb;
}

/* Text input (for custom price + budgets) */
div.stTextInput > div > input[type="text"] {
  background-color: rgba(15,23,42,1);
  border-radius: 6px;
  border: 1px solid rgba(148,163,184,0.45);
  color: #e5e7eb;
  padding: 6px 8px;
}

/* Budgets heading */
.budgets-title {
  font-weight: 700;
  color: #e0f2fe;
  margin: 0 0 4px 0;
}

/* Budget label text */
.budget-label {
  color: #cbd5f5;
  margin-bottom: 2px;
  font-size: 0.84rem;
}

/* Summary block */
.summary-card {
  background-color: rgba(15,23,42,0.9);
  border-radius: 6px;
  border: 1px solid rgba(148,163,184,0.5);
  padding: 10px;
  margin-top: 6px;
}

/* Summary diffs */
.diff-positive { color: #4ade80; font-weight: 600; }
.diff-negative { color: #fb7185; font-weight: 600; }

</style>
""",
    unsafe_allow_html=True,
)

# -------------------------
# Data models & options
# -------------------------
MealType = Literal["breakfast", "lunch", "dinner"]

@dataclass
class Meal:
    id: str
    name: str
    price: float

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
    {"week": 1, "day": 4, "meal_name": "Maggi"},
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

# -------------------------
# Helpers
# -------------------------
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
    for d in range(6):
        total += get_meal_price(week, d, get_main_meal_type(week, d))
        total += get_meal_price(week, d, "dinner")
    return total

def sunday_total_cost_all_weeks() -> float:
    tot = 0.0
    for w in range(1, 5):
        tot += get_meal_price(w, 6, "lunch")
        tot += get_meal_price(w, 6, "dinner")
    return tot

def weekdays_total_cost_all_weeks() -> float:
    tot = 0.0
    for w in range(1, 5):
        tot += weekly_cost_for(w)
    return tot

def format_difference_html(cost: float, budget: float) -> str:
    diff = budget - cost
    if abs(diff) < 1e-9:
        return ""
    sign = "+" if diff > 0 else ""
    cls = "diff-positive" if diff > 0 else "diff-negative"
    return f" <span class='{cls}'>({sign}{diff:.2f})</span>"

# -------------------------
# Session state init
# -------------------------
if "selected_week" not in st.session_state:
    st.session_state.selected_week = 1

if "day_meal_choices" not in st.session_state:
    st.session_state.day_meal_choices = {}

if "budgets_initialized" not in st.session_state:
    for k, v in DEFAULT_BUDGETS.items():
        st.session_state[f"budget-{k}"] = f"{float(v):.2f}"
    st.session_state.budgets_initialized = True

# -------------------------
# Top UI
# -------------------------
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

# -------------------------
# 2x4 grid: 7 day cards + 1 budget card
# -------------------------
rows = 2
cols_per_row = 4
cell_index = 0

for r in range(rows):
    row_cols = st.columns(cols_per_row, gap="small")
    for col in row_cols:
        with col:
            if cell_index < 7:
                day_index = cell_index
                is_sunday = (day_index == 6)

                st.markdown("<div class='card'>", unsafe_allow_html=True)

                # Day header
                header_cls = "day-header sunday" if is_sunday else "day-header"
                st.markdown(f"<div class='{header_cls}'>{WEEK_DAYS[day_index]}</div>", unsafe_allow_html=True)

                # Toggle breakfast/lunch for Mon–Sat
                if not is_sunday:
                    key = get_meal_key(selected_week, day_index)
                    cur = st.session_state.day_meal_choices.get(key, "breakfast")
                    icon = "☕" if cur == "breakfast" else "🍛"
                    label = f"{icon} {cur.capitalize()} — click to switch"
                    if st.button(label, key=f"toggle-{selected_week}-{day_index}"):
                        st.session_state.day_meal_choices[key] = "lunch" if cur == "breakfast" else "breakfast"
                        st.rerun()

                # Which meal types to show
                if is_sunday:
                    meal_types: List[MealType] = ["lunch", "dinner"]
                else:
                    meal_types = [get_main_meal_type(selected_week, day_index), "dinner"]

                for mt in meal_types:
                    pretty = mt.capitalize()
                    icon = "☕" if mt == "breakfast" else ("☀️" if mt == "lunch" else "🌙")
                    st.markdown(f"<div class='meal-label'>{icon} {pretty}</div>", unsafe_allow_html=True)

                    meals = get_options_for_meal_type(mt, selected_week, day_index)
                    option_values = ["skip"] + [m.id for m in meals] + ["custom"]
                    labels = {
                        "skip": "Skip this meal",
                        "custom": "Custom price (type Rs.)",
                    }
                    for m in meals:
                        labels[m.id] = f"{m.name} (Rs. {m.price:.2f})"

                    select_key = f"sel-w{selected_week}-d{day_index}-{mt}"
                    if select_key not in st.session_state:
                        default_val = "skip"
                        if mt == "breakfast":
                            dflt = get_default_meal_for(selected_week, day_index)
                            if dflt:
                                default_val = dflt.id
                        st.session_state[select_key] = default_val

                    choice = st.selectbox(
                        "",
                        option_values,
                        key=select_key,
                        format_func=lambda v, labels=labels: labels[v],
                        label_visibility="collapsed",
                    )

                    if choice == "custom":
                        price_key = f"price-w{selected_week}-d{day_index}-{mt}"
                        if price_key not in st.session_state:
                            st.session_state[price_key] = "0"
                        st.text_input("Custom price (Rs.)", key=price_key, label_visibility="collapsed")

                st.markdown("</div>", unsafe_allow_html=True)

            else:
                # Budgets card
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("<div class='budgets-title'>Budgets</div>", unsafe_allow_html=True)

                budget_labels = {
                    "weekly": "Week Total",
                    "sunday": "Sunday Total (all 4 weeks)",
                    "weekdays": "Weekdays Total (all 4 weeks)",
                    "grandTotal": "Grand Total",
                }

                for key, label in budget_labels.items():
                    left, right = st.columns([1, 3], gap="small")
                    with left:
                        if st.button("Default", key=f"reset-{key}"):
                            st.session_state[f"budget-{key}"] = f"{float(DEFAULT_BUDGETS[key]):.2f}"
                            st.rerun()
                    with right:
                        if f"budget-{key}" not in st.session_state:
                            st.session_state[f"budget-{key}"] = f"{float(DEFAULT_BUDGETS[key]):.2f}"
                        st.markdown(f"<div class='budget-label'>{label}</div>", unsafe_allow_html=True)
                        st.text_input("Budget (Rs.)", key=f"budget-{key}", label_visibility="collapsed")

                st.markdown("</div>", unsafe_allow_html=True)

        cell_index += 1

# -------------------------
# Cost summary
# -------------------------
budgets = {}
for k in DEFAULT_BUDGETS.keys():
    raw = st.session_state.get(f"budget-{k}", f"{DEFAULT_BUDGETS[k]:.2f}")
    budgets[k] = parse_float_safe(raw, DEFAULT_BUDGETS[k])

wk_cost = weekly_cost_for(selected_week)
sun_cost = sunday_total_cost_all_weeks()
wd_cost = weekdays_total_cost_all_weeks()
grand_cost = sun_cost + wd_cost

st.markdown("")
st.markdown("<div class='summary-card'>", unsafe_allow_html=True)
st.markdown("<div style='font-weight:700;margin-bottom:4px;'>Cost Summary</div>", unsafe_allow_html=True)

def summary_row(label: str, value: float, budget_key: str):
    diff_html = format_difference_html(value, budgets[budget_key])
    st.markdown(
        f"<div style='display:flex;justify-content:space-between;margin-bottom:4px;'>"
        f"<div style='color:#e5f1ff'>{label}</div>"
        f"<div style='font-weight:700;color:#c4ddff'>Rs. {value:.2f}{diff_html}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

summary_row("Current Week Total:", wk_cost, "weekly")
summary_row("Sunday Total:", sun_cost, "sunday")
st.markdown("<hr style='border-color:rgba(148,163,184,0.45);margin:6px 0;'/>", unsafe_allow_html=True)
summary_row("Weekdays Total:", wd_cost, "weekdays")
summary_row("Grand Total:", grand_cost, "grandTotal")
st.markdown("</div>", unsafe_allow_html=True)
