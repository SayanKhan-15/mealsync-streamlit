# Full app.py — Streamlit version mimicking your React UI/UX
import streamlit as st
from dataclasses import dataclass
from typing import List, Literal, Optional, Dict
from math import isfinite

# -------------------------
# Page config & CSS
# -------------------------
st.set_page_config(page_title="MealSync", layout="wide")

st.markdown(
    """
<style>
/* Background and container */
body { background: radial-gradient(circle at top, #0b1220 0, #071022 55%, #020617 100%) !important; color: #e6eef8 !important; }
section.main > div.block-container { padding-top: 0.8rem !important; padding-bottom: 1.5rem !important; }

/* Title */
.mealsync-title { font-size: 2.6rem; font-weight: 800; color: #60a5fa; text-align:center; margin-bottom: 0.2rem; }
.mealsync-subtitle { text-align:center; color:#9ca3af; margin-bottom: 1rem; }

/* Week buttons (pill) */
div.week-buttons > div.stButton > button { border-radius: 999px !important; padding: 0.36rem 1rem !important; font-size:0.85rem !important; border: 1px solid rgba(148,163,184,0.4) !important; background: rgba(14,20,30,0.6) !important; color: #e6eef8 !important; white-space: nowrap !important; }
div.week-buttons > div.stButton > button[kind="primary"] { background: linear-gradient(135deg,#2563eb,#a855f7) !important; }

/* Cards */
.card { background: rgba(12,18,30,0.95) !important; border-radius: 0.9rem !important; padding: 0.9rem !important; border: 1px solid rgba(148,163,184,0.06) !important; box-shadow: 0 14px 32px rgba(2,6,23,0.6) !important; margin-bottom: 0.8rem !important; }

/* Day header: no extra box */
.day-header { font-weight:700 !important; font-size:1.02rem !important; margin:0 0 0.45rem 0 !important; color:#cfefff !important; background:none !important; padding:0 !important; border:none !important; }

/* Sunday header color */
.day-header.sunday { color: #ff9aa2 !important; }

/* Meal card row layout */
.meal-row { display:flex; align-items:center; gap:0.6rem; margin-bottom:0.4rem; }
.meal-main { flex:1; display:flex; align-items:center; gap:0.75rem; text-align:left; }
.meal-icon { width:36px; height:36px; display:inline-flex; align-items:center; justify-content:center; border-radius:8px; background: rgba(255,255,255,0.03); font-size:18px; }
.meal-name { font-size:0.95rem; font-weight:600; color:#e6eef8; }
.meal-price { font-size:0.82rem; color:#9ca3af; }

/* small action button (repeat) */
.action-btn { border-radius:8px !important; padding:6px 8px !important; min-width:36px !important; white-space:nowrap !important; font-size:0.8rem !important; }

/* Select & inputs style */
div.stSelectbox > div > div, div.stTextInput > div > input[type="text"], div.stNumberInput > div > div {
    background-color: rgba(8,12,20,0.96) !important; border-radius:0.55rem !important; border:1px solid rgba(148,163,184,0.06) !important; color:#e6eef8 !important;
}

/* Budgets card tweaks */
.budgets-title { font-size:1.03rem; font-weight:700; margin-bottom:0.3rem; color:#e6f8ff; }
.budget-row { display:flex; gap:0.6rem; align-items:center; margin-bottom:0.5rem; }
.budget-label { font-size:0.9rem; color:#dff3ff; margin-bottom:0.18rem; }

/* ensure Default doesn't wrap */
div.stButton > button { white-space: nowrap !important; }

/* summary card */
.summary-row { display:flex; justify-content:space-between; margin-bottom:0.4rem; }
.summary-value { font-weight:700; color:#bfe6ff; }

/* small helpers */
.small-muted { color:#9ca3af; font-size:0.85rem; }
</style>
""",
    unsafe_allow_html=True,
)

# -------------------------
# Types & data
# -------------------------
MealType = Literal["breakfast", "lunch", "dinner"]

@dataclass
class Meal:
    id: str
    name: str
    price: float

