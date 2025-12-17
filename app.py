

import streamlit as st


st.set_page_config(page_title="Student Percentage & Grade Calculator", layout="centered")

st.title("Student Percentage & Grade Calculator")
st.write("Enter the number of subjects, marks for each subject, then click Calculate to get percentage and grade.")


def get_grade(percentage: float) -> str:
	if percentage >= 90:
		return "A+"
	if percentage >= 80:
		return "A"
	if percentage >= 70:
		return "B"
	if percentage >= 60:
		return "C"
	if percentage >= 50:
		return "D"
	return "F"


num_subjects = int(st.number_input("Number of subjects", min_value=1, max_value=50, value=3, step=1))
max_marks = float(st.number_input("Max marks per subject", min_value=1.0, value=100.0, step=1.0))

with st.form("marks_form"):
	st.markdown("---")
	st.write("Enter subject names (optional) and marks obtained:")
	marks = []
	subject_names = []
	cols = st.columns([3, 1])
	for i in range(1, num_subjects + 1):
		name = st.text_input(f"Subject {i} name", key=f"name_{i}")
		mark = st.number_input(
			f"Marks obtained (Subject {i})",
			min_value=0.0,
			max_value=max_marks,
			value=0.0,
			step=1.0,
			key=f"marks_{i}",
		)
		subject_names.append(name.strip())
		marks.append(float(mark))

	submitted = st.form_submit_button("Calculate")

if submitted:
	total_obtained = sum(marks)
	total_max = num_subjects * max_marks
	percentage = (total_obtained / total_max) * 100 if total_max > 0 else 0.0
	grade = get_grade(percentage)

	# Determine pass/fail: require percentage >= 40 AND each subject >= 33% of max marks
	per_subject_min = 0.33 * max_marks
	per_subject_ok = all(m >= per_subject_min for m in marks)
	overall_ok = percentage >= 40.0
	status = "Pass" if (per_subject_ok and overall_ok) else "Fail"

	st.markdown("---")
	st.subheader("Results")
	st.write("**Subject-wise marks:**")
	result_table = []
	for i, m in enumerate(marks, start=1):
		subj = subject_names[i - 1] if subject_names[i - 1] else f"Subject {i}"
		result_table.append({"Subject": subj, "Marks Obtained": m, "Max Marks": max_marks})

	st.table(result_table)

	st.metric("Total Obtained", f"{total_obtained:.2f} / {total_max:.2f}")
	st.metric("Percentage", f"{percentage:.2f}%")
	st.metric("Grade", grade)
	st.write(f"**Status:** {status}")

	if status == "Pass":
		st.success(f"Congratulations! You passed with {percentage:.2f}% and grade {grade}.")
	else:
		st.error(f"Result: {status}. Percentage: {percentage:.2f}%. Grade: {grade}.")

	# Offer a simple downloadable summary
	summary = "\n".join([
		f"{r['Subject']}: {r['Marks Obtained']}/{r['Max Marks']}" for r in result_table
	])
	summary += f"\nTotal: {total_obtained}/{total_max}\nPercentage: {percentage:.2f}%\nGrade: {grade}\nStatus: {status}"

	st.download_button("Download summary as .txt", summary, file_name="result_summary.txt")

