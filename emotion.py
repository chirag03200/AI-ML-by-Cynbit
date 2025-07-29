{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "8f3353ce-82a1-41bc-8950-5fa10cafd9f0",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-07-28 09:47:19.971 WARNING streamlit.runtime.scriptrunner_utils.script_run_context: Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-07-28 09:47:22.964 \n",
      "  \u001b[33m\u001b[1mWarning:\u001b[0m to view this Streamlit app on a browser, run it with the following\n",
      "  command:\n",
      "\n",
      "    streamlit run C:\\ProgramData\\anaconda3\\Lib\\site-packages\\ipykernel_launcher.py [ARGUMENTS]\n",
      "2025-07-28 09:47:22.966 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-07-28 09:47:22.970 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-07-28 09:47:22.973 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-07-28 09:47:22.976 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-07-28 09:47:22.980 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-07-28 09:47:22.983 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-07-28 09:47:22.986 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-07-28 09:47:22.989 Session state does not function when running a script without `streamlit run`\n",
      "2025-07-28 09:47:22.993 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-07-28 09:47:22.995 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-07-28 09:47:22.999 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-07-28 09:47:23.002 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-07-28 09:47:23.005 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-07-28 09:47:23.008 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2025-07-28 09:47:23.010 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    }
   ],
   "source": [
    "# app.py\n",
    "import streamlit as st\n",
    "import joblib\n",
    "import pandas as pd\n",
    "\n",
    "# Load model\n",
    "model = joblib.load(\"emotion_model.pkl\")\n",
    "\n",
    "# Emoji map\n",
    "emojis = {\n",
    "    \"joy\": \"😄\", \"anger\": \"😠\", \"sadness\": \"😢\",\n",
    "    \"fear\": \"😨\", \"love\": \"❤️\", \"surprise\": \"😲\"\n",
    "}\n",
    "\n",
    "st.title(\"🧠 Emotion Detection App\")\n",
    "st.write(\"Enter a sentence to detect the emotion:\")\n",
    "\n",
    "# Input\n",
    "text_input = st.text_input(\"Your Text\")\n",
    "\n",
    "if st.button(\"Detect Emotion\"):\n",
    "    if text_input:\n",
    "        prediction = model.predict([text_input])[0]\n",
    "        probs = model.predict_proba([text_input])[0]\n",
    "        \n",
    "        st.markdown(f\"### Emotion: **{prediction.capitalize()}** {emojis.get(prediction)}\")\n",
    "\n",
    "        # Show probability chart\n",
    "        prob_df = pd.DataFrame({'Emotion': model.classes_, 'Probability': probs})\n",
    "        st.bar_chart(prob_df.set_index(\"Emotion\"))\n",
    "    else:\n",
    "        st.warning(\"⛔ Please enter text to detect emotion.\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b19a4411-cbbf-459b-a0b6-a77288c7334f",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
