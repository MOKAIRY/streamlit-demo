"""
===============================================================================
 STREAMLIT LAB - "Spend Tracker"                                  ~30 minutes
===============================================================================
 You will build a small expense tracker that uses every idea from the demo:

   Step 1  Page setup + sidebar     st.set_page_config, st.title, st.sidebar
   Step 2  Somewhere to remember    st.session_state
   Step 3  Collect input in a form  st.form, text_input, number_input, selectbox
   Step 4  Save the submission      st.session_state, st.error / warning / success
   Step 5  Show the data            st.dataframe, st.metric, st.bar_chart
   Step 6  Filter and reset         st.multiselect, st.button, st.rerun

 The steps are in the order they appear in this file, and that order matters -
 the script runs top to bottom, so nothing can use a value that has not been
 created above it yet.

-------------------------------------------------------------------------------
 HOW TO RUN
-------------------------------------------------------------------------------
     streamlit run lab/lab_starter.py

 Leave the server running for the whole lab. Each time you save this file
 Streamlit shows a "Rerun" button top-right - click "Always rerun" once and the
 page refreshes itself every time you hit save.

-------------------------------------------------------------------------------
 HOW THE TODOs WORK
-------------------------------------------------------------------------------
 Each step gives you the code with the interesting parts blanked out as ___
 Uncomment the block and replace every ___ with your own value.

 Nothing is a trick question: the blanks are labels, keys and column names.
 The structure is already there.

-------------------------------------------------------------------------------
 THE RULE THAT EXPLAINS EVERYTHING
-------------------------------------------------------------------------------
 Touch a widget -> Streamlit re-runs this ENTIRE file from line 1.
 Ordinary variables are wiped. Only st.session_state survives.

 Scroll to the bottom of the running app: there is a counter proving it.
===============================================================================
"""

import streamlit as st
import pandas as pd

# The categories every expense must belong to. Used by Steps 3, 5 and 6.
CATEGORIES = ["Food", "Transport", "Rent", "Fun", "Other"]


# =============================================================================
# STEP 1 - PAGE SETUP
# =============================================================================
# set_page_config must be the FIRST Streamlit command in the script, and may be
# called only once per run. It is already done for you:
st.set_page_config(page_title="Spend Tracker", page_icon=":money_with_wings:")

# TODO 1 - a heading for the page, and a greeting in the sidebar.
#          Anything drawn with st.sidebar.* lands in the left panel.
#
st.title("Spend Tracker")                       # e.g. "Spend Tracker"
st.caption("Track your expenses easily")     # one small grey line under the title
#
name = st.sidebar.text_input("What is your name?")   # the label shown above the box
#
# text_input returns "" until the user types, so only greet once it isn't:
if name:
    st.sidebar.write(f"Hi {name}, here is where your money went.")


# =============================================================================
# STEP 2 - SOMEWHERE TO REMEMBER
# =============================================================================
# st.session_state is the only thing that survives a re-run. Initialise it once,
# guarded by an `if ... not in ...` check, otherwise you would wipe it on every
# single re-run.
#
# This has to sit ABOVE the form - the form in Step 3 needs somewhere to put
# its results, and the script runs top to bottom.
#
# TODO 2 - create the empty list, once.
#
if "expenses" not in st.session_state:
    st.session_state["expenses"] = []
#
# Each item you store later will be a dict shaped like:
#     {"Description": "Coffee", "Amount": 4.5, "Category": "Food"}


# =============================================================================
# STEP 3 - THE INPUT FORM
# =============================================================================
# A form batches widgets: nothing re-runs while the user is filling it in, and
# everything is submitted at once. Every form needs exactly ONE
# st.form_submit_button(), and that button returns the True/False you branch on.
#
# TODO 3 - build the form.
#
st.header("Add an expense")

with st.form("add_expense", clear_on_submit=True):
    description = st.text_input("What did you buy?")            # "What did you buy?"
    amount      = st.number_input("Amount", min_value=0.0, step=0.5, format="%.2f")
    category    = st.selectbox("Category", CATEGORIES) # label, then the options
    submitted   = st.form_submit_button("Add expense")

# Note the argument order every widget shares: LABEL first, options second.


# =============================================================================
# STEP 4 - SAVE THE SUBMISSION
# =============================================================================
# `submitted` is True on exactly the one re-run that follows the click.
#
# TODO 4 - validate, then store.
#
if submitted:
    if not description:
        st.error("Description is required.")
    elif amount == 0:
        st.warning("Amount must be above 0.")
    else:
        st.session_state.expenses.append(
            {"Description": description, "Amount": amount, "Category": category}
        )
        st.success(f"Added {description}")
#
# Appending to the list is all you have to do. The script is about to re-run
# anyway, and Step 5 draws the new row.


# =============================================================================
# STEP 5 - SHOW THE DATA
# =============================================================================
# TODO 5 - the empty state, the table, the numbers and the chart.
#
st.header("Your spending")                          # e.g. "Your spending"

if not st.session_state.expenses:
    st.info("No expenses yet - add one above.")                        # "No expenses yet - add one above."
else:
    # a list of dicts becomes a DataFrame in one line
    df = pd.DataFrame(st.session_state.expenses)

    chosen = st.sidebar.multiselect("Filter by category", CATEGORIES, default=CATEGORIES)
    df = df[df["Category"].isin(chosen)]

    # two numbers side by side: st.columns gives you containers to draw in
    left, right = st.columns(2)
    left.metric("Total spent", f"${df['Amount'].sum():.2f}")   # hint: df["Amount"].sum()
    right.metric("Entries", len(df))                # hint: how many rows?

    st.dataframe(df)

    # a chart shows one bar per ROW unless you aggregate first
    by_category = df.groupby("Category")["Amount"].sum()
    st.bar_chart(by_category)

# An empty state is half of a good app - without it the page looks broken on
# first load.


# =============================================================================
# STEP 6 - FILTER AND RESET
# =============================================================================
# TODO 6a - the filter. Write it INSIDE the `else:` from Step 5, immediately
#           after `df = pd.DataFrame(...)` and BEFORE anything is drawn from df.
#
#
# TODO 6b - the reset button. This one goes at the TOP LEVEL of the file, above
#           Step 5, so it can empty the list before the table is drawn.
#
if st.sidebar.button("Clear all"):              # "Clear all"
    st.session_state.expenses = []
    st.rerun()
#
# st.rerun() restarts the script immediately, so the page redraws empty instead
# of showing the old table for one more frame.


# =============================================================================
# STRETCH - only if you finish early
# =============================================================================
# A. Import a CSV. It returns None until a file is picked, so guard it.
#    There is a ready-made file next door: lab/sample_expenses.csv
#
uploaded = st.file_uploader("Upload CSV", type="csv")
if uploaded is not None:
    incoming = pd.read_csv(uploaded)
    st.dataframe(incoming)
    if st.button("Add these rows"):
        st.session_state.expenses.extend(incoming.to_dict("records"))
        st.rerun()
#
# B. Split the two views:  table_tab, chart_tab = st.tabs(["Table", "Chart"])
# C. st.download_button("Download CSV", df.to_csv(index=False), "spend.csv")
# D. Wrap the app in a function and add a second page with a sidebar radio, the
#    way the demo file does it.


# =============================================================================
# PROOF THE SCRIPT RE-RUNS  -  leave this at the bottom
# =============================================================================
st.divider()
if "run_count" not in st.session_state:
    st.session_state.run_count = 0
st.session_state.run_count += 1
st.caption(
    f"This file has run {st.session_state.run_count} time(s) since the page "
    "loaded. Touch any widget and watch that number climb."
)
