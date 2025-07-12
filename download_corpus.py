# download_corpus.py
import os
import requests

def download_file_from_google_drive(file_id, dest_path):
    URL = "https://drive.google.com/uc?export=download"

    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        response = session.get(URL, params={'id': file_id, 'confirm': token}, stream=True)

    save_response_content(response, dest_path)
    print(f"✅ 다운로드 완료: {dest_path}")

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value
    return None

def save_response_content(response, destination):
    with open(destination, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)

def ensure_corpus_downloaded():
    files = [
        {
            "file_id": "1h61BTGOSyoItcfV_3jXgqtdMffBlWL8R",
            "filename": "NYcorpus_SPOKEN_tagged.csv"
        },
        {
            "file_id": "1WnsN85iaPTBipJ047Mr2QCIgY4DhuZOV",
            "filename": "NYcorpus_WRITTEN_tagged.csv"
        }
    ]

    for f in files:
        if not os.path.exists(f["filename"]):
            print(f"📦 {f['filename']}이 존재하지 않습니다. 다운로드 시작...")
            download_file_from_google_drive(f["file_id"], f["filename"])
        else:
            print(f"✅ {f['filename']} 이미 존재함")

if __name__ == "__main__":
    ensure_corpus_downloaded()
