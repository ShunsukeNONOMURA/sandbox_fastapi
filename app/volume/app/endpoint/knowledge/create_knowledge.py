from app.endpoint.knowledge.router import router
from app.infrastructure.database.db import get_session

from fastapi import Depends
from sqlmodel import Session

# ========== 埋め込み関数 ==========
from ollama import Client
OLLAMA_URL = "http://host.docker.internal:11434"
OLLAMA_EMMBEDDING_MODEL = "zylonai/multilingual-e5-large:latest"
OLLAMA_LLM_MODEL = "llama3:latest"
def get_embedding(text: str):
    # ollamaクライアント
    client = Client(host=OLLAMA_URL)
    # emb実行
    result = client.embed(model=OLLAMA_EMMBEDDING_MODEL, input=text)
    return result

# ========== 簡易グラフ変換関数 ==========
import json
def get_graph_by_manual(text: str):
    """
    非LLMなルールベース処理。
    例文：「田中さんはABC株式会社でエンジニアをしています。」
    """
    if "は" in text and "で" in text:
        person = text.split("は")[0].strip()
        company = text.split("は")[-1].split("で")[0].strip()
        role = text.split("で")[-1].replace("をしています", "").replace("として働いています", "").strip("。")
        return {"person": person, "company": company, "role": role}
    return None

def get_graph_by_ollama(text: str):
    prompt = f"""
あなたは自然文を構造化するAIアシスタントです。
以下の日本語文を、グラフ構造としてノードとリレーションに分解してください。

出力形式は JSON としてください。形式は以下の通りです。
**必ずこの形式で返してください。余計な文章や説明は一切入れないでください。**

{{
  "nodes": [{{"id": "名前", "label": "ラベル"}}],
  "relationships": [{{"from": "ノードID", "to": "ノードID", "type": "リレーションタイプ", "properties": {{}} }}]
}}

入力文：
{text}
"""
    # ollamaクライアント
    client = Client(host=OLLAMA_URL)
    response = client.generate(
        model=OLLAMA_LLM_MODEL,
        prompt=prompt
    )

    print(response['response'])
    # 応答を JSON にパース
    try:
        result = json.loads(response['response'])
        
    except json.JSONDecodeError:
        raise ValueError("Ollamaからの応答をJSONとして解析できませんでした:\n" + response['response'])

    return result

# neo4j登録
from neo4j import GraphDatabase
NEO4J_URI = "bolt://search:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "password"

def register_graph(graph_data, text, embedding):
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
    with driver.session() as session:
        for node in graph_data.get("nodes", []):
            props = {
                "id": node["id"],
                "text": text,
                "embedding": embedding,
            }
            label = node.get("label", "Entity")
            session.run(
                f"""
                MERGE (n:{label} {{id: $id}})
                SET n.text = $text,
                    n.embedding = $embedding
                """,
                **props
            )

        for rel in graph_data.get("relationships", []):
            session.run(
                f"""
                MATCH (a {{id: $_from}})
                MATCH (b {{id: $to}})
                MERGE (a)-[r:{rel["type"]}]->(b)
                SET r += $props
                """,
                _from=rel["from"],
                to=rel["to"],
                props=rel.get("properties", {})
            )

from sqlmodel import SQLModel
class CreateKnowledgeRequest(SQLModel):
    text: str

@router.post(
    "/knowledges"
)
async def create_knowledge(
    request: CreateKnowledgeRequest,
    session: Session = Depends(get_session),
):
    text = request.text
    print(text)
    embedding = get_embedding(text)['embeddings'][0]
    graph = get_graph_by_ollama(text)
    # person, company, role = graph["person"], graph["company"], graph["role"]

    # 3. Neo4j にノード＋リレーション登録
    register_graph(graph, text, embedding)


    return {
        "graph": graph, 
        "text": text,
        # "neo4j": {
        #     "person": person,
        #     "company": company,
        #     "role": role
        # },
        "embedding": embedding,
    }