# Breakfast / lunch / dinner options
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

WEEK_DAYS = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]

# -------------------------
# Helpers
# -------------------------
def get_meal_key(week:int, day:int)->str:
    return f"w{week}-d{day}"

def parse_float_safe(s: str, fallback: float = 0.0) -> float:
    try:
        f = float(s)
        if not isfinite(f):
            return fallback
        return f
    except Exception:
        return fallback

def find_by_name(options:List[Meal], name:str)->Optional[Meal]:
    for m in options:
        if m.name.lower() == name.lower():
            return m
    return None

def get_breakfast_options_for(week:int, day:int)->List[Meal]:
    specific_names = ["Medu vada","Pongal","Sambar vada","Curd vada"]
    specific = [m for m in breakfast_options if m.name in specific_names]
    # check default for the selectedWeek/day
    for d in DEFAULTS:
        if d["week"] == st.session_state.selected_week and d["day"] == day+1:
            dm = find_by_name(breakfast_options, d["meal_name"])
            if dm:
                rest = [m for m in specific if m.id != dm.id]
                return [dm] + rest
    return specific

def get_options(meal_type:MealType, day:int)->List[Meal]:
    if meal_type=="breakfast": return get_breakfast_options_for(st.session_state.selected_week, day)
    if meal_type=="lunch": return lunch_options
    return dinner_options

def get_selected_price(week:int, day:int, meal_type:MealType)->float:
    sel_key = f"sel-{week}-{day}-{meal_type}"
    choice = st.session_state.get(sel_key, "skip")
    if choice=="skip": return 0.0
    if choice=="custom":
        price_key = f"price-{week}-{day}-{meal_type}"
        return parse_float_safe(st.session_state.get(price_key,"0"), 0.0)
    # otherwise find meal price
    for m in get_options(meal_type, day):
        if m.id==choice:
            return m.price
    return 0.0

def week_weekly_cost(week:int)->float:
    tot = 0.0
    for d in range(6):
        # main meal
        main_type = st.session_state.day_meal_choices.get(get_meal_key(week,d),"breakfast")
        tot += get_selected_price(week,d,main_type)
        tot += get_selected_price(week,d,"dinner")
    return tot

def sunday_total_all_weeks()->float:
    tot=0.0
    for w in range(1,5):
        tot += get_selected_price(w,6,"lunch") + get_selected_price(w,6,"dinner")
    return tot

def weekdays_total_all_weeks()->float:
    tot = 0.0
    for w in range(1,5):
        tot += week_weekly_cost(w)
    return tot

# -------------------------
# Session state init
# -------------------------
if "selected_week" not in st.session_state:
    st.session_state.selected_week = 1
if "day_meal_choices" not in st.session_state:
    st.session_state.day_meal_choices = {}  # key -> 'breakfast'|'lunch'
# selection keys & price keys are created lazily
if "budgets" not in st.session_state:
    st.session_state.budgets = {k: f"{v:.2f}" for k,v in DEFAULT_BUDGETS.items()}

# -------------------------
# Top UI: title + week buttons
# -------------------------
st.markdown("<div class='mealsync-title'>MealSync</div>", unsafe_allow_html=True)
st.markdown("<div class='mealsync-subtitle'>Your weekly meal planning, simplified.</div>", unsafe_allow_html=True)

st.markdown("<div class='week-buttons'></div>", unsafe_allow_html=True)
wcols = st.columns(4)
for i, col in enumerate(wcols, start=1):
    with col:
        clicked = st.button(f"Week {i}", key=f"week-{i}",
                            type=("primary" if st.session_state.selected_week==i else "secondary"))
        if clicked:
            st.session_state.selected_week = i
            st.experimental_rerun()

