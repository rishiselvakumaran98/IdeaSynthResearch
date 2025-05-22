import os
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import numpy as np
load_dotenv()

client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint=os.getenv("AZURE_EMBEDDING_ENDPOINT"),
    api_key=os.getenv("AZURE_EMBEDDING_API_KEY")
)

response = client.embeddings.create(
    input=["first phrase","second phrase","third phrase"],
    model=os.getenv("AZURE_EMBEDDING_MODEL")
)

for item in response.data:
    length = len(item.embedding)
    print(
        f"data[{item.index}]: length={length}, "
        f"[{item.embedding[0]}, {item.embedding[1]}, "
        f"..., {item.embedding[length-2]}, {item.embedding[length-1]}]"
    )

similarity_matrix = np.zeros((3, 3))

for i, item1 in enumerate(response.data):
    for j, item2 in enumerate(response.data):
        similarity_matrix[i, j] = np.dot(item1.embedding, item2.embedding)

print(similarity_matrix)

print(response.usage)