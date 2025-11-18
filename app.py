import streamlit as st
from dataclasses import dataclass
from typing import List, Dict, Literal, Optional

# ---------- Data models ----------

MealType = Literal["breakfast", "lunch", "dinner"]

@dataclass
class Meal:
    id: str
    name: str
    price: float


# ---------- Static meal data (adapt these to match your Firebase/TS data) ----------

# These are based on the names in your React code.
# Change prices or add/remove items as you like.
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

# Placeholder lunch/dinner options – replace with your real data
lunch_options: List[Meal] = [
    Meal("mess-lunch", "Mess Lunch", 60.0),
    Meal("special-lunch", "Special Lunch", 80.0),
]

dinner_options: List[Meal] = [
    Meal("mess-dinner", "Mess Dinner", 60.0),
    Meal("special-dinner", "Special Dinner", 80.0),
]


# Defaults from your React code
DEFAULTS = [
    {"week": 1, "day": 2, "meal_name": "Pav bhaji"},
    {"week": 3, "day": 3, "meal_name": "Pav bhaji"},
    {"week": 1, "day": 4, "meal_name": "Maggi"},        # Make sure Maggi exists if you want it
    {"week": 1, "day": 6, "meal_name": "Alu paratha"},
    {"week": 4, "day": 4, "meal_name": "Alu paratha"},
    {"week": 2, "day": 4, "meal_name": "Macaroni"},
    {"week": 2, "day": 5, "meal_name": "Macaroni"},
    {"week": 4, "day": 6, "meal_name": "Daal poori"},
]

# You can add Maggi to breakfast_options if you actually use it:
# breakfast_options.append(Meal("maggi", "Maggi", 30.0))


# ---------- Budget defaults ----------

DEFAULT_BUDGETS = {
    "weekly": 840.0,
    "sunday": 2140.0,
    "weekdays": 3360.0,
    "grandTotal": 5500.0,
}


# ---------- Helpers ----------

WEEK_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def get_meal_key(week: int, day_index: int) -> str:
    return f"w{week}-d{day_index}"


def find_breakfast_by_name(name: str) -> Optional[Meal]:
    for m in breakfast_options:
        if m.name.lower() == name.lower():
            return m
    return None


def get_default_meal_for(week: int, day_index: int) -> Optional[Meal]:
    day_of_week = day_index + 1  # your TS used 1–7 for day
    for item in DEFAULTS:
        if item["week"] == week and item["day"] == day_of_week:
            return find_breakfast_by_name(item["meal_name"])
    return None


def get_breakfast_options_for(week: int, day_index: int) -> List[Meal]:
    # In your React code, specificOptions were 4 items.
    specific_names = {"Medu vada", "Pongal", "Sambar vada", "Curd vada"}
    specific = [m for m in breakfast_options if m.name in specific_names]

    default_meal = get_default_meal_for(week, day_index)
    if default_meal and default_meal in breakfast_options:
        # Put default meal first, then the specific options without duplicating
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
    """Breakfast/lunch toggle for Mon–Sat; Sunday is always lunch."""
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
    # regular meal ID
    meals = get_options_for_meal_type(meal_type, week, day_index)
    for m in meals:
        if m.id == choice:
            return m.price
    return 0.0


def weekly_cost_for(week: int) -> float:
    total = 0.0
    # Mon–Sat
    for day_index in range(6):
        main_type = get_main_meal_type(week, day_index)
        total += get_meal_price(week, day_index, main_type)
        total += get_meal_price(week, day_index, "dinner")
    return total


def sunday_cost_for(week: int) -> float:
    # Sunday = day_index 6, lunch + dinner
    return (
        get_meal_price(week, 6, "lunch")
        + get_meal_price(week, 6, "dinner")
    )


def format_difference(cost: float, budget: float) -> str:
    diff = budget - cost
    if abs(diff) < 1e-9:
        return ""
    sign = "+" if diff > 0 else ""
    word = "under" if diff > 0 else "over"
    return f" ({sign}{diff:.2f} {word} budget)"


# ---------- Session state init ----------

if "selected_week" not in st.session_state:
    st.session_state.selected_week = 1

if "day_meal_choices" not in st.session_state:
    # key: "w{week}-d{day}" -> "breakfast" | "lunch"
    st.session_state.day_meal_choices = {}

if "budgets_initialized" not in st.session_state:
    for k, v in DEFAULT_BUDGETS.items():
        st.session_state[f"budget-{k}"] = float(v)
    st.session_state.budgets_initialized = True


# ---------- UI ----------

st.set_page_config(page_title="MealSync", layout="wide")