# -------------------------
# 2x4 grid: days 0..6 then budgets card
# -------------------------
cols_per_row = 4
cell = 0
for row in range(2):
    cols = st.columns(cols_per_row, gap="small")
    for ci, col in enumerate(cols):
        with col:
            # day cards for first 7 cells
            if cell < 7:
                day_idx = cell
                is_sun = (day_idx==6)
                header_class = "day-header sunday" if is_sun else "day-header"
                st.markdown(f"<div class='{header_class}'>{WEEK_DAYS[day_idx]}</div>", unsafe_allow_html=True)
                # card wrapper
                st.markdown("<div class='card'>", unsafe_allow_html=True)

                # Toggle (mon-sat)
                if not is_sun:
                    key = get_meal_key(st.session_state.selected_week, day_idx)
                    current_choice = st.session_state.day_meal_choices.get(key, "breakfast")
                    toggle_label = f"{'☕' if current_choice=='breakfast' else '🍛'} {current_choice.capitalize()} — switch"
                    if st.button(toggle_label, key=f"tgl-{st.session_state.selected_week}-{day_idx}"):
                        st.session_state.day_meal_choices[key] = "lunch" if current_choice=="breakfast" else "breakfast"
                        st.experimental_rerun()

                # which meal types to show
                if is_sun:
                    meal_types = ["lunch","dinner"]
                else:
                    meal_types = [st.session_state.day_meal_choices.get(get_meal_key(st.session_state.selected_week, day_idx),"breakfast"), "dinner"]

                # Render each meal row
                for mt in meal_types:
                    options = get_options(mt, day_idx)
                    # header label
                    st.markdown(f"<div class='meal-row'>", unsafe_allow_html=True)
                    # main part clickable
                    col_main, col_action = st.columns([9,1], gap="small")
                    with col_main:
                        # clickable area: emulate button -> we show a select modal when clicked
                        name = None
                        price = None
                        # determine selected meal for this cell
                        sel_key = f"sel-{st.session_state.selected_week}-{day_idx}-{mt}"
                        sel_val = st.session_state.get(sel_key, "skip")
                        if sel_val == "skip":
                            name = None
                        elif sel_val == "custom":
                            price = parse_float_safe(st.session_state.get(f"price-{st.session_state.selected_week}-{day_idx}-{mt}", "0"))
                            name = "Custom Meal"
                        else:
                            found = next((m for m in options if m.id==sel_val), None)
                            if found:
                                name = found.name
                                price = found.price

                        # render main row (icon + name/price or Not planned)
                        icon = "☕" if mt=="breakfast" else ("☀️" if mt=="lunch" else "🌙")
                        display_name = name or "Not planned"
                        display_price = f"Rs. {price:.2f}" if price is not None else ""
                        html = f"""
<div class='meal-main'>
  <div class='meal-icon'>{icon}</div>
  <div style='flex:1;'>
    <div class='meal-name'>{display_name}</div>
    <div class='meal-price'>{display_price}</div>
  </div>
</div>
"""
                        # instead of a true button we render the HTML and then put a small "Change" control below to open modal
                        st.markdown(html, unsafe_allow_html=True)
                        if st.button("Change", key=f"openselect-{st.session_state.selected_week}-{day_idx}-{mt}"):
                            # open add-meal modal for this day/meal
                            st.session_state["_modal_open"] = {
                                "type": "select_meal",
                                "week": st.session_state.selected_week,
                                "day": day_idx,
                                "meal_type": mt
                            }
                            st.experimental_rerun()

                    # small repeat / toggle btn on right for non-dinner
                    with col_action:
                        if mt != "dinner":
                            if st.button("↻", key=f"rep-{st.session_state.selected_week}-{day_idx}-{mt}", help="Toggle breakfast/lunch"):
                                # toggle main meal choice for this date
                                date_key = get_meal_key(st.session_state.selected_week, day_idx)
                                current = st.session_state.day_meal_choices.get(date_key, "breakfast")
                                new = "lunch" if current=="breakfast" else "breakfast"
                                st.session_state.day_meal_choices[date_key] = new
                                # when toggling off breakfast, clear breakfast selection to avoid mismatch
                                # We simply rerun and keep data
                                st.experimental_rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

                # close card wrapper
                st.markdown("</div>", unsafe_allow_html=True)

            else:
                # Budgets card — 8th cell
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("<div class='budgets-title'>Budgets</div>", unsafe_allow_html=True)
                # each budget row: Default button (left) + label + text_input
                budget_labels = {
                    "weekly": "Week Total",
                    "sunday": "Sunday Total (all 4 weeks)",
                    "weekdays": "Weekdays Total (all 4 weeks)",
                    "grandTotal": "Grand Total"
                }
                for bkey, blabel in budget_labels.items():
                    cleft, cright = st.columns([1,4], gap="small")
                    with cleft:
                        if st.button("Default", key=f"default-{bkey}"):
                            st.session_state.budgets[bkey] = f"{DEFAULT_BUDGETS[bkey]:.2f}"
                            st.experimental_rerun()
                    with cright:
                        # ensure key exists
                        if bkey not in st.session_state.budgets:
                            st.session_state.budgets[bkey] = f"{DEFAULT_BUDGETS[bkey]:.2f}"
                        st.markdown(f"<div class='budget-label'>{blabel}</div>", unsafe_allow_html=True)
                        st.text_input("Budget (Rs.)", key=f"budget-input-{bkey}", value=st.session_state.budgets[bkey], label_visibility="collapsed", on_change=lambda bk=bkey: st.session_state.budgets.__setitem__(bk, st.session_state[f"budget-input-{bk}"]))
                st.markdown("</div>", unsafe_allow_html=True)
            cell += 1
