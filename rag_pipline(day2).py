#creating a basic rag pipline that will extract text from a document and then give answer of query based on the text

#first creating setup
"""loader
splitter(chunker)
embedder
qdrant setup
query"""
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance,VectorParams,Filter,PointStruct

model=SentenceTransformer("all-miniLM-L6-v2")
QDRANT_URL=""
QDRANT_API_KEY=""
client=QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

#===================================================
#Step 1 loaad document
#===================================================
document=TextLoader(
    file_path="data/sample.txt",
    encoding="utf-8"
)
Document=document.load()

#===================================================
#step 2 splitting
#===================================================
splitter=RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks=splitter.split_documents(Document)
print(chunks[0].page_content[:80])

#===================================================
#step 3 creating embeddings
#===================================================

#getting the list of chunks data so we can create embeddings for it
chunks_text=[chunk.page_content  for chunk in chunks]
chunks_embeddings=model.encode(chunks_text)

print(chunks_embeddings[0][:5])

#===================================================
#step 4 vector data sending vectors and metadata on it
#===================================================
#crating collection inside vector store
client.create_collection(
    collection_name="Personal_data",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)
#now we will store vectors in the collection
points=[]
for ind,(text,embeddings) in enumerate(zip(chunks_text,chunks_embeddings)):
    point=PointStruct(
        id=ind,
        vector=embeddings.tolist(),
        payload={
            "chunk_id":(id+1),
            "source": "sample.txt"
        }
    )
    points.append(point)

client.upsert(
    collection_name="Personal_data",
    points=points
)
#===================================================
#step 5 query
#===================================================
query="what do you mean by nlp?"
query_embed=model.encode(query)

result=client.query_points(
    collection_name="Personal_data",
    query=query_embed,
    limit=3
).points

for i,ans in enumerate(result):
    print(f"Rank:{i+1}: answer:{ans}")


