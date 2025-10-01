import os
import torch
import numpy as np
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import hashlib
from datetime import datetime
from typing import List, Dict
from tqdm import tqdm

os.environ["OMP_NUM_THREADS"] = "12"
os.environ["MKL_NUM_THREADS"] = "12"

class AMDOptimizedKnowledgeBase:
    def __init__(self, use_gpu=True):
        print("🚀 AMD Optimizeli Sistem Başlatılıyor...")
        self.model = SentenceTransformer("BAAI/bge-small-en-v1.5")
        self.qdrant = QdrantClient(path="./qdrant_data")
        self.collection_name = "research_docs"
        self._setup_collection()
    
    def _setup_collection(self):
        try:
            self.qdrant.delete_collection(self.collection_name)
        except:
            pass
        self.qdrant.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )
    
    def search_semantic(self, keyword1, keyword2, max_results=10):
        query = f"{keyword1} {keyword2}"
        query_embedding = self.model.encode(query)
        results = self.qdrant.search(
            collection_name=self.collection_name,
            query_vector=query_embedding.tolist(),
            limit=max_results
        )
        return results
