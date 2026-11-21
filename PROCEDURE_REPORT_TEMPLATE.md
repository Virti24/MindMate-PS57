# Procedure Report – PS 57: Mental Wellness Journal Companion

**Name:** [Your name]  
**Roll Number:** [Your roll number]  
**Class/Division:** [Your class]  
**GitHub Link:** [Add after creating repository]

## 1. Problem Statement
Students may experience stress but often do not take time to reflect on their feelings. The Mental Wellness Journal Companion provides a simple journal interface, supportive AI-generated reflections, approximate mood labels, and helpline information when selected distress-related language is detected.

## 2. Tools and Model
- Language: Python
- UI: Streamlit
- LLM: Gemini 2.5 Flash through Google GenAI API
- Supporting libraries: Streamlit, google-genai, json, datetime, pathlib
- Storage: Local JSON file

## 3. Procedure
1. Created a Python project folder and installed the required packages using `pip install -r requirements.txt`.
2. Obtained a Gemini API key and configured it as the `GEMINI_API_KEY` environment variable. The key is not included in the source code or GitHub repository.
3. Designed a system prompt instructing the model to respond empathetically, avoid diagnosis, keep responses concise, and encourage human support when distress is indicated.
4. Developed `ai_helper.py` to send the journal entry and mood context to Gemini and provide a safe fallback response if the API is unavailable.
5. Developed `journal.py` to estimate mood using simple keyword matching, flag selected distress-related terms, and save/retrieve entries from a local JSON file.
6. Developed `app.py` using Streamlit to provide journal input, AI responses, mood display, distress support information, and journal history.
7. Tested the application with sample journal entries representing positive mood, sadness, stress, anxiety, and distress-related wording. Recorded screenshots of the working application.

## 4. Prompt Used
“You are MindMate, a warm, calm, non-judgmental journaling companion for students. Acknowledge feelings without judging. Do not diagnose or prescribe treatment. Offer one or two gentle reflection questions or realistic coping ideas. If the entry suggests self-harm, suicide, abuse, or immediate danger, encourage immediate human support and display relevant support contacts. Keep the response concise.”

**Prompt improvement:** Added explicit instructions not to diagnose or minimise feelings, and to encourage immediate human support when safety concerns appear.

## 5. Results
The application accepts journal entries, estimates a mood, generates a supportive response, and saves the entry for later viewing. Add 1–2 genuine screenshots of your running application here before submission.

## 6. Challenges
Possible API connectivity or quota errors are handled using a local fallback response. The API key is stored outside the source code. Keyword-based mood and distress detection is approximate and may not understand every context.

## 7. Conclusion
The prototype demonstrates a basic LLM-powered journaling companion with a simple interface and local history. It does not provide diagnosis or professional care. A future improvement would be more reliable context-aware distress detection, stronger privacy controls, and optional export of journal entries.

**Important:** Edit this report so it accurately describes what you personally ran and tested. Insert your own screenshots and GitHub URL before exporting it as a two-page PDF.
