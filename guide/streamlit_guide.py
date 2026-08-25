"""
===============================================================================
 STREAMLIT TEACHING Guide

 A single runnable file covering the four sections of the course guide:

   1. Streamlit Hello World
   2. Core Streamlit Components   (inputs + selection widgets)
   3. Displaying Data             (text, data structures, file uploader)
   4. Creating Interactive Apps   (session state, forms)

-------------------------------------------------------------------------------
 HOW TO RUN
-------------------------------------------------------------------------------
     pip install streamlit
     streamlit run streamlit_guide.py

 A browser tab opens at http://localhost:8501.
 Press Ctrl+C in the terminal to stop the server.

 IMPORTANT: never run this with `python streamlit_guide.py`. Streamlit runs its
 own web server, so the command is ALWAYS `streamlit run <file>.py`.
 (Running it with plain python prints a warning and draws nothing.)

-------------------------------------------------------------------------------
 THE ONE BIG IDEA - say this out loud to the class before anything else
-------------------------------------------------------------------------------
 A Streamlit app is an ordinary Python script that runs TOP TO BOTTOM.
 Every time the user touches any widget - clicks a button, drags a slider,
 types a character - Streamlit RE-RUNS THE WHOLE SCRIPT from line 1 and
 redraws the page. Widgets remember their own values across that re-run, so
 the page looks stable even though the code just ran again.

 That single rule explains nearly every "weird" Streamlit behaviour:
   - a normal variable resets           -> because the script restarted
   - st.session_state exists            -> to survive the restart
   - the page order == the code order   -> it draws as it executes
   - `if st.button(...)` is True once   -> only on the run caused by the click

-------------------------------------------------------------------------------
 A NOTE ON `with st.echo():`
-------------------------------------------------------------------------------
 Many guides below are wrapped in `with st.echo():`. That is a teaching helper:
 it RUNS the code inside the block AND prints that same code onto the page,
 so students see the source and its result together. You do not need it in a
 real app - it is here so the app itself is the slide deck.
===============================================================================
"""

# -----------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------
# `import streamlit as st` is the universal convention: every tutorial, every
# doc page and every Stack Overflow answer uses the name `st`.
import streamlit as st

# pandas ships as a Streamlit dependency, so it is always available.
# We use it in section 3 for tables / dataframes.
import pandas as pd

# Used by the time-range slider in section 2.
from datetime import time


# -----------------------------------------------------------------------------
# PAGE CONFIG  -  optional, but it must come first
# -----------------------------------------------------------------------------
# st.set_page_config() controls the browser tab title, the favicon, the page
# width and the sidebar's starting state.
#
# TWO RULES (both are classic beginner errors):
#   1. It must be the FIRST Streamlit command executed in the script.
#   2. It may be called only ONCE per run.
#
#   layout="centered" (default) -> narrow, readable column
#   layout="wide"               -> use the full browser width
st.set_page_config(
    page_title="Streamlit Guide - Teaching File",
    page_icon="🎈",              # an emoji, or a path to an image file
    layout="centered",
    initial_sidebar_state="expanded",
)


# =============================================================================
# SECTION 0 - START HERE: how Streamlit actually works
# =============================================================================
def section_0_how_it_works() -> None:
    st.title("🎈 Streamlit in one page")
    st.markdown(
        """
        **Streamlit turns a Python script into a web app.**
        No HTML, no CSS, no JavaScript, no callbacks to wire up - you write
        `st.something(...)` and it appears on the page, in the order it runs.
        """
    )

    st.subheader("The execution model")
    st.markdown(
        """
        1. The user opens the app -> Streamlit runs the script top to bottom.
        2. The user interacts with a widget -> Streamlit runs the **whole script
           again**, from line 1.
        3. Widgets keep their values across that re-run, so the page looks stable.
        """
    )

    # --- A live proof that the script really does re-run -----------------------
    # st.session_state is the only thing that survives a re-run (section 4).
    # We use it here purely as a counter of how many times this script has run.
    if "run_count" not in st.session_state:
        st.session_state.run_count = 0
    st.session_state.run_count += 1     # this line executes once per script run

    st.info(
        f"This script has run **{st.session_state.run_count}** time(s) "
        "since you opened the tab. Click the button below and watch it jump."
    )
    # Clicking any widget triggers a re-run, which increments the counter above.
    st.button("Click me and watch the number above change")

    st.divider()
    st.subheader("What each menu item covers")
    st.markdown(
        """
        | Section | Topic |
        |---|---|
        | 1 | Hello World - `st.title`, `st.text_input`, `st.write` |
        | 2 | Core components - text, number, button, slider, checkbox, radio, selectbox |
        | 3 | Displaying data - `write` vs `markdown`, lists, dicts, tables, file upload |
        | 4 | Interactivity - `st.session_state` and `st.form` |
        """
    )
    st.caption("Use the sidebar on the left to move between sections. 👈")


