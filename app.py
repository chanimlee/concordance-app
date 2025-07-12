# app.py
from flask import Flask, request, jsonify
import pandas as pd
from download_corpus import ensure_corpus_downloaded

app = Flask(__name__)

# 🧩 말뭉치 파일 존재 여부 확인 및 다운로드
ensure_corpus_downloaded()

# 🧠 말뭉치 데이터 로딩
spoken_path = "NYcorpus_SPOKEN_tagged.csv"
written_path = "NYcorpus_WRITTEN_tagged.csv"
df_spoken = pd.read_csv(spoken_path)
df_written = pd.read_csv(written_path)
print(f"📊 SPOKEN 문장 수: {len(df_spoken)}")
print(f"📊 WRITTEN 문장 수: {len(df_written)}")


@app.route("/")
def index():
    return "✅ 말뭉치 형태소 검색기 서비스 정상 작동 중입니다."

@app.route("/search", methods=["POST"])
def search_morph():
    """
    POST JSON:
    {
        "morphs": ["은/JX", "는/JX"],
        "corpus": "SPOKEN" or "WRITTEN" or "BOTH",
        "left": 10,
        "right": 10
    }
    """
    data = request.get_json()
    morphs = data.get("morphs", [])
    corpus = data.get("corpus", "BOTH")
    left = int(data.get("left", 10))
    right = int(data.get("right", 10))

    # ✅ 데이터 선택
    dfs = []
    if corpus in ["SPOKEN", "BOTH"]:
        dfs.append(df_spoken)
    if corpus in ["WRITTEN", "BOTH"]:
        dfs.append(df_written)
    if not dfs:
        return jsonify({"error": "말뭉치 선택 오류"}), 400

    df = pd.concat(dfs)

    # 🔍 형태소 검색
    results = []
    for _, row in df.iterrows():
        tagged = row['sentence_tagged']
        eojeols = tagged.split('^')[1:]

        for idx, eoj in enumerate(eojeols):
            if '|' not in eoj:
                continue
            surface, morph_str = eoj.split('|', 1)
            morphs_in_eoj = morph_str.strip().split()
            if any(m in morphs_in_eoj for m in morphs):
                left_ctx = [eu.split('|')[0] for eu in eojeols[max(0, idx-left):idx] if '|' in eu]
                right_ctx = [eu.split('|')[0] for eu in eojeols[idx+1:idx+1+right] if '|' in eu]
                results.append({
                    "category": row.get("category", ""),
                    "fname": row.get("fname", ""),
                    "좌문맥": ' '.join(left_ctx),
                    "핵심어": surface,
                    "우문맥": ' '.join(right_ctx),
                })
                break  # 문장당 1회만 수집

    print(f"✅ 검색 결과 수: {len(results)}")

    return jsonify(results)
