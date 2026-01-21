import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate



def ai_assistant(medical_history_text, question):
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