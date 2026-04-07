import streamlit as st

# --- Logic Engine ---
def analyze_surgical_patient(name, pod, temp_str, hr_str):
    risks = []
    try:
        # Convert strings to numbers
        temp = float(temp_str)
        hr = int(hr_str)
        
        # Apply “5 W’s” Post-Op Fever Logic
        if temp > 38.0:
            if pod <= 2:
                risks.append("Potential **Respiratory Complications** (Wind): Atelectasis or Pneumonia")
            elif 3 <= pod <= 5:
                risks.append("Potential **Urinary Tract Infection (UTI)** (Water), often associated with Foley catheter")
            elif 4 <= pod <= 6:
                risks.append("Potential **Venous Thromboembolism (VTE)** (Walking): DVT or Pulmonary Embolism")
            elif 5 <= pod <= 7:
                risks.append("Potential **Surgical Site Infection (SSI)** or deep wound infection (Wound)")
            elif pod >= 7:
                risks.append("Potential **Drug-Related Fever or Line Infection/Thrombophlebitis** (Wonder/Drugs)")

        # Add tachycardia warning
        if hr > 100:
            risks.append("Tachycardia: Evaluate for Pain, PE, Hypovolemia, or sepsis")

        # Special note for immediate post-op fever (<24h)
        if pod == 0 and temp > 38.0:
            risks.append("Immediate post-op fever (<24h) likely due to tissue trauma or pre-existing infection")

        if not risks:
            return "✅ **Patient Status:** Stable\n\nContinue routine post-operative monitoring.", "success"

        # Format output with bullets and clinical note
        formatted_output = "⚠️ **Clinical Assessment:**\n\n"
        for risk in risks:
            formatted_output += f"- {risk}\n"
        formatted_output += "\n**Note:** Correlate clinically with patient symptoms, labs, and imaging."

        return formatted_output, "warning"

    except ValueError:
        return "❌ **Error**: Please enter valid numbers for Temperature and Heart Rate.", "error"

# --- Streamlit Web Interface ---
st.title("🩺 SurgiLogic: Surgical Post-Op Decision Support")

st.write(
    "A clinical decision support tool designed to assist in evaluating post-operative fever "
    "using the '5 W's' framework (Wind, Water, Walking, Wound, Wonder/Drugs)."
)

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

st.info(
    "Developed by a Medical Doctor using standard clinical reasoning frameworks for "
    "post-operative patient assessment. For educational and decision-support purposes only."
)
