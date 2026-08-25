# Streamlit Learning Projects

This repository contains a small collection of Streamlit apps and lab exercises designed to teach interactive web app development with Python.

## Overview

The projects cover common beginner-to-intermediate Streamlit concepts, including:

- Text inputs and widgets
- Forms and buttons
- Data display and tables
- Session state
- Charts and metrics
- Simple ML prediction interfaces
- Expense tracking and grade analysis

## Project Structure

```text
streamlit/
├── BMI_Calculator/
│   └── BMI.py                 # BMI calculator app
├── expense_tracker/
│   └── expense.py             # Personal expense tracker
├── grade_analyzer/
│   └── grade.py               # Student grade analyzer
├── guide/
│   └── streamlit_guide.py     # Teaching guide and examples
├── iris_flowers/
│   ├── iris_flower_classifier.py
│   ├── iris_model.pkl         # Trained ML model
│   └── train_model.py         # Model training script
├── spend_tracker/
│   ├── LAB.md                 # Lab instructions
│   ├── lab_starter.py         # Starter for the lab exercise
│   └── sample_expenses.csv    # Sample expense data
├── .gitignore
├── README.md
└── .venv/
```

## Prerequisites

Make sure Python is installed, then install the required packages:

```bash
pip install streamlit pandas scikit-learn joblib
```

If you are already using a virtual environment, activate it first.

## Running the Apps

From the project root, run any app with Streamlit:

```bash
streamlit run BMI_Calculator/BMI.py
```

Other apps:

```bash
streamlit run expense_tracker/expense.py
streamlit run grade_analyzer/grade.py
streamlit run guide/streamlit_guide.py
streamlit run iris_flowers/iris_flower_classifier.py
```

## Notes on the Lab App

The spend tracker lab in the `spend_tracker` folder is a guided exercise. Open `spend_tracker/LAB.md` for the step-by-step instructions and work from `lab_starter.py`.

## Learning Goals

By completing these examples, you will practice:

- Creating interactive UI components with Streamlit
- Managing app state across reruns
- Building small business and academic dashboards
- Processing data with Pandas
- Creating simple machine learning demos

## Useful Tips

- Run apps with `streamlit run <file>.py`, not with `python <file>.py`
- Save the file while the app is running to trigger a rerun in the browser
- Use `st.session_state` when values need to persist between interactions

## License

This project is intended for educational use.
