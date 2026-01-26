import os
import pandas as pd
import requests
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

API_URL = "http://app:5000/ask"
DATA_PATH = "dataset.json"

df_gabarito = pd.read_json(DATA_PATH)
results = []

print("🎯 Coletando respostas da API com Re-ranker...")
for _, row in df_gabarito.iterrows():
    resp = requests.post(API_URL, json={"input_text": row['question']})
    data = resp.json()
    results.append({
        "question": row['question'],
        "answer": data.get("resposta", ""),
        "contexts": data.get("contextos", []),
        "ground_truth": row['answer']
    })

dataset = Dataset.from_pandas(pd.DataFrame(results))
result = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    embeddings=OpenAIEmbeddings()
)

final_df = result.to_pandas()
final_df.to_csv("re.csv", index=False)

# Print seguro (independente do nome da coluna de input do Ragas)
cols = [c for c in ['user_input', 'question', 'faithfulness', 'context_recall'] if c in final_df.columns]
print("\n📊 RESULTADOS FINAIS:\n", final_df[cols])
