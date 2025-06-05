from app.endpoint.knowledge.router import router
from app.infrastructure.database.db import get_session

from fastapi import Depends
from sqlmodel import Session


# neo4j登録
from neo4j import GraphDatabase
NEO4J_URI = "bolt://search:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "password"

def register_graph(graph_data, text, embedding):
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))


from pydantic import BaseModel
class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


@router.post(
    "/knowledges:search"
)
async def search_knowledge(
    req: SearchRequest,
    session: Session = Depends(get_session),
):
    query = req.query
    from .create_knowledge import get_embedding
    embedding = get_embedding(query)['embeddings'][0]
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
    with driver.session() as session:
        results = []

        # 🔍 1. 全文検索（text CONTAINS）
        text_results = session.run(
            """
            MATCH (n)
            WHERE toLower(n.text) CONTAINS toLower($query)
            RETURN n LIMIT $k
            """, 
            {"query": query, "k": req.top_k}
            # query=query, k=req.top_k
        )
        results.extend([r["n"] for r in text_results])

        # 📐 2. ベクトル検索（Neo4j 5.11+）
        # WITH n, vector.similarity.cosine(n.embedding, $embedding) AS score
        vector_results = session.run(
            """
            MATCH (n)
            WHERE n.embedding IS NOT NULL
            WITH n, vector.similarity.cosine(n.embedding, $embedding) AS score
            RETURN n ORDER BY score DESC LIMIT $k
            """,
            {"embedding": embedding, "k": req.top_k} 
            # embedding=embedding, k=req.top_k
        )
        results.extend([r["n"] for r in vector_results])

        # 🧠 3. グラフ構造探索（全文一致とリレーション）
        graph_results = session.run(
            """
            MATCH (a)-[r]-(b)
            WHERE toLower(a.text) CONTAINS toLower($query)
               OR toLower(b.text) CONTAINS toLower($query)
            RETURN a, r, b LIMIT $k
            """, 
            {"query": query, "k": req.top_k}
            # query=query, k=req.top_k
        )
        for r in graph_results:
            results.extend([r["a"], r["b"]])

        # ✅ 重複除去して返却（idベース）
        seen = set()
        deduped = []
        for node in results:
            node_id = node.get("id")
            if node_id and node_id not in seen:
                seen.add(node_id)
                deduped.append({
                    "id": node.get("id"),
                    "label": list(node.labels)[0] if node.labels else "Entity",
                    "text": node.get("text"),
                    # "embedding": node.get("embedding"),
                    # "score": score,
                })

        return {"results": deduped}
