from retrieval import retrieve
from llm import generate_answer


def answer_question(question):

    results = retrieve(question)
    if not results:
        return {
            "question": question,
            "answer": "I couldn't find that information in the filing.",
            "sources": []
        }

    context = "\n\n".join(
        f"Section: {result['section']}\n\n{result['text']}"
        for result in results
    )

    answer = generate_answer(
        question,
        context
    )

    return {
        "question": question,
        "answer": answer,
        "sources": [
            {
                "company": result["company"],
                "section": result["section"],
                "chunk_id": result["chunk_id"],
                "distance": result["distance"]
            }
            for result in results
        ]
    }