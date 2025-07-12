# download_corpus.py
import os
import gdown

def ensure_corpus_downloaded():
    files = [
        {
            "url": "https://drive.google.com/uc?id=1h61BTGOSyoItcfV_3jXgqtdMffBlWL8R",
            "filename": "NYcorpus_SPOKEN_tagged.csv"
        },
        {
            "url": "https://drive.google.com/uc?id=1WnsN85iaPTBipJ047Mr2QCIgY4DhuZOV",
            "filename": "NYcorpus_WRITTEN_tagged.csv"
        }
    ]

    for f in files:
        if not os.path.exists(f["filename"]):
            print(f"📦 {f['filename']}이 존재하지 않습니다. 다운로드 시작...")
            gdown.download(f["url"], f["filename"], quiet=False)
        else:
            print(f"✅ {f['filename']} 이미 존재함")

if __name__ == "__main__":
    ensure_corpus_downloaded()
