# Spend Tracker — a 30 minute Streamlit lab

Build a working expense tracker in six steps. It uses every command from the
demo — widgets, forms, session state, dataframes, charts — and it only works if
you understand the re-run loop.

```
streamlit run lab/lab_starter.py
```

| File | | |
|---|---|---|
| `lab/lab_starter.py` | what you edit | tasks are numbered `TODO` blocks, in file order |
| `lab/lab_solution.py` | the worked answer | open it if you get stuck, not before |
| `lab/sample_expenses.csv` | five rows | for the CSV stretch task |

**Time budget** — Setup 2 · Step 1 4 · Step 2 2 · Step 3 6 · Step 4 5 · Step 5 6 · Step 6 5 = **30 min**

---

## The rule the whole lab tests

Touch any widget and Streamlit re-runs the **entire file from line 1**. Ordinary
variables are wiped every time. Only `st.session_state` survives.

> you click → whole script re-runs → page redraws → widgets remember their own values

The starter file prints a run counter at the bottom of the page. Watch it while
you work — it is the lab's heartbeat monitor.

**How the TODOs work.** Each step gives you the code with the interesting parts
blanked out as `___`. Uncomment the block and replace every `___` with your own
value. Nothing is a trick question: the blanks are labels, keys and column
names. The structure is already there.

---

## Setup

Run the command above. A browser tab opens at `localhost:8501`.

- Streamlit shows a **Rerun** button top-right whenever you save. Click
  **Always rerun** once so the page refreshes itself from now on.
- Open `lab/lab_starter.py` and search for `TODO`.

> **Check** — the page loads with a divider and a run counter, and nothing else.
> Never run it with `python lab_starter.py`; that prints a warning and draws
> nothing. The command is always `streamlit run <file>.py`.

---

## Step 1 — Page setup and sidebar

A heading for the page, and a greeting in the sidebar. Anything drawn with
`st.sidebar.*` lands in the left panel.

```python
st.title(___)                       # e.g. "Spend Tracker"
st.caption(___)                     # one small grey line under the title

name = st.sidebar.text_input(___)   # the label shown above the box

# text_input returns "" until the user types, so only greet once it isn't:
if ___:
    st.sidebar.write(f"Hi {___}, here is where your money went.")
```

> **Check** — type your name in the sidebar. The greeting appears as you type,
> and the run counter climbs with every keystroke. That is the whole script
> re-running each time.

---

## Step 2 — Somewhere to remember

`st.session_state` is the only thing that survives a re-run. Initialise it once,
guarded by an `if ... not in ...` check — otherwise you wipe it on every re-run.

This has to sit **above** the form. The script runs top to bottom, so nothing
can use a value created below it.

```python
if "expenses" not in ___:
    ___["expenses"] = []
```

Each item you store later will be a dict shaped like:

```python
{"Description": "Coffee", "Amount": 4.5, "Category": "Food"}
```

> **Check** — nothing new appears on the page. Correct. To see it, drop in
> `st.write(st.session_state)` for a moment, then delete it.

---

## Step 3 — The input form

A form batches widgets: nothing re-runs while you fill it in, and everything
submits at once. Every form needs exactly **one** `st.form_submit_button()`, and
that button returns the `True`/`False` you branch on.

```python
st.header(___)                                  # e.g. "Add an expense"

with st.form("add_expense", clear_on_submit=True):
    description = st.text_input(___)            # "What did you buy?"
    amount      = st.number_input(___, min_value=0.0, step=0.5, format="%.2f")
    category    = st.selectbox(___, CATEGORIES) # label, then the options
    submitted   = st.form_submit_button(___)    # "Add expense"
```

Note the argument order every widget shares: **label first, options second.**

> **Check** — type in the form and the run counter *stays put*. Click Add
> expense and it jumps. That is exactly what a form is for: it batches the
> widgets and re-runs once.

---

## Step 4 — Save the submission

`submitted` is `True` on exactly the one re-run that follows the click.

```python
if submitted:
    if not description:
        st.error(___)                   # "Description is required."
    elif amount == 0:
        st.warning(___)                 # "Amount must be above 0."
    else:
        st.session_state.expenses.append(
            {"Description": ___, "Amount": ___, "Category": ___}
        )
        st.success(___)                 # f"Added {description}"
```

Appending to the list is all you have to do. The script is about to re-run
anyway, and Step 5 draws the new row.