# =============================================================================
# SECTION 1 - STREAMLIT HELLO WORLD
# =============================================================================
# The smallest useful app: a title, one input, one output.
# Three commands do all the work:
#   st.title()      -> big page heading
#   st.text_input() -> a text box; RETURNS whatever the user typed (a str)
#   st.write()      -> prints almost anything to the page
# =============================================================================
def section_1_hello_world() -> None:
    st.title("1. Streamlit Hello World")

    st.markdown(
        "The classic first app. Save it as `app.py` and run "
        "`streamlit run app.py`:"
    )

    # st.code() shows a syntax-highlighted, copy-able code block.
    # It only DISPLAYS code - it does not execute it.
    st.code(
        '''import streamlit as st

st.title("My First Streamlit App")
name = st.text_input("What's your name?")
if name:
    st.write(f"Hello, {name}!")''',
        language="python",
    )

    st.markdown("**Terminal commands:**")
    st.code("pip install streamlit\nstreamlit run app.py", language="bash")

    st.divider()
    st.subheader("The same app, running live right here")

    # Everything inside `with st.echo():` is executed AND printed on the page.
    with st.echo():
        st.title("My First Streamlit App")

        # text_input returns the current contents of the box as a string.
        # On the very first run nothing is typed yet, so it returns "".
        name = st.text_input("What's your name?")

        # "" is falsy in Python, so this is a neat way of saying
        # "only greet the user once they have typed something".
        if name:
            st.write(f"Hello, {name}!")

    st.divider()
    st.subheader("What just happened")
    st.markdown(
        """
        - You typed a letter -> Streamlit **re-ran the whole script**.
        - On that re-run `st.text_input(...)` returned the new text.
        - `if name:` became `True`, so `st.write(...)` drew the greeting.

        There is no "on change" handler anywhere. The script simply runs again
        and the new value flows through your normal Python `if` statement.
        """
    )
    st.success("Try it: edit this file, hit save, and Streamlit offers to rerun.")

    # Teacher note: when running with `streamlit run`, saving the file shows a
    # "Rerun / Always rerun" prompt in the top-right corner - that is live reload.