# -------------------------
# Modals: AddMeal select modal, Custom Meal modal, Custom Budget modal
# -------------------------
def open_select_modal(state):
    week = state["week"]; day = state["day"]; mt = state["meal_type"]
    title = f"Select {mt.capitalize()}"
    options = get_options(mt, day)
    # sort by price ascending
    options_sorted = sorted(options, key=lambda x: x.price)
    with st.modal(title=title):
        st.write("Choose a meal or Skip. Select Custom to enter a manual price.")
        # build list for selectbox: ('skip','clear') etc
        labels = ["Skip meal"] + [f"{m.name} — Rs. {m.price:.2f}" for m in options_sorted] + ["Custom meal (enter price)"]
        # to keep a stable key across modals use unique key
        sel_key = f"_modal_sel_{week}_{day}_{mt}"
        if sel_key not in st.session_state:
            st.session_state[sel_key] = labels[0]
        sel = st.selectbox("Select:", labels, key=sel_key)
        col1, col2 = st.columns([1,1])
        with col1:
            if st.button("Save selection", key=f"save_sel_{week}_{day}_{mt}"):
                # interpret selection
                if sel == labels[0]:
                    # skip
                    st.session_state[f"sel-{week}-{day}-{mt}"] = "skip"
                elif sel == labels[-1]:
                    # custom: open custom input modal
                    st.session_state[f"sel-{week}-{day}-{mt}"] = "custom"
                    # ensure a price field exists
                    st.session_state[f"price-{week}-{day}-{mt}"] = st.session_state.get(f"price-{week}-{day}-{mt}", "0")
                else:
                    # find matching meal by name prefix
                    chosen_name = sel.split(" — ")[0].strip()
                    found = next((m for m in options_sorted if m.name==chosen_name), None)
                    if found:
                        st.session_state[f"sel-{week}-{day}-{mt}"] = found.id
                        # remove custom price key if existed
                        if f"price-{week}-{day}-{mt}" in st.session_state:
                            del st.session_state[f"price-{week}-{day}-{mt}"]
                # close modal state and rerun
                if "_modal_open" in st.session_state: del st.session_state["_modal_open"]
                st.experimental_rerun()
        with col2:
            if st.button("Cancel", key=f"cancel_sel_{week}_{day}_{mt}"):
                if "_modal_open" in st.session_state: del st.session_state["_modal_open"]
                st.experimental_rerun()

