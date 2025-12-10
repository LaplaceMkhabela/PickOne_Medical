import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

with open("patient.txt","r") as file:
    medical_history_text = file.read()

def ai_summary(medical_history_text):
    model = ChatGroq(
        model= "llama-3.3-70b-versatile",
        temperature=0,
        api_key= "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"
    )


    template = """
    You are an expert medical assistant. You are analyzing the medical history of a patient and answer questions based on the given patient.

    Here are the patient's records:
    {records}

    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    question_to_ask ="Generate a brief summary of the patient's medical history for the doctor to review for current conditions."

    result = chain.invoke({
        "records": medical_history_text,
        "question": question_to_ask
    })

    return result.content






def ai_assistant(medical_history_text):
    model = ChatGroq(
        model= "llama-3.3-70b-versatile",
        temperature=0,
        api_key= "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"
    )


    template = """
    You are an expert medical assistant. You are analyzing the medical history of a patient and answer questions based on the given patient.

    Here are the patient's records:
    {records}

    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    while True:
        print("\n\n-------------------------------")
        question_to_ask = input("ask your question (q to quit): ")
        print("\n\n-------------------------------")
        if question_to_ask == "q":
            break

        result = chain.invoke({
            "records": medical_history_text,
            "question": question_to_ask
        })

        print(result.content)


if __name__ == "__main__":
    print("\n\n-------------------------------")
    print(ai_summary(medical_history_text))
    print("\n\n-------------------------------")
    ai_assistant(medical_history_text)