# =============================================================================
# SECTION 2 - CORE STREAMLIT COMPONENTS
# =============================================================================
# Every input widget follows the SAME pattern:
#
#       value = st.widget("Label", ...options...)
#
# The widget draws itself and RETURNS its current value immediately. You then
# use that value with plain Python. No callbacks required.
# =============================================================================
def section_2_core_components() -> None:
    st.title("2. Core Streamlit Components")

    # -------------------------------------------------------------------------
    # 2.1 BASIC INPUT COMPONENTS
    # -------------------------------------------------------------------------
    st.header("2.1 Basic Input Components")

    # --- Text input ----------------------------------------------------------
    st.subheader("Text input - st.text_input()")
    # Signature used here: st.text_input(label, value)
    #   label -> the caption shown above the box
    #   value -> the text the box starts with (the 2nd positional argument)
    with st.echo():
        name = st.text_input("What's your name?",placeholder="Type here...")

        # Because the box starts out holding placeholder text, we compare
        # against that text instead of using `if name:`.
        if name != "Type here...":
            st.write(f"Hello {name}!")

    st.caption(
        "Tip: passing placeholder='Type here...' instead shows grey hint text, "
        "which keeps the returned value an empty string until the user types."
    )

    # --- Password input ------------------------------------------------------
    st.subheader("Password input - type='password'")
    # Same widget, one extra argument: the characters are masked on screen.
    # NOTE for students: masking is cosmetic. Never hard-code real secrets in
    # your script - Streamlit provides st.secrets for that.
    with st.echo():
        password = st.text_input("Enter password", type="password",max_chars=16)
        if password:
            st.write("Password length:", len(password))

    # --- Number input --------------------------------------------------------
    st.subheader("Number input - st.number_input()")
    # min_value / max_value clamp the input; value is the starting number.
    # Pass ints and you get an int back; pass floats and you get a float.
    with st.echo():
        age = st.number_input("Enter your age", min_value=0, max_value=120, value=25)
        st.write(f"You are {age} years old")

    # --- Button --------------------------------------------------------------
    st.subheader("Button - st.button()")
    # THE most important gotcha in Streamlit:
    # st.button() returns True ONLY on the single re-run caused by the click.
    # On the next interaction it is False again - a button is a pulse, not a
    # switch. If something must stay on, use st.checkbox() or store a flag in
    # st.session_state (section 4).
    with st.echo():
        if st.button("Click me!"):
            st.write("Button was clicked!")
        else:
            st.write("Button hasn't been clicked yet")

    st.warning(
        "Click the button, then drag any slider below: the message disappears. "
        "That is the button pulse - the classic beginner surprise.",
        icon="⚠️",
    )

    st.divider()

    # -------------------------------------------------------------------------
    # 2.2 SELECTION COMPONENTS
    # -------------------------------------------------------------------------
    st.header("2.2 Selection Components")

    # --- Slider (numeric) ----------------------------------------------------
    st.subheader("Slider - st.slider()")
    # Positional arguments: st.slider(label, min_value, max_value, default)
    with st.echo():
        number = st.slider("Pick a number", 0, 100, 50)
        st.write(f"You picked: {number}")

    # --- Slider (time range) -------------------------------------------------
    st.subheader("Range slider with times")
    # The slider is polymorphic:
    #   - pass a TUPLE as `value` -> you get a two-handled RANGE slider
    #   - pass datetime.time / date objects -> you get a time / date slider
    # It returns a tuple (start, end) of the same type you passed in.
    with st.echo():
        appointment = st.slider(
            "Schedule your appointment:",
            value=(time(11, 30), time(12, 45)),   # a tuple -> range slider
        )
        st.write("Your appointment:", appointment)

    # --- Checkbox ------------------------------------------------------------
    st.subheader("Checkbox - st.checkbox()")
    # Returns a bool: True when ticked. Unlike a button it STAYS True, which
    # makes it the standard way to show or hide part of a page.
    with st.echo():
        if st.checkbox("Show/Hide"):
            st.write("You can see this text!")

    # --- Radio ---------------------------------------------------------------
    st.subheader("Radio buttons - st.radio()")
    # Pass a list of options; the widget RETURNS THE OPTION ITSELF (here a str),
    # not its position. Use index=0/1/2 to pick which starts selected, or
    # index=None to start with nothing selected.
    with st.echo():
        favorite_color = st.radio(
            "What's your favorite color?",
            ["Red", "Green", "Blue"],
        )
        st.write(f"Your favorite color is {favorite_color}")

    # --- Selectbox -----------------------------------------------------------
    st.subheader("Select box - st.selectbox()")
    # Same idea as radio, drawn as a dropdown. Use radio for 2-4 options (all
    # visible at once) and selectbox when the list is long.
    with st.echo():
        activity = st.selectbox(
            "What are you doing?",
            ["Eating", "Sleeping", "Coding"],
        )
        st.write(f"You are {activity}")

    st.divider()
    st.subheader("Bonus: one close relative")
    # st.multiselect is selectbox for many answers: it returns a LIST of the
    # chosen options (an empty list when nothing is selected).
    with st.echo():
        languages = st.multiselect(
            "Which languages do you know?",
            ["Python", "JavaScript", "C++", "Arabic", "English"],
            default=["Python"],
        )
        st.write("You picked:", languages)


