import streamlit as st

st.set_page_config(
    page_title="Student Grade Analyzer",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Student Grade Analyzer")
st.caption("Python Fundamentals + Streamlit Demo")

st.divider()

name = st.text_input("Student name")

python_score = st.slider("Python", 0, 100, 70)
cloud_score = st.slider("Cloud Computing", 0, 100, 70)
database_score = st.slider("Databases", 0, 100, 70)

scores = {
    "Python": python_score,
    "Cloud Computing": cloud_score,
    "Databases": database_score
}


def calculate_average(student_scores):
    total = sum(student_scores.values())
    return total / len(student_scores)


def get_grade(average):
    if average >= 70:
        return "Distinction"
    elif average >= 60:
        return "Merit"
    elif average >= 40:
        return "Pass"
    else:
        return "Fail"


if st.button("Analyse Results", use_container_width=True):

    if not name:
        st.warning("Please enter a student name.")

    else:
        average = calculate_average(scores)
        grade = get_grade(average)

        st.subheader(f"Results for {name}")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Average Score", f"{average:.1f}%")

        with col2:
            st.metric("Final Grade", grade)

        st.divider()

        st.subheader("Module Results")

        for subject, score in scores.items():

            st.write(f"**{subject}** — {score}%")
            st.progress(score / 100)

        st.divider()

        strongest_subject = max(scores, key=scores.get)
        weakest_subject = min(scores, key=scores.get)

        st.success(
            f"Strongest subject: {strongest_subject} "
            f"({scores[strongest_subject]}%)"
        )

        st.info(
            f"Area to improve: {weakest_subject} "
            f"({scores[weakest_subject]}%)"
        )

        if grade == "Fail":
            st.error("Student requires additional support.")
        elif grade == "Pass":
            st.warning("Good progress. Keep practising.")
        else:
            st.balloons()