> **Check** — submitting empty gives a red error. Adding "Coffee, 4.50, Food"
> gives a green success and the form clears itself.

---

## Step 5 — Show the data

```python
st.header(___)                          # e.g. "Your spending"

if not st.session_state.expenses:
    st.info(___)                        # "No expenses yet - add one above."
else:
    # a list of dicts becomes a DataFrame in one line
    df = pd.DataFrame(___)

    # two numbers side by side: st.columns gives you containers to draw in
    left, right = st.columns(2)
    left.metric("Total spent", f"${___:.2f}")   # hint: df["Amount"].sum()
    right.metric("Entries", ___)                # hint: how many rows?

    st.dataframe(df)

    # a chart shows one bar per ROW unless you aggregate first
    by_category = df.groupby(___)[___].sum()
    st.bar_chart(___)
```

An empty state is half of a good app — without it the page looks broken on
first load.

> **Check** — add three expenses in two categories. Table, both metrics and a
> two-bar chart all update on every submit.

---

## Step 6 — Filter and reset

**6a — the filter.** Write it *inside* the `else:` from Step 5, immediately after
`df = pd.DataFrame(...)` and **before** anything is drawn from `df`.

```python
chosen = st.sidebar.multiselect(___, CATEGORIES, default=___)
df = df[df["Category"].isin(___)]
```

**6b — the reset button.** This one goes at the top level of the file, above
Step 5, so it can empty the list before the table is drawn.

```python
if st.sidebar.button(___):              # "Clear all"
    st.session_state.expenses = []
    st.rerun()
```

`st.rerun()` restarts the script immediately, so the page redraws empty instead
of showing the old table for one more frame.

> **Check** — untick a category: those rows vanish, the total drops, the chart
> loses a bar. Clear all takes you back to the empty state.

---

## What will bite you

**1. No guard on the session state init**

```python
st.session_state.expenses = []   # no guard
```

Your list empties itself every time you click anything. Without the
`if "expenses" not in st.session_state` check, that line runs on every re-run
and throws the list away. This is the number one Streamlit bug.

**2. Charting the raw frame**

```python
st.bar_chart(df)
```

You get a bar per row, not a bar per category. Charts plot the DataFrame you
hand them, indexed as-is. Aggregate with `groupby` first, then chart the result.

**3. Filtering below the table**

```python
df = df[df["Category"].isin(chosen)]   # written below st.dataframe(df)
```

The filter appears to do nothing. Top to bottom, always — the table was already
drawn with the unfiltered frame, so reassigning `df` afterwards changes nothing
on screen.

**4. The wrong command**

```
python lab_starter.py
```

A warning prints and no page opens. Streamlit runs its own web server, so the
command is always `streamlit run <file>.py`.

---

## Finished early?

**A. Import a CSV.** `st.file_uploader` returns `None` until a file is picked,
so guard it. There is a ready-made `lab/sample_expenses.csv` next door.

```python
uploaded = st.file_uploader(___, type="csv")
if uploaded is not None:
    incoming = pd.read_csv(uploaded)
    st.dataframe(incoming)
    if st.button("Add these rows"):
        st.session_state.expenses.extend(incoming.to_dict("records"))
        st.rerun()
```

**B. Split the views.** `table_tab, chart_tab = st.tabs(["Table", "Chart"])`

**C. Let them take it home.**
`st.download_button("Download CSV", df.to_csv(index=False), "spend.csv")`

**D. Make it multipage.** Wrap the app in a function and add a sidebar radio,
the way the demo file does.

---

## Instructor notes

**Running the room**

- Do the setup step together, on screen. The run counter at the bottom of the
  file is the most useful thing in it — point at it before anyone writes a line.
- Steps 1–2 and 3–4 pair naturally. Call a 30-second regroup before **Step 4**
  and before **Step 6**; anyone behind can paste the matching block from
  `lab_solution.py` and keep moving.
- The Step 3 checkpoint is the one to demo live: typing inside a form does not
  re-run, submitting does. It lands better shown than described.

**Debrief questions — 5 minutes if you have them**

1. The run counter climbs on every keystroke, so why doesn't your expense list
   reset with it?
2. What breaks if you move the `session_state` initialisation below the form?
3. Why does the multiselect have to be written above the table when it appears
   beside it on screen?
4. You clicked Clear all and the old table flashed for a moment. Which line
   fixes that?

Every answer is the same sentence: the script runs top to bottom, start to
finish, on every interaction.
