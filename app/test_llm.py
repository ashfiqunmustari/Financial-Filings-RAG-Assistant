from rag import answer_question

question = input("Ask a question: ")

response = answer_question(question)

print("Answer: ")
print(response["answer"])

seen = set()

for source in response["sources"]:

    if source["section"] in seen:
        continue

    seen.add(source["section"])

    print("-" * 70)
    print("\nSources:")
    print(source["section"])
    print(f"Distance: {source['distance']:.4f}")