# =============================================================================
# SECTION 3 - DISPLAYING DATA IN STREAMLIT
# =============================================================================
# Streamlit has one "magic" output command (st.write) plus a family of
# specialised ones (st.markdown, st.table, st.dataframe, st.json, ...).
# Rule of thumb: reach for st.write first, switch to a specific command when
# you need control over the formatting.
# =============================================================================
def section_3_displaying_data() -> None:
    st.title("3. Displaying Data in Streamlit")

    # -------------------------------------------------------------------------
    # 3.1 TEXT DISPLAY METHODS
    # -------------------------------------------------------------------------
    st.header("3.1 Text Display Methods")

    st.markdown(
        """
        **`st.write()`** is the swiss-army knife: it looks at the *type* of what
        you give it and picks a sensible renderer - strings, numbers, lists,
        dicts, DataFrames, charts, even matplotlib figures.

        **`st.markdown()`** does one job: render a string as Markdown.
        """
    )

    with st.echo():
        # st.write() - accepts several arguments and joins them with spaces
        st.write("Normal text with st.write()")
        st.write("You can write", "multiple", "arguments")
        st.write("...and non-text objects too:", [1, 2, 3], 42)

        # st.markdown() - formatting comes from the Markdown syntax itself
        st.markdown("# This is a heading")
        st.markdown("**Bold text** and *italic text*")
        st.markdown("- Bullet point 1\n- Bullet point 2")

    st.caption(
        "Note the \\n inside that last string: Markdown needs a real newline "
        "between list items, so one string with \\n gives two bullets."
    )

    # The dedicated heading commands are shortcuts for common Markdown:
    #   st.title()     ~ "# "      (one per page, at the top)
    #   st.header()    ~ "## "
    #   st.subheader() ~ "### "
    #   st.caption()   -> small grey helper text
    #   st.code()      -> syntax-highlighted block with a copy button
    #   st.text()      -> fixed-width text, no Markdown parsing at all
    st.info(
        "Shortcuts: st.title / st.header / st.subheader are just Markdown "
        "headings; st.caption is small grey text; st.text does no formatting.",
        icon="ℹ️",
    )

    st.divider()

    # -------------------------------------------------------------------------
    # 3.2 DISPLAYING DATA STRUCTURES
    # -------------------------------------------------------------------------
    st.header("3.2 Displaying Data Structures")

    st.subheader("Lists and dictionaries")
    with st.echo():
        # A list renders as a small read-only table of its items.
        my_list = ["apple", "banana", "orange"]
        st.write("List:", my_list)

        # A dict renders as an expandable, collapsible JSON viewer.
        my_dict = {
            "name": "John",
            "age": 30,
            "city": "New York",
        }
        st.write("Dictionary:", my_dict)

    st.subheader("Tables: st.table() vs st.dataframe()")
    st.markdown(
        """
        | | `st.table()` | `st.dataframe()` |
        |---|---|---|
        | Rendering | static, every row drawn at once | interactive grid |
        | Sorting / resizing | no | yes, click a column header |
        | Scrolling | no - the page grows | yes, fixed height |
        | Best for | small summary tables | real datasets |
        """
    )

    with st.echo():
        # pandas is already installed as a Streamlit dependency.
        df = pd.DataFrame(
            {
                "Name": ["John", "Anna", "Peter"],
                "Age": [25, 30, 35],
                "City": ["New York", "Paris", "London"],
            }
        )

        st.write("Simple table:")
        st.table(df)            # static - good for 3 rows like this

        st.write("Interactive dataframe:")
        st.dataframe(df)        # sortable / scrollable - good for 3000 rows

    st.caption(
        "st.write(df) is a third option: it forwards a DataFrame to "
        "st.dataframe automatically."
    )

    st.divider()

    # -------------------------------------------------------------------------
    # 3.3 FILE UPLOADER
    # -------------------------------------------------------------------------
    st.header("3.3 File Uploader")

    st.markdown(
        """
        `st.file_uploader()` returns **`None`** until a file is chosen, and then
        an `UploadedFile` object. That object behaves like an open file, so it
        can be handed straight to `pd.read_csv()`, `open()`-style readers,
        `PIL.Image.open()`, and so on.

        Always guard with `if uploaded_file is not None:` - on the first run
        there is no file yet and the script still has to finish.
        """
    )

    # Give the class something to upload: a download button producing a CSV.
    # .to_csv(index=False) makes the text, .encode() turns it into bytes,
    # which is what st.download_button wants.
    sample_csv = pd.DataFrame(
        {
            "Name": ["John", "Anna", "Peter", "Linda"],
            "Age": [25, 30, 35, 28],
            "City": ["New York", "Paris", "London", "Cairo"],
        }
    ).to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download a sample CSV to test with",
        data=sample_csv,
        file_name="sample_people.csv",
        mime="text/csv",
    )

    with st.echo():
        # type="csv" filters the OS file picker and rejects other extensions.
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write("Data from your CSV file:")
            st.dataframe(df)

            # Handy metadata carried on the uploaded object:
            st.caption(f"File name: {uploaded_file.name} - {uploaded_file.size} bytes")

    st.info(
        "Useful arguments: accept_multiple_files=True returns a LIST of files, "
        "and type=['csv', 'xlsx'] accepts several extensions.",
        icon="ℹ️",
    )


