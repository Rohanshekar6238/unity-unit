from flask import Flask, request, jsonify
import google.generativeai as genai
import gradio as gr

# Configure API key securely (store in environment variable for security)
GOOGLE_API_KEY = "AIzaSyBXvRTEuuCT5iiGtTYYgjI5djv867QU-cE"
genai.configure(api_key=GOOGLE_API_KEY)

app = Flask(__name__)

# Function to get medication advice with structured formatting
def get_medication_advice(symptom):
    """
    Given a symptom, this function queries Gemini AI for:
    - Medications (generic & brand names)
    - Side effects
    - Possible allergies
    - Home remedies
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            f"Symptom: {symptom}\n"
            "Provide the following details in a well-structured format:\n\n"
            "**Medications & Treatments**\n\n"
            "**Medication Name:** (Generic & Brand Name)\n"
            "**Side Effects:** (Common adverse effects)\n"
            "**Possible Allergies:** (Potential allergic reactions)\n"
            "**Home Remedies:** (Natural remedies)\n\n"
            "Ensure that each section is properly formatted and easy to read."
        )
        response = model.generate_content(prompt)
        return response.text if response.text else "No relevant information found."
    except Exception as e:
        return f"API Error: {e}"

@app.route('/check_symptom', methods=['POST'])
def check_symptom():
    data = request.json
    symptom = data.get('symptom', '')
    
    if not symptom:
        return jsonify({'error': 'No symptom provided'}), 400
    
    advice = get_medication_advice(symptom)
    return jsonify({'response': advice})

# Create chatbot UI without the flag button
iface = gr.Interface(
    fn=get_medication_advice,
    inputs=gr.Textbox(label="Enter your symptom"),
    outputs=gr.Markdown(),
    title="CareWise: AI Symptom Checker and Treatment Advisor",
    #description="Enter a symptom and get AI-generated medication suggestions, side effects, allergies, and home remedies.",
    allow_flagging="never"  # Removes flag button
)

if __name__ == '__main__':
    iface.launch()  # Launch Gradio interface
    app.run(debug=True)