st.markdown(
    "<h1 style='text-align:center;'>MealSync</h1>",
    unsafe_allow_html=True,
)
st.write(
    "<p style='text-align:center;'>Your weekly meal planning, simplified (Streamlit).</p>",
    unsafe_allow_html=True,
)

# Week selector
st.markdown("### Select week")
week_cols = st.columns(4)
for i, col in enumerate(week_cols, start=1):
    with col:
        if st.button(
            f"Week {i}",
            type="primary" if st.session_state.selected_week == i else "secondary",
            key=f"week-btn-{i}",
        ):
            st.session_state.selected_week = i

selected_week = st.session_state.selected_week

st.markdown("---")

# Grid of days for selected week
st.markdown(f"## Week {selected_week} plan")

day_cols = st.columns(4)

for idx, day_index in enumerate(range(7)):
    col = day_cols[idx % 4]
    with col:
        st.markdown(f"**{WEEK_DAYS[day_index]}**")
        is_sunday = day_index == 6

        if not is_sunday:
            key = get_meal_key(selected_week, day_index)
            current_choice: MealType = st.session_state.day_meal_choices.get(
                key, "breakfast"
            )
            toggle_label = (
                "Showing: Breakfast (click to switch to Lunch)"
                if current_choice == "breakfast"
                else "Showing: Lunch (click to switch to Breakfast)"
            )
            if st.button(
                toggle_label,
                key=f"toggle-{selected_week}-{day_index}",
                help="Toggle between breakfast/lunch as main meal",
            ):
                new_choice = "lunch" if current_choice == "breakfast" else "breakfast"
                st.session_state.day_meal_choices[key] = new_choice
                st.experimental_rerun()

        # Which meal types do we show?
        if is_sunday:
            main_meal_types: List[MealType] = ["lunch", "dinner"]
        else:
            main_meal_types = [get_main_meal_type(selected_week, day_index), "dinner"]

        for meal_type in main_meal_types:
            pretty = meal_type.capitalize()

            st.write(f"{pretty}:")

            options_meals = get_options_for_meal_type(
                meal_type, selected_week, day_index
            )

            # "skip" + real options + "custom"
            option_values = ["skip"] + [m.id for m in options_meals] + ["custom"]

            labels = {"skip": "Skip this meal", "custom": "Custom meal (enter price)"}
            for m in options_meals:
                labels[m.id] = f"{m.name} (Rs. {m.price:.2f})"

            select_key = f"sel-w{selected_week}-d{day_index}-{meal_type}"

            # Initial default selection – if breakfast and we have a default, use that;
            # otherwise skip.
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
                )

        st.markdown("---")

# ---------- Budgets card ----------

st.markdown("## Budgets")

budget_labels = {
    "weekly": "Current Week Total budget",
    "sunday": "Sunday Total budget (all 4 weeks)",
    "weekdays": "Weekdays Total budget (all 4 weeks)",
    "grandTotal": "Grand Total budget",
}

for key, label in budget_labels.items():
    cols = st.columns([2, 2, 1])
    with cols[0]:
        st.write(label)
    with cols[1]:
        st.number_input(
            "Budget (Rs.)",
            min_value=0.0,
            step=10.0,
            key=f"budget-{key}",
            label_visibility="collapsed",
        )
    with cols[2]:
        if st.button("Default", key=f"reset-{key}"):
            st.session_state[f"budget-{key}"] = DEFAULT_BUDGETS[key]
            st.experimental_rerun()

budgets = {
    k: float(st.session_state[f"budget-{k}"])
    for k in DEFAULT_BUDGETS.keys()
}


# ---------- Cost summary ----------

st.markdown("## Cost summary")

weekly_cost = weekly_cost_for(selected_week)

sunday_total = sum(sunday_cost_for(week) for week in range(1, 5))
weekdays_total = sum(weekly_cost_for(week) for week in range(1, 5))
grand_total = sunday_total + weekdays_total

st.write(
    f"**Current Week Total:** Rs. {weekly_cost:.2f}"
    f"{format_difference(weekly_cost, budgets['weekly'])}"
)
st.write(
    f"**Sunday Total (all weeks):** Rs. {sunday_total:.2f}"
    f"{format_difference(sunday_total, budgets['sunday'])}"
)
st.write(
    f"**Weekdays Total (all weeks):** Rs. {weekdays_total:.2f}"
    f"{format_difference(weekdays_total, budgets['weekdays'])}"
)
st.write(
    f"**Grand Total:** Rs. {grand_total:.2f}"
    f"{format_difference(grand_total, budgets['grandTotal'])}"
)