# =============================================================================
# SECTION 4 - CREATING INTERACTIVE APPLICATIONS
# =============================================================================
# Sections 1-3 were one-way: user input in, output drawn. Real apps need to
# REMEMBER things across re-runs (session state) and to collect several inputs
# before doing any work (forms).
# =============================================================================
def section_4_interactive_apps() -> None:
    st.title("4. Creating Interactive Applications")

    # -------------------------------------------------------------------------
    # 4.1 SESSION STATE
    # -------------------------------------------------------------------------
    st.header("4.1 Session State")

    st.markdown(
        """
        Remember the big idea: **the whole script re-runs on every interaction**,
        so ordinary variables are rebuilt from scratch each time. `count = 0`
        would reset to 0 forever.

        `st.session_state` is a dictionary that Streamlit keeps alive **for one
        browser session**. Values you put there survive re-runs. Open the app in
        a second tab and you get a second, independent session state.

        The standard three-step pattern:
        1. **initialise** it once, guarded by `if "key" not in st.session_state`
        2. **update** it inside an `if st.button(...)` block
        3. **read** it wherever you need the value
        """
    )

    with st.echo():
        # 1. Initialise - runs only on the very first script run of the session.
        if "count" not in st.session_state:
            st.session_state.count = 0

        # 2. Update - the button is True only on the run caused by the click,
        #    so the counter goes up exactly once per click.
        if st.button("Increment"):
            st.session_state.count += 1

        # 3. Read - both syntaxes work: attribute and dictionary style.
        st.write("Count = ", st.session_state.count)

    # A second button showing that state is shared by everything on the page.
    if st.button("Reset counter"):
        st.session_state.count = 0
        # st.rerun() restarts the script immediately, so the page redraws with
        # the new value rather than waiting for the next interaction.
        st.rerun()

    st.subheader("Widgets can live in session state too")
    # Passing key="..." to any widget stores its value in
    # st.session_state["..."], so other parts of the script can read it by name.
    with st.echo():
        st.text_input("Your city", key="city_box")
        st.write("session_state['city_box'] =", st.session_state.get("city_box", ""))

    # Peek at the whole dictionary - very useful when teaching or debugging.
    with st.expander("Peek inside st.session_state"):
        st.write(dict(st.session_state))

    st.divider()

    # -------------------------------------------------------------------------
    # 4.2 FORMS
    # -------------------------------------------------------------------------
    st.header("4.2 Forms")

    st.markdown(
        """
        Without a form, **every keystroke re-runs the script** - fine for a guide,
        wasteful when the app queries a database or calls an API.

        `st.form()` batches widgets: nothing is re-run while the user fills them
        in, and everything is submitted together when the submit button is
        pressed.

        Two rules:
        - every form needs exactly one **`st.form_submit_button()`**
        - a plain `st.button()` is **not allowed** inside a form
        """
    )

    with st.echo():
        # "contact_form" is the form's unique key - each form needs its own.
        with st.form("contact_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            message = st.text_area("Message")

            # Returns True on the run where the form was submitted.
            submitted = st.form_submit_button("Submit")

            if submitted:
                st.success("Thank you for your message!")
                st.write(f"We'll contact {name} at {email}")

    st.caption(
        "Try it: type in the boxes and watch nothing happen until you press "
        "Submit. That is the whole point of a form."
    )

    # Small extra worth showing: validating before acting on the submission.
    st.subheader("Validating a submission")
    with st.echo():
        with st.form("signup_form", clear_on_submit=True):   # empties on submit
            username = st.text_input("Username")
            agreed = st.checkbox("I accept the terms")
            if st.form_submit_button("Create account"):
                if not username:
                    st.error("Username is required.")
                elif not agreed:
                    st.warning("You must accept the terms.")
                else:
                    st.success(f"Account created for {username}!")
                    st.balloons()          # a little confetti animation


# =============================================================================
# BONUS - a one-screen cheat sheet to leave on the projector
# =============================================================================
def section_5_cheat_sheet() -> None:
    st.title("Cheat sheet")

    st.markdown(
        """
        ### The rule
        The script re-runs top to bottom on **every** interaction.

        ### Text
        `st.title` `st.header` `st.subheader` `st.markdown` `st.caption`
        `st.code` `st.text` `st.write` (accepts anything)

        ### Input
        `st.text_input` `st.text_area` `st.number_input` `st.button`
        `st.checkbox` `st.radio` `st.selectbox` `st.multiselect` `st.slider`
        `st.file_uploader` `st.date_input` `st.time_input` `st.color_picker`

        ### Data
        `st.table` (static) `st.dataframe` (interactive) `st.json` `st.metric`

        ### Charts (all take a DataFrame)
        `st.line_chart` `st.bar_chart` `st.area_chart` `st.scatter_chart` `st.map`

        ### Layout
        `st.sidebar` `st.columns` `st.tabs` `st.expander` `st.container`

        ### Status
        `st.success` `st.info` `st.warning` `st.error` `st.spinner`
        `st.progress` `st.balloons`

        ### State and flow
        `st.session_state` `st.form` `st.form_submit_button` `st.rerun`
        `st.cache_data` (cache slow functions / data loading)
        """
    )

    st.subheader("Charts in three lines")
    # Every built-in chart takes a DataFrame and picks sensible axes for you.
    with st.echo():
        chart_df = pd.DataFrame(
            {"Sales": [120, 150, 90, 200], "Returns": [10, 25, 5, 30]},
            index=["Jan", "Feb", "Mar", "Apr"],
        )
        st.line_chart(chart_df)
        st.bar_chart(chart_df)

    st.subheader("Layout in three lines")
    with st.echo():
        left, right = st.columns(2)          # two side-by-side containers
        left.metric("Revenue", "$1,200", "+12%")
        right.metric("Returns", "70", "-4%")

    st.subheader("Where to go next")
    st.markdown(
        """
        - **Multipage apps:** create a `pages/` folder next to your main script -
          every `.py` file inside becomes a page in the sidebar automatically.
          (The newer, more flexible API is `st.Page` + `st.navigation`.)
        - **Speed:** decorate slow functions with `@st.cache_data` so they are
          not re-executed on every re-run.
        - **Deploying:** push to GitHub and use share.streamlit.io to host it free.
        - **Docs:** https://docs.streamlit.io - the API reference lists every command.
        """
    )


# =============================================================================
# SIDEBAR NAVIGATION  -  this is what actually runs
# =============================================================================
# Everything above is just function definitions; nothing has been drawn yet.
# The code below runs on every re-run, draws the sidebar menu, and calls the
# ONE section function the user selected.
#
# Anything drawn with `st.sidebar.*` (or inside a `with st.sidebar:` block)
# goes into the left panel instead of the main page.
# =============================================================================

# A dict mapping menu label -> the function that draws that page.
# Note we store the function OBJECT (no parentheses) and call it later.
PAGES = {
    "Start here: how Streamlit works": section_0_how_it_works,
    "1. Hello World": section_1_hello_world,
    "2. Core Components": section_2_core_components,
    "3. Displaying Data": section_3_displaying_data,
    "4. Interactive Apps": section_4_interactive_apps,
    "Cheat sheet": section_5_cheat_sheet,
}

st.sidebar.title("Streamlit Guide")
st.sidebar.caption("A teaching walkthrough")

# st.sidebar.radio returns the selected label, exactly like st.radio.
choice = st.sidebar.radio("Go to section:", list(PAGES.keys()))

st.sidebar.divider()
st.sidebar.markdown(
    "**Run it with:**\n\n`streamlit run streamlit_guide.py`\n\n"
    "Every widget you touch re-runs this whole file."
)

# Look up the chosen function and CALL it - that draws the selected page.
PAGES[choice]()

# Teacher note: this dictionary trick is a hand-rolled "multipage app" that
# keeps the guide in a single file. For real projects Streamlit has built-in
# multipage support (a `pages/` folder, or st.Page + st.navigation), which
# gives each page its own file and its own URL.
