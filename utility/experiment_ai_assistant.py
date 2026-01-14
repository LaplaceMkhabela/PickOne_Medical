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
    You are an expert medical assistant. You are analyzing the medical history of a patient and answer questions based on the given patient.
    Instruction:
    -Answer in 1–2 sentences only.
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