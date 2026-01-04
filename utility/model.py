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
    You are an expert medical assistant. You are analyzing the medical history of a patient and answer questions based on the given patient.

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

    print(result.content)


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
