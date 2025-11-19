import streamlit as st
from dataclasses import dataclass
from typing import List, Literal, Optional

# -------------------------
# Page config & minimal rectangular frames UI
# -------------------------
st.set_page_config(page_title="MealSync", layout="wide")

st.markdown(
    """
<style>
/* Page background */
body {
  background: linear-gradient(180deg, #061025 0%, #020617 100%);
  color: #e6eef8;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
}

/* reduce top/bottom container padding */
section.main > div.block-container {
  padding-top: 0.5rem;
  padding-bottom: 0.8rem;
}

/* Title */
.app-title {
  font-size: 2.2rem;
  font-weight: 800;
  color: #7dd3fc;
  text-align: center;
  margin-bottom: 0.12rem;
}
.app-sub {
  text-align: center;
  color: #9fb6c9;
  margin-bottom: 0.6rem;
}

/* Week buttons row */
div.week-buttons > div.stButton > button {
  border-radius: 999px !important;
  padding: 6px 10px !important;
  font-size: 0.85rem !important;
  background: rgba(255,255,255,0.03) !important;
  color: #e6eef8 !important;
  border: 1px solid rgba(255,255,255,0.04) !important;
  white-space: nowrap !important;
}
div.week-buttons > div.stButton > button[kind="primary"]{
  background: linear-gradient(135deg,#2563eb,#7c3aed) !important;
  color: #fff !important;
  border: none !important;
}

/* Generic button look (Default etc) - keep single line */
div.stButton > button {
  white-space: nowrap;
  min-width: 72px;
  border-radius: 8px;
  padding: 6px 10px;
  background-color: rgba(255,255,255,0.03);
  color: #e6eef8;
  border: 1px solid rgba(255,255,255,0.04);
  font-size: 0.82rem;
}

/* RECTANGULAR CARD framed style */
.card {
  background: rgba(8,12,20,0.75);
  border-radius: 6px;
  border: 1px solid rgba(125, 211, 252, 0.10); /* soft frame */
  padding: 10px 10px;      /* small padding */
  margin: 4px 0;           /* minimal vertical spacing */
  box-shadow: none;
}

/* Narrower top gap: prevent Streamlit markdown from adding spacing above first element */
.card > .stMarkdown, .card > .stTextInput, .card > .stSelectbox, .card > .stButton {
  margin-top: 0 !important;
  margin-bottom: 6px !important;
}

/* Day header inside card (no extra box above it) */
.day-header {
  font-weight: 700;
  font-size: 1.0rem;
  margin: 0 0 6px 0;
  color: #e6f7ff;
}

/* Sunday tint */
.day-header.sunday { color: #ffd6d8; }

/* Meal label small */
.meal-label {
  font-size: 0.72rem;
  color: #9fb6c9;
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Selectbox styling compact */
div.stSelectbox > div > div {
  border-radius: 6px;
  background-color: rgba(10,14,20,0.98);
  border: 1px solid rgba(255,255,255,0.04);
  color: #e6eef8;
  padding: 6px;
}

/* Text input styling (custom prices + budgets) - plain text */
div.stTextInput > div > input[type="text"] {
  background-color: rgba(10,14,20,0.98);
  border-radius: 6px;
  border: 1px solid rgba(255,255,255,0.04);
  color: #e6eef8;
  padding: 6px 8px;
}

/* Budgets header flush */
.budgets-title {
  font-weight: 700;
  color: #e6f7ff;
  margin: 0 0 6px 0;
}

/* Budget label */
.budget-label { color: #cfefff; margin-bottom: 4px; font-size: 0.86rem; }

/* Summary small frame */
.summary-frame {
  background: rgba(8,12,20,0.8);
  border-radius: 6px;
  border: 1px solid rgba(255,255,255,0.04);
  padding: 10px;
  margin-top: 8px;
}

/* diffs */
.diff-pos { color: #4ade80; font-weight: 600; }
.diff-neg { color: #fb7185; font-weight: 600; }

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

# breakfast/lunch/dinner options
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
# Helpers (same logic)
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
    cls = "diff-pos" if diff > 0 else "diff-neg"
    return f" <span class='{cls}'>({sign}{diff:.2f})</span>"

# -------------------------
# Session state defaults
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
# Top UI: title & weeks
# -------------------------
st.markdown("<div class='app-title'>MealSync</div>", unsafe_allow_html=True)
st.markdown("<div class='app-sub'>Your weekly meal planning, simplified.</div>", unsafe_allow_html=True)

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
# 2x4 grid: 7 day framed cards, 8th budgets framed card
# -------------------------
rows = 2
cols_per_row = 4
cell = 0

for r in range(rows):
    cols = st.columns(cols_per_row, gap="small")
    for col in cols:
        with col:
            if cell < 7:
                day_index = cell
                is_sunday = (day_index == 6)

                # one framed card per day
                st.markdown("<div class='card'>", unsafe_allow_html=True)

                # header inside card (no extra empty stripe)
                hdr_cls = "day-header sunday" if is_sunday else "day-header"
                st.markdown(f"<div class='{hdr_cls}'>{WEEK_DAYS[day_index]}</div>", unsafe_allow_html=True)

                # toggle (Mon-Sat)
                if not is_sunday:
                    key = get_meal_key(selected_week, day_index)
                    cur = st.session_state.day_meal_choices.get(key, "breakfast")
                    icon = "☕" if cur == "breakfast" else "🍛"
                    label = f"{icon} {cur.capitalize()} — click to switch"
                    if st.button(label, key=f"toggle-{selected_week}-{day_index}"):
                        st.session_state.day_meal_choices[key] = "lunch" if cur == "breakfast" else "breakfast"
                        st.rerun()

                # show meal selects
                if is_sunday:
                    mtypes = ["lunch", "dinner"]
                else:
                    mtypes = [get_main_meal_type(selected_week, day_index), "dinner"]

                for mt in mtypes:
                    pretty = mt.capitalize()
                    icon = "☕" if mt == "breakfast" else ("☀️" if mt == "lunch" else "🌙")
                    st.markdown(f"<div class='meal-label'>{icon} {pretty}</div>", unsafe_allow_html=True)

                    opts = get_options_for_meal_type(mt, selected_week, day_index)
                    values = ["skip"] + [m.id for m in opts] + ["custom"]
                    labels = {"skip": "Skip this meal", "custom": "Custom price (type Rs.)"}
                    for m in opts:
                        labels[m.id] = f"{m.name} (Rs. {m.price:.2f})"

                    sel_key = f"sel-w{selected_week}-d{day_index}-{mt}"
                    if sel_key not in st.session_state:
                        dv = "skip"
                        if mt == "breakfast":
                            df = get_default_meal_for(selected_week, day_index)
                            if df:
                                dv = df.id
                        st.session_state[sel_key] = dv

                    choice = st.selectbox(
                        "",
                        values,
                        key=sel_key,
                        format_func=lambda v, labels=labels: labels[v],
                        label_visibility="collapsed",
                    )

                    if choice == "custom":
                        price_key = f"price-w{selected_week}-d{day_index}-{mt}"
                        if price_key not in st.session_state:
                            st.session_state[price_key] = "0"
                        st.text_input("Custom price (Rs.)", key=price_key, label_visibility="collapsed")

                st.markdown("</div>", unsafe_allow_html=True)  # close card

            else:
                # budgets framed card
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

        cell += 1

# -------------------------
# Cost summary below grid
# -------------------------
budgets = {}
for k in DEFAULT_BUDGETS.keys():
    raw = st.session_state.get(f"budget-{k}", f"{DEFAULT_BUDGETS[k]:.2f}")
    budgets[k] = parse_float_safe(raw, DEFAULT_BUDGETS[k])

wk_cost = weekly_cost_for(selected_week)
sun_cost = sunday_total_cost_all_weeks()
wd_cost = weekdays_total_cost_all_weeks()
grand_cost = sun_cost + wd_cost

st.markdown("")  # spacing
st.markdown("<div class='summary-frame'>", unsafe_allow_html=True)
st.markdown("<div style='font-weight:700;margin-bottom:6px;color:#e6f7ff'>Cost Summary</div>", unsafe_allow_html=True)

def summary_row(label: str, value: float, budget_key: str):
    diff_html = format_difference_html(value, budgets[budget_key])
    st.markdown(
        f"<div style='display:flex;justify-content:space-between;margin-bottom:6px;'>"
        f"<div style='color:#dff6ff'>{label}</div>"
        f"<div style='font-weight:700;color:#bfe6ff'>Rs. {value:.2f}{diff_html}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

summary_row("Current Week Total:", wk_cost, "weekly")
summary_row("Sunday Total:", sun_cost, "sunday")
st.markdown("<hr style='border-color:rgba(255,255,255,0.03);margin:6px 0;'/>", unsafe_allow_html=True)
summary_row("Weekdays Total:", wd_cost, "weekdays")
summary_row("Grand Total:", grand_cost, "grandTotal")
st.markdown("</div>", unsafe_allow_html=True)
