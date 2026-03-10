import streamlit as st
import pandas as pd
from datetime import date, time

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(page_title="Scheduling Planner", layout="wide")

# ---------------- SESSION STATE ----------------
if "schedules" not in st.session_state:
    st.session_state.schedules = []

# ---------------- SIDEBAR NAVIGATION ----------------
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Home", "Create Schedule", "Schedule Dashboard", "About"]
)

# ---------------- HOME PAGE ----------------
if page == "Home":

    st.title("📅 Scheduling Planner")

    st.write("""
This application helps students organize their daily tasks and schedules.
Users can create tasks, assign priorities, track progress, and visualize their workload.
""")

    st.info("Use the sidebar to create and manage your schedule.")

    st.image(
        "https://images.unsplash.com/photo-1506784983877-45594efa4cbe",
        use_column_width=True
    )

# ---------------- CREATE SCHEDULE ----------------
elif page == "Create Schedule":

    st.title("📝 Create a Schedule")

    with st.form("schedule_form"):

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Name")
            task = st.text_input("Task / Subject")

            category = st.selectbox(
                "Category",
                ["Study", "Work", "Exercise", "Personal", "Other"]
            )

            priority = st.select_slider(
                "Priority Level",
                ["Low", "Medium", "High", "Urgent"]
            )

        with col2:

            schedule_date = st.date_input("Date", date.today())

            schedule_time = st.time_input("Time", time(9, 0))

            duration = st.slider("Duration (hours)", 1, 10)

            repeat = st.radio(
                "Repeat Task?",
                ["No", "Daily", "Weekly"]
            )

        description = st.text_area("Notes / Description")

        reminder = st.checkbox("Enable Reminder")

        file_upload = st.file_uploader("Upload File")

        color = st.color_picker("Task Color")

        motivation = st.selectbox(
            "Motivation Level",
            ["Low", "Medium", "High", "Very High"]
        )

        submitted = st.form_submit_button("Save Schedule")

    if submitted:

        new_task = {
            "Name": name,
            "Task": task,
            "Category": category,
            "Priority": priority,
            "Date": schedule_date,
            "Time": schedule_time,
            "Duration": duration,
            "Status": "Pending"
        }

        st.session_state.schedules.append(new_task)

        st.success("✅ Schedule saved successfully!")

        st.write("### Schedule Summary")
        st.json(new_task)

# ---------------- DASHBOARD ----------------
elif page == "Schedule Dashboard":

    st.title("📊 Schedule Dashboard")

    if len(st.session_state.schedules) == 0:

        st.warning("No schedules created yet.")

    else:

        df = pd.DataFrame(st.session_state.schedules)

        # ---------- FILTERS ----------
        st.subheader("🔎 Filter Tasks")

        col1, col2 = st.columns(2)

        with col1:
            category_filter = st.selectbox(
                "Filter by Category",
                ["All"] + list(df["Category"].unique())
            )

        with col2:
            priority_filter = st.selectbox(
                "Filter by Priority",
                ["All"] + list(df["Priority"].unique())
            )

        if category_filter != "All":
            df = df[df["Category"] == category_filter]

        if priority_filter != "All":
            df = df[df["Priority"] == priority_filter]

        # ---------- TABLE ----------
        st.subheader("📋 Schedule Table")
        st.dataframe(df)

        st.subheader("📑 Schedule List")
        st.table(df)

        # ---------- MARK TASK COMPLETE ----------
        st.subheader("✔ Mark Task Completed")

        for i, task in enumerate(st.session_state.schedules):

            completed = st.checkbox(
                f"{task['Task']} ({task['Status']})",
                key=i
            )

            if completed:
                st.session_state.schedules[i]["Status"] = "Done"
            else:
                st.session_state.schedules[i]["Status"] = "Pending"

        # ---------- DELETE TASK ----------
        st.subheader("❌ Delete Task")

        task_to_delete = st.selectbox(
            "Select Task",
            df["Task"]
        )

        if st.button("Delete Task"):

            st.session_state.schedules = [
                t for t in st.session_state.schedules
                if t["Task"] != task_to_delete
            ]

            st.success("Task deleted successfully!")
            st.rerun()

        # ---------- METRICS ----------
        st.subheader("📊 Productivity Metrics")

        total_tasks = len(df)

        total_hours = df["Duration"].sum()

        completed_tasks = len(df[df["Status"] == "Done"])

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Tasks", total_tasks)
        col2.metric("Total Study Hours", total_hours)
        col3.metric("Completed Tasks", completed_tasks)

        st.progress(min(total_tasks * 10, 100))

        # ---------- CHART ----------
        st.subheader("📈 Task Duration Chart")

        st.bar_chart(df.set_index("Task")["Duration"])

        # ---------- DOWNLOAD CSV ----------
        st.subheader("⬇ Download Schedule")

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Schedule as CSV",
            data=csv,
            file_name="schedule.csv",
            mime="text/csv",
        )

# ---------------- ABOUT PAGE ----------------
elif page == "About":

    st.title("ℹ️ About This App")

    st.markdown("""
### What the App Does
This scheduling planner helps users organize and manage their daily tasks.
Users can create schedules, assign priorities, and track their productivity.

### Target Users
- Students
- Professionals
- Anyone who wants to manage their time effectively

### Inputs Collected
The application collects:
- Name
- Task or subject
- Category
- Priority level
- Date and time
- Duration
- Notes
- File uploads
- Reminder option
- Motivation level

### Outputs Displayed
The app shows:
- Schedule summaries
- Task tables
- Charts showing duration
- Productivity metrics
- Downloadable schedule file
""")
