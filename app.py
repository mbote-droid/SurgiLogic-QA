import streamlit as st

# --- Logic Engine ---
def analyze_surgical_patient(name, pod, temp_str, hr_str):
    risks = []
    try:
        # Convert strings to floats to prevent crashes from manual typing
        temp = float(temp_str)
        hr = int(hr_str)
        
        # Clinical Logic based on Post-Op Day (POD)
        if temp > 38.0:
            if pod <= 2:
                risks.append("⚠️ **Potential Atelectasis/Pneumonia** (Early POD Fever)")
            elif 3 <= pod <= 5:
                risks.append("⚠️ **Potential UTI or Thrombophlebitis** (Mid POD Fever)")
            else:
                risks.append("🚨 **Potential SSI or Deep Abscess** (Late POD Fever)")

        if hr > 100:
            risks.append("⚠️ **Tachycardia**: Evaluate for Pain, PE, or Hypovolemia.")

        if not risks:
            return "✅ Patient is stable. Continue routine monitoring.", "success"
        return " | ".join(risks), "warning"

    except ValueError:
        return "❌ **Error**: Please enter valid numbers for Temperature and Heart Rate.", "error"

# --- Streamlit Web Interface ---
st.title("🩺 SurgiLogic: Surgical Post-Op Decision Support")
st.write("A clinical reasoning tool for General Surgery Residents.")

with st.form("patient_form"):
    name = st.text_input("Patient Initials/ID")
    pod = st.slider("Post-Op Day (POD)", 0, 30, 1)
    temp_input = st.text_input("Temperature (°C)", placeholder="e.g. 38.5")
    hr_input = st.text_input("Heart Rate (BPM)", placeholder="e.g. 110")
    
    submitted = st.form_submit_button("Analyze Patient")
    
    if submitted:
        result, status = analyze_surgical_patient(name, pod, temp_input, hr_input)
        if status == "success":
            st.success(result)
        elif status == "warning":
            st.warning(result)
        else:
            st.error(result)

st.info("Built by a General Surgery Resident & IBM Certified Data Scientist.")
