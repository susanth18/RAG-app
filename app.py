from flask import Flask, request, render_template, jsonify
import os
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
from dotenv import load_dotenv
import pymysql
from contextlib import closing


load_dotenv()

app = Flask(__name__)


app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")

pinecone = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
together_client = OpenAI(
  api_key=os.getenv("TOGETHER_API_KEY"),
  base_url=os.getenv("TOGETHER_BASE_URL"),
)
index = pinecone.Index("assignment")

def get_db_connection():
    try:
        return pymysql.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB'],
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.MySQLError as e:
        raise Exception(f"Database connection error: {e}")

    
def log_message(role, content):
    with closing(get_db_connection()) as connection:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO chat_history (role, content)
                VALUES (%s, %s)
            """
            cursor.execute(sql, (role, content))
            connection.commit()


def get_embedding(text):
    return together_client.embeddings.create(
        input=[text],
        model="togethercomputer/m2-bert-80M-32k-retrieval"
    ).data[0].embedding

def rag_query(question, top_k=3):
    query_embedding = get_embedding(question)
    
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )
    
    context = "\n\n".join([match.metadata["text"] for match in results.matches])
    
    response = together_client.chat.completions.create(
        model="meta-llama/Meta-Llama-3-70B-Instruct-Turbo",
        messages=[
            {"role": "system", "content": f"Answer the question based on this context:\n\n{context}"},
            {"role": "user", "content": question}
        ]
    )
    
    return {
        "answer": response.choices[0].message.content,
        "sources": [{"source": match.metadata["source"], "chunk": match.metadata["chunk_number"]} 
                   for match in results.matches]
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question', '')
    
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    try:
        log_message('user', question)        
        result = rag_query(question)
        log_message('system', result['answer'])
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)