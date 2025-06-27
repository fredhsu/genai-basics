import faiss
from google import genai
from google.genai.types import HttpOptions
from sentence_transformers import SentenceTransformer

MODEL_NAME = "gemini-2.0-flash-001"

client = genai.Client(http_options=HttpOptions(api_version="v1"))

# Initialize embedding model and vector database
print("Loading embedding model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

with open("data.txt", "r", encoding="utf-8") as file:
    lines = [line.rstrip("\n") for line in file.readlines()]
#
# Sample knowledge base 7280 datasheet
documents = lines

# Create embeddings and add to vector database
print("Creating embeddings and building vector database...")
embeddings = embedding_model.encode(documents)
embedding_dim = embeddings.shape[1]
index = faiss.IndexFlatL2(embedding_dim)  # L2 distance for similarity
index.add(embeddings)
print(f"Added {len(documents)} documents to vector database")


def search_and_generate(query, k=2):
    """
    Search for similar documents and generate response using Gemini

    Args:
        query: User question
        k: Number of documents to retrieve
    """
    # Convert query to embedding
    query_embedding = embedding_model.encode([query])

    # Search for similar documents
    distances, indices = index.search(query_embedding, k)

    # Retrieve relevant documents
    retrieved_docs = []
    for i, idx in enumerate(indices[0]):
        if idx < len(documents):
            retrieved_docs.append(documents[idx])

    # Create context for Gemini
    context = "\n\n".join(
        [f"Document {i + 1}: {doc}" for i, doc in enumerate(retrieved_docs)]
    )

    # Generate response using Gemini
    prompt = f"""Based on the following context, answer the question. If the answer isn't in the context, say so.

Context:
{context}

Question: {query}

Answer:"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    return response.text, retrieved_docs


if __name__ == "__main__":
    queries = [
        "What accessory kits does the DCS-7280CR3K-96 come with?",
        "What accessory kits does the DCS-7280CR3A-72 come with?",
    ]

    for query in queries:
        print(f"\n🔍 Query: {query}")
        print("-" * 30)

        answer, docs = search_and_generate(query)

        print(f"🤖 Answer: {answer}")
        print(f"\n📚 Retrieved Documents:")
        for i, doc in enumerate(docs):
            print(f"  {i + 1}. {doc[:80]}...")
