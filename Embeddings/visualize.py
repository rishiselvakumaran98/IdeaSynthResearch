import os
import json
from glob import glob
from typing import List, Dict
import re

import numpy as np
from openai import AzureOpenAI
from dotenv import load_dotenv
import tiktoken

import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from umap import UMAP


def read_folder_texts(folder: str) -> Dict[str, str]:
    texts = {}
    for path in sorted(glob(os.path.join(folder, "*.txt"))):
        name = os.path.basename(path)
        with open(path, "r", encoding="utf-8") as f:
            texts[name] = f.read().strip()
    return texts


def concatenate_texts(texts: List[str]) -> str:
    return "\n\n".join(texts)


def count_tokens(text: str, model_name: str) -> int:
    enc = tiktoken.encoding_for_model(model_name)
    return len(enc.encode(text))


def select_within_token_budget(
    segments: List[str],
    model_name: str,
    max_tokens: int = 8000
) -> List[str]:
    selected, total = [], 0
    for seg in segments:
        toks = count_tokens(seg, model_name)
        if total + toks > max_tokens:
            break
        selected.append(seg)
        total += toks
    return selected


def get_embeddings(client: AzureOpenAI, texts: List[str], model_env_var: str) -> np.ndarray:
    resp = client.embeddings.create(
        input=texts,
        model=os.getenv(model_env_var)
    )
    return np.array([d.embedding for d in resp.data])


def extract_facets(
    client: AzureOpenAI,
    full_text: str,
    facets: List[str],
    system_prompt: str,
    llm_model_env: str,
    embed_model_env: str
) -> Dict[str, Dict]:
    # force pure JSON
    user_msg = (
        f"You will be given the full text of one paper.  "
        f"Respond *only* with a JSON object whose keys are exactly {facets!r} "
        f"and values are one‐paragraph summaries.\n\n"
        f"{full_text}"
    )
    chat = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_msg}
        ],
        model=os.getenv(llm_model_env)
    )
    raw = chat.choices[0].message.content.strip()
    m = re.search(r"(\{.*\})", raw, re.S)
    if not m:
        raise ValueError(f"No JSON found in response:\n{raw}")
    js = m.group(1)
    try:
        facet_texts = json.loads(js)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON parse error {e}:\n{js}")

    texts = [facet_texts[f] for f in facets]
    embs = get_embeddings(client, texts, embed_model_env)
    return {f: {"text": facet_texts[f], "embedding": embs[i]} for i, f in enumerate(facets)}


def save_embeddings(embs: np.ndarray, labels: List[str], prefix: str, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    np.save(os.path.join(out_dir, f"{prefix}_emb.npy"), embs)
    with open(os.path.join(out_dir, f"{prefix}_labels.json"), "w") as f:
        json.dump(labels, f, indent=2)
    print(f"→ saved {prefix} embeddings in {out_dir}")

def _scatter_and_save(reduced: np.ndarray, labels: List[str], method: str, out_dir: str):
    plt.figure(figsize=(8, 6))
    for (x, y), lbl in zip(reduced, labels):
        plt.scatter(x, y, s=20)
        plt.text(x + 0.01, y + 0.01, lbl, fontsize=8)
    plt.title(f"{method}")
    plt.tight_layout()
    path = os.path.join(out_dir, f"{method.lower()}.png")
    plt.savefig(path, dpi=300)
    plt.close()
    print(f"→ {method} plot → {path}")


def plot_all(embs: np.ndarray, labels: List[str], out_dir: str):
    os.makedirs(out_dir, exist_ok=True)

    # PCA
    pca_red = PCA(n_components=2, random_state=42).fit_transform(embs)
    _scatter_and_save(pca_red, labels, "PCA", out_dir)

    # t-SNE
    perp = max(2, min(30, len(labels)-1))
    tsne_red = TSNE(
        n_components=2,
        perplexity=perp,
        init="random",
        early_exaggeration=6.0,
        learning_rate="auto",
        random_state=42
    ).fit_transform(embs)
    _scatter_and_save(tsne_red, labels, "t-SNE", out_dir)

    # UMAP — use keyword for n_components
    nbrs = max(2, min(30, len(labels)-1))
    umap_red = UMAP(
        n_components=2,       # <-- explicitly name this
        n_neighbors=nbrs,
        min_dist=0.01,
        metric="cosine",
        random_state=42
    ).fit_transform(embs)
    _scatter_and_save(umap_red, labels, "UMAP", out_dir)


def main():
    load_dotenv()
    client = AzureOpenAI(
        api_version="2024-12-01-preview",
        azure_endpoint=os.getenv("AZURE_EMBEDDING_ENDPOINT"),
        api_key=os.getenv("AZURE_EMBEDDING_API_KEY")
    )
    embed_model = os.getenv("AZURE_EMBEDDING_MODEL")

    facets = [
        "Problem Description and RQ",
        "Proposed Design and Solution",
        "Evaluation Method",
        "Contribution and Impact",
        "Limitation and Future Work"
    ]

    all_facet_embs = []
    all_facet_labels = []

    # iterate over each paper‐folder
    for idx, fld in enumerate(sorted(glob("./outputs/*_sections")) , start=1):
        paper_id = f"Paper{idx}"
        print(f"\n--- Processing {paper_id}: {fld} ---")

        texts = read_folder_texts(fld)
        segs = [texts[os.path.basename(p)] for p in sorted(glob(os.path.join(fld, "*.txt")))]
        kept = select_within_token_budget(segs, embed_model, 8000)
        full = concatenate_texts(kept)
        print(f"Kept {len(kept)}/{len(segs)} sections ({count_tokens(full,embed_model)} tokens)")

        # extract facets for this single paper
        res = extract_facets(
            client=client,
            full_text=full,
            facets=facets,
            system_prompt="You are an academic-paper extractor.",
            llm_model_env="AZURE_OPENAI_DEPLOYMENT",
            embed_model_env="AZURE_EMBEDDING_MODEL"
        )

        # collect embeddings & labels, prefixing with paper id
        for f in facets:
            emb = res[f]["embedding"]
            lbl = f"{paper_id}: {f}"
            all_facet_embs.append(emb)
            all_facet_labels.append(lbl)

        # save per‐paper facets if desired
        paper_embs = np.vstack([res[f]["embedding"] for f in facets])
        paper_labels = [f"{f}" for f in facets]
        save_embeddings(paper_embs, paper_labels, f"{paper_id}_facets", f"./embeddings/{paper_id}")

    E = np.vstack(all_facet_embs)
    L = all_facet_labels
    plot_all(E, L, out_dir="./plots/facets")


if __name__ == "__main__":
    main()
