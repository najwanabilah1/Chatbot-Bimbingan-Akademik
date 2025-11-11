import os
import pandas as pd
from backend.config import app, db
from backend.db.models import Dataset, Peraturan

# Folder upload
DATASET_PATH = os.path.join("backend", "uploads", "datasets")
TEXT_PATH = os.path.join("backend", "uploads", "texts")

def load_dataset_to_db():
    dataset_files = [f for f in os.listdir(DATASET_PATH) if f.endswith(".csv")]
    if not dataset_files:
        raise FileNotFoundError("❌ Tidak ada file CSV di uploads/datasets/")
    
    dataset_file = os.path.join(DATASET_PATH, dataset_files[0])
    print(f"📄 Membaca dataset: {dataset_file}")
    data = pd.read_csv(dataset_file)

    if "pertanyaan" not in data.columns or "jawaban" not in data.columns:
        raise ValueError("❌ CSV harus punya kolom: pertanyaan, jawaban")

    with app.app_context():
        db.session.query(Dataset).delete()
        for _, row in data.iterrows():
            item = Dataset(pertanyaan=row["pertanyaan"], jawaban=row["jawaban"])
            db.session.add(item)
        db.session.commit()
        print(f"✅ {len(data)} baris dataset berhasil dimasukkan ke tabel 'dataset'.")


def load_peraturan_to_db():
    text_files = [f for f in os.listdir(TEXT_PATH) if f.endswith(".txt")]
    if not text_files:
        raise FileNotFoundError("❌ Tidak ada file hasil parsing PDF di uploads/texts/")
    
    text_file = os.path.join(TEXT_PATH, text_files[0])
    print(f"📘 Membaca file peraturan: {text_file}")

    with open(text_file, "r", encoding="utf-8") as f:
        text = f.read()

    # Bagi berdasarkan 'Pasal' agar tiap pasal disimpan terpisah
    pasals = []
    lines = text.split("\n")
    current_pasal, isi = "", []

    for line in lines:
        line = line.strip()
        if line.lower().startswith("pasal "):
            if current_pasal:
                pasals.append((current_pasal, "\n".join(isi).strip()))
                isi = []
            current_pasal = line
        else:
            if line:
                isi.append(line)
    if current_pasal:
        pasals.append((current_pasal, "\n".join(isi).strip()))

    with app.app_context():
        db.session.query(Peraturan).delete()
        for pasal, isi in pasals:
            entry = Peraturan(pasal=pasal, isi=isi)
            db.session.add(entry)
        db.session.commit()
        print(f"✅ {len(pasals)} pasal berhasil dimasukkan ke tabel 'peraturan'.")


if __name__ == "__main__":
    print("🚀 Memulai proses load dataset & peraturan ke database...")
    load_dataset_to_db()
    load_peraturan_to_db()
    print("🎉 Semua data berhasil dimasukkan ke MySQL!")
