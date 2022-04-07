#CISC 467 - :notebook_with_decorative_cover: Professor Rating System :books:
This is a project by Jake Ahearne, Aubrey McLeod, and Renee Tibando.

##:fire:about:fire:
This project uses a fuzzy linguistic ruleset to produce a defuzzified rating for a given professor (1-10). 
The user is asked to rate a professor using linguistic descriptors, and these
rating are translated into production rules based on our own research and data collection.

We employ a backend database to track and aggregate overall reviews for professors.

##:bar_chart: our data :chart_with_upwards_trend:
Our data was collected using an online survey which was distributed over multiple channels.

The survey was split into two sections. In the first section respondents where asked to rank attributes according to how
relevant they felt the attribute was in relation to being a good professor. This question was asked across three broader
categories in relation to pedagogy. The queried attributes were:
```
|Communication
+--Email Reply Speed
+--Public Speaking Ability
+--Ability to Fluently Speak Classroom Language
+--Ability to Effectively Convey Course Topics
+--Ability to Communicate in a One-on-one setting
+--Availability Outside of Classroom
+--Classroom Management Skills
+--Empathy towards Students

|Course Content
+--Course Workload
+--Preparedness for Lesson
+--Weighting of Assignments
+--Quality of Course Assessments
+--Quality of Course Web-platform
+--How the Material Prepares Students for Working in Relevant Field
+--Resources Available to Students

|Experience
+--Knowledge of Topic
+--Length of Pedigogical Experience
+--Has Tenure
+--Rate My Professor Score
+--Number of Publications
+--Number of Times Teaching the Current Course
```

In the second section, respondents where asked to determine whether each of the above attributes
contributed positively towards a professor being good, contributed neutrally, or was completely irrelevant towards a professor being good.

For more information, see the `dataset/data.md`; raw results are stored in `dataset/raw.csv`

##:factory: our production rules :factory:
*insert relevant test here...*
##setup
First we need to install the requirements with: `pip install -r requirements.txt`

Then set up the MySQL Database, using:
```
CREATE DATABASE professor_rating_system;

USE professor_rating_system;

CREATE TABLE professors (
    ID int AUTO_INCREMENT PRIMARY KEY,    
    firstname varchar(20),
    lastname varchar(20),
    
    email_reply float(24),
    public_speaking float(24),
    fluency float(24),
    concept_conveyence float(24),
    one_on_one float(24),
    availability float(24),
    classroom_management float(24),
    empathy float(24),
    
    workload float(24),
    preparedness float(24),
    assignment_weighting float(24),
    assessment_quality float(24),
    webplatform_quality float(24),
    workplace_applicability float(24),
    available_resources float(24),
    
    domain_knowledge float(24),
    experience_length float(24),
    tenured float(24),
    rate_my_prof_score float(24),
    frequently_published float(24),
    course_iterations float(24)
);
```

After creating the DB, we just need to create a Streamlit config file at `.streamlit/secrets.toml`, and configure it using:
```
# .streamlit/secrets.toml
[mysql]
host = "[DB URL]"
port = [DB PORT]
database = "professor_rating_system"
user = "[DB Username]"
password = "[DB Password]"
```