def open_custom_price_modal(state):
    week = state["week"]; day = state["day"]; mt = state["meal_type"]
    with st.modal("Enter custom price"):
        st.write(f"Enter manual price for {mt.capitalize()} on {WEEK_DAYS[day]} (Week {week})")
        price_key = f"price-{week}-{day}-{mt}"
        if price_key not in st.session_state:
            st.session_state[price_key] = "0"
        val = st.text_input("Price (Rs.)", key=price_key, value=st.session_state[price_key], label_visibility="collapsed")
        col1,col2 = st.columns(2)
        with col1:
            if st.button("Save", key=f"save_price_{week}_{day}_{mt}"):
                st.session_state[price_key] = val
                st.session_state[f"sel-{week}-{day}-{mt}"] = "custom"
                if "_modal_open" in st.session_state: del st.session_state["_modal_open"]
                st.experimental_rerun()
        with col2:
            if st.button("Cancel", key=f"cancel_price_{week}_{day}_{mt}"):
                if "_modal_open" in st.session_state: del st.session_state["_modal_open"]
                st.experimental_rerun()

def open_budget_modal(state):
    # not used currently, budgets are inline text inputs; kept for parity if later needed
    pass

# Handle modal open state
if "_modal_open" in st.session_state:
    modal_state = st.session_state["_modal_open"]
    # if modal type is select_meal and selection was set to "custom" previously, we should open custom price modal
    if modal_state.get("type") == "select_meal":
        # If we already set sel to custom, prefer custom modal
        week = modal_state["week"]; day = modal_state["day"]; mt = modal_state["meal_type"]
        # If modal previously had sel set to 'custom' and price entered, open price modal; else open select modal
        open_select_modal(modal_state)

# -------------------------
# After UI: show cost summary (preserve original positions)
# -------------------------
st.markdown("")  # spacer
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div style='font-weight:700; margin-bottom:0.5rem;'>Cost Summary</div>", unsafe_allow_html=True)

# parse budgets from session inputs
budgets: Dict[str,float] = {}
for k in DEFAULT_BUDGETS.keys():
    # if user changed inline text_input, its value lives at key f"budget-input-{k}"
    raw_key = f"budget-input-{k}"
    if raw_key in st.session_state:
        raw_val = st.session_state.get(raw_key, st.session_state.budgets.get(k, f"{DEFAULT_BUDGETS[k]:.2f}"))
        st.session_state.budgets[k] = raw_val  # sync
    raw = st.session_state.budgets.get(k, f"{DEFAULT_BUDGETS[k]:.2f}")
    budgets[k] = parse_float_safe(raw, DEFAULT_BUDGETS[k])

current_week_cost = week_weekly_cost(st.session_state.selected_week)
sunday_cost = sunday_total_all_weeks()
weekdays_cost = weekdays_total_all_weeks()
grand_cost = sunday_cost + weekdays_cost

def diff_html(cost, budget):
    diff = budget - cost
    if abs(diff) < 1e-9:
        return ""
    sign = "+" if diff>0 else ""
    cls = "small-muted" if diff>=0 else "small-muted"
    return f"<span style='margin-left:6px; color:{'#4ade80' if diff>0 else '#ff8b8b'}'>({sign}{diff:.2f})</span>"

st.markdown(f"<div class='summary-row'><span>Current Week Total:</span><span class='summary-value'>Rs. {current_week_cost:.2f}{diff_html(current_week_cost,budgets['weekly'])}</span></div>", unsafe_allow_html=True)
st.markdown(f"<div class='summary-row'><span>Sunday Total:</span><span class='summary-value'>Rs. {sunday_cost:.2f}{diff_html(sunday_cost,budgets['sunday'])}</span></div>", unsafe_allow_html=True)
st.markdown("<hr style='border-color: rgba(148,163,184,0.06)'/>", unsafe_allow_html=True)
st.markdown(f"<div class='summary-row'><span>Weekdays Total:</span><span class='summary-value'>Rs. {weekdays_cost:.2f}{diff_html(weekdays_cost,budgets['weekdays'])}</span></div>", unsafe_allow_html=True)
st.markdown(f"<div class='summary-row'><span>Grand Total:</span><span class='summary-value'>Rs. {grand_cost:.2f}{diff_html(grand_cost,budgets['grandTotal'])}</span></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
