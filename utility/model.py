import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


def ai_summary(medical_history_text):
    model = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key="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"
    )

    template = """
You are an expert medical assistant tasked with analyzing a patient’s medical history.

Your response will be evaluated automatically.
You must therefore follow all instructions exactly.

General Rules:

- Use only information explicitly provided in the input.
- Do not infer, assume, or hallucinate any medical facts.
- If a data element is missing, output exactly: Not provided
- Do not add extra sections, explanations, or commentary.
- Maintain a clinical, concise, neutral tone.
- Use plain text only (no markdown symbols beyond the required headings).
- Follow the exact section order, wording, and bullet structure below.

Required Output Structure:

1. Safety Scan

Allergies:
- (List allergies separated by commas OR write Not provided)
Current Medications:
- (List medications separated by commas OR write Not provided)

************************************************

2. Problem List

Chronic Conditions:
- (List conditions separated by commas OR write Not provided)
Past Surgeries / Procedures:
- (List surgeries/procedures separated by commas OR write Not provided)

************************************************

3. Clinical Story (Recent Trajectory)

Recent Hospitalizations or Emergency Department Visits:
- (Summarize concisely OR write Not provided)
Laboratory Trends:
- (Describe trends if available OR write Not provided)
Most Recent Assessment and Plan:
- (Summarize the latest assessment and plan OR write Not provided)

Validation Constraints:

- Every bullet must be present, even if the value is Not provided
- Do not repeat information across sections
- Do not include speculative language (e.g., “likely,” “possibly,” “suggests”)
- Output must be fully self-contained
    
    Here are the patient's records:
    {records}

    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    question_to_ask = "Generate a brief summary of the patient's medical history for the doctor to review for current conditions."

    result = chain.invoke({
        "records": medical_history_text,
        "question": question_to_ask
    })

    return result.content





def ai_assistant(medical_history_text, question):
    model = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key="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"
    )

    template = """
    You are an expert medical assistant. You are analyzing the medical history of a patient and answer questions based on the given patient.
    Instruction:
    -Answer in 1-2 sentences only.
    -Your answers should Be direct and factual.
    -No explanations, examples, or emojis unless asked.


    Here are the patient's records:
    {records}

    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    result = chain.invoke({
        "records": medical_history_text,
        "question": question
    })

    return result.content






def html_parser(text):
    model = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key="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"
    )

    template = """
    You are an expert markdown to html parser.
    return the expected output only
    return No record found if the input is empty
    Here is the text:
    {text}

    """

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    result = chain.invoke({
        "text": text
    })

    return result.content




# The function for AI notes
def ai_notes(medical_history_text, question):
    model = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key="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"
    )

    template = """
    You are an expert medical assistant. You are analyzing the conversation of a doctor and their patient 
    and provide notes based on the conversation which can be used for future consultations as part of the 
    patient's medical history.

    Instruction:
    - Do not make up any information.
    - Use only information explicitly provided in the input.
    - Do not infer, assume, or hallucinate any medical facts.
    - Do not add extra sections, explanations, or commentary.
    - Maintain a clinical, concise, neutral tone.
    - Use plain text only.
    - Your reply must be a short informative note.

    Here are the patient's records:
    {records}

    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    result = chain.invoke({
        "records": medical_history_text,
        "question": question
    })

    return result.content




# The function that check for conflicts in doctor's prescription and patient's medical history
def ai_conflict_checker(medical_history_text, question):
    model = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key="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"
    )

    template = """
    You are an expert medical assistant. You are analyzing the doctor's diagnosis 
    and also their prescription suggestion then check if is not in conflict with 
    the patient's medical history.

    Instruction:
    - Do not make up any information.
    - Only raise warning if there is a conflict.
    - If there is no conflict, explicitly reply with the words "Approved"

    Here are the patient's records:
    {records}

    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    result = chain.invoke({
        "records": medical_history_text,
        "question": question
    })

    return result.content