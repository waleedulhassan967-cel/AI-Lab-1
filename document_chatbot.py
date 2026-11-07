import json
from task2_chunks import make_chunks
from lab6_search import Retriever

def main():
    try:
        with open("corpus.json", encoding="utf-8") as f:
            docs = json.load(f)
    except FileNotFoundError:
        print("Please run create_dataset.py first to generate corpus.json!")
        return

    engine = Retriever(make_chunks(docs, "sentence"), "tfidf")
    print("Evidence Assistant (Document Retrieval Chatbot). Type 'exit' to stop.")

    while True:
        try:
            query = input("\nQuestion: ")
        except (EOFError, KeyboardInterrupt):
            break
        if query.strip().lower() == "exit":
            break
        
        hits = engine.search(query)
        if not hits:
            print("No candidate evidence found; rephrase or contact human support.")
            continue

        print("\nCandidate evidence retrieved (requires verification):")
        for number, (r, score) in enumerate(hits, 1):
            print(f"{number}. [{r['id']}] Score: {score:.3f} | Characters: {r['start']}-{r['end']}")
            print(f"   Excerpt: {r['text'][:80]}...")

        chosen = input("\nChoose candidate (1-3) to inspect complete passage (or press Enter to skip): ")
        if not chosen.isdigit() or not 1 <= int(chosen) <= len(hits):
            print("No selection made. Rephrase or contact human support.")
            continue

        r, score = hits[int(chosen) - 1]
        print("\n--- RETRIEVED EVIDENCE PASSAGE ---")
        print(f"Document ID: {r['doc']}")
        print(f"Character Offsets: {r['start']} to {r['end']}")
        print(f"Full Text:\n{r['text']}")
        print("-----------------------------------")

if __name__ == "__main__":
    main()
