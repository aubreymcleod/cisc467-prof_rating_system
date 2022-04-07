"""
This file defines a form that the user can fill out to get their profs score. Once the user has rated their professor,
the screen should rerender and display graphical breakdowns of the qualities of their professor.

They are prompted as to whether or not they would like to commit their score to the database; upon completion,
they will then be taken back to the rating page.
"""
import streamlit as st

from src.library.rule_engine import evaluate

def app():
    st.title("CISC 467 - Fuzzy Logic-based Professor Rating System")
    if "results" in st.session_state:
        _results()
    else:
        _form()

def _results():
    st.header("Rated Professor")
    with st.form("Output"):
        valuation = evaluate(st.session_state["input_values"])

        for name, attribute in valuation.items():
            st.subheader(name)
            for level, value in attribute.items():
                st.write(str(level)+": "+str(value))

        if st.form_submit_button("Back"):
            del st.session_state["results"]

def _form():
    st.header("Rate a professor")
    st.markdown(
        """
        Please fill out the following form, by rating the your chosen professor on a scale between 1 and 10\\
        1 being strong disagreement.
        10 being strong agreement.
        """
    )
    with st.form("Professor Ratings"):

        st.subheader("Communication skills")
        com_email = st.slider("In my experience, the professor replies immediately to emails", min_value=1, max_value=10)
        com_public_speaking = st.slider("I feel that the professor speaks confidently in front of the entire class", min_value=1, max_value=10)
        com_native_speaker = st.slider("There is no language barrier between the professor and I", min_value=1, max_value=10)
        com_concept_conveyance = st.slider("In my experience, the professor effectively conveys new concepts", min_value=1, max_value=10)
        com_one_on_one = st.slider("I have found that the professor is effective in one-on-one discussion", min_value=1, max_value=10)
        com_availability = st.slider("The professor is always available to meet with me outside of class", min_value=1, max_value=10)
        com_class_management = st.slider("In my experience, the professor always exerts high level of control over students in the classroom", min_value=1, max_value=10)
        com_empathy = st.slider("I find the professor to be highly empathetic", min_value=1, max_value=10)

        st.subheader("Course Content")
        cor_workload = st.slider("The course workload is very high", min_value=1, max_value=10)
        cor_preparation = st.slider("The professor is generally very prepared for class", min_value=1, max_value=10)
        cor_weight_assignments = st.slider("The weightings of individual assessments is very high", min_value=1, max_value=10)
        cor_assessments = st.slider("The course assessments are reflective of course content", min_value=1, max_value=10)
        cor_webplatform = st.slider("The course's web platform is generally well designed and intuitive", min_value=1, max_value=10)
        cor_reallife = st.slider("The content of the course is applicable to the real world", min_value=1, max_value=10)
        cor_resources = st.slider("There are sufficient resources available to me, so that I feel prepared", min_value=1, max_value=10)

        st.subheader("Academic Experience")
        aca_knowledge = st.slider("The professor is very knowledgable about the course subject matter", min_value=1, max_value=10)
        aca_career_length = st.slider("The professor has had a very long career", min_value=1, max_value=10)
        aca_tenured = st.slider("The professor is likely tenured", min_value=1, max_value=10, step=9)
        aca_rate_my_prof = st.slider("The professor has a high Rate My Professor Score", min_value=1, max_value=10)
        aca_publications = st.slider("The professor is highly published", min_value=1, max_value=10)
        aca_repeat_instruction = st.slider("The professor has taught this course many many times", min_value=1, max_value=10)

        # Buttons here
        if st.form_submit_button("Calculate"):
            bulk_representation = {"email_speed": com_email/10.0,
                                    "public_speaking": com_public_speaking/10.0,
                                    "native_speaker": com_native_speaker/10.0,
                                    "explanation_quality": com_concept_conveyance/10.0,
                                    "one_on_one": com_one_on_one/10.0,
                                    "availability": com_availability/10.0,
                                    "class_management": com_class_management/10.0,
                                    "empathy": com_empathy/10.0,
                                    "workload": cor_workload/10.0,
                                    "preparation": cor_preparation/10.0,
                                    "assignment_value": cor_weight_assignments/10.0,
                                    "assignment_quality": cor_assessments/10.0,
                                    "webplatform_quality": cor_webplatform/10.0,
                                    "real_world_applicability": cor_reallife/10.0,
                                    "available_resources": cor_resources/10.0,
                                    "knowledge": aca_knowledge/10.0,
                                    "career_length": aca_career_length/10.0,
                                    "tenure": aca_tenured/10.0,
                                    "rate_my_prof_score": aca_rate_my_prof/10.0,
                                    "publication": aca_publications/10.0,
                                    "repeat_instruction": aca_repeat_instruction/10.0}
            st.session_state["input_values"] = bulk_representation
            st.session_state["results"] = True
