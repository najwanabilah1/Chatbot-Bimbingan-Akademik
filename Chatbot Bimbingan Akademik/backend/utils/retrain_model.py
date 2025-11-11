import os
import sys
import pickle
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from sklearn.preprocessing import LabelEncoder

# ======== FIX IMPORT PATHS ========
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from backend.config import app, db
from backend.db.models import Dataset, Peraturan

# ======== MODEL SAVE FOLDER ========
MODEL_DIR = os.path.join(os.path.dirname(__file__), "../model")
os.makedirs(MODEL_DIR, exist_ok=True)


# ==============================================================
# 🔹 TRAIN MODEL UTAMA (Dataset dari pertanyaan dan jawaban)
# ==============================================================
def retrain_main_from_db(epochs=30):
    with app.app_context():
        data = Dataset.query.all()
        if not data:
            raise ValueError("❌ Tabel Dataset kosong — tidak ada data untuk dilatih.")
        questions = [d.pertanyaan for d in data]
        answers = [d.jawaban for d in data]

    # Tokenisasi pertanyaan
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(questions)
    X = tokenizer.texts_to_sequences(questions)
    X = pad_sequences(X, padding="post")

    # Encode label jawaban
    le = LabelEncoder()
    y = le.fit_transform(answers)

    # Bangun model LSTM
    model = Sequential([
        Embedding(len(tokenizer.word_index)+1, 64, input_length=X.shape[1]),
        LSTM(128),
        Dense(64, activation='relu'),
        Dense(len(set(y)), activation='softmax')
    ])
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X, y, epochs=epochs, verbose=1)

    # Simpan model dan tokenizer
    model.save(os.path.join(MODEL_DIR, "main_model.h5"))
    with open(os.path.join(MODEL_DIR, "tokenizer_main.pkl"), "wb") as f:
        pickle.dump(tokenizer, f)
    with open(os.path.join(MODEL_DIR, "label_main.pkl"), "wb") as f:
        pickle.dump(le, f)

    print(f"✅ Model utama selesai dilatih ({len(questions)} data, vocab {len(tokenizer.word_index)})")
    return {"samples": len(questions), "vocab": len(tokenizer.word_index)}


# ==============================================================
# 🔹 TRAIN MODEL FALLBACK (dari pasal & isi peraturan)
# ==============================================================
def retrain_fallback_from_db(epochs=20):
    with app.app_context():
        regs = Peraturan.query.all()
        if not regs:
            raise ValueError("❌ Tabel Peraturan kosong — upload PDF dulu.")
        titles = [r.pasal or f"Pasal {r.id}" for r in regs]
        contents = [r.isi for r in regs]

    # Tokenisasi pasal
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(titles)
    X = tokenizer.texts_to_sequences(titles)
    X = pad_sequences(X, padding="post")

    # Encode isi pasal
    le = LabelEncoder()
    y = le.fit_transform(contents)

    # Model LSTM fallback
    model = Sequential([
        Embedding(len(tokenizer.word_index)+1, 64, input_length=X.shape[1]),
        LSTM(128),
        Dense(64, activation='relu'),
        Dense(len(set(y)), activation='softmax')
    ])
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X, y, epochs=epochs, verbose=1)

    # Simpan model & tokenizer fallback
    model.save(os.path.join(MODEL_DIR, "fallback_model.h5"))
    with open(os.path.join(MODEL_DIR, "tokenizer_fallback.pkl"), "wb") as f:
        pickle.dump(tokenizer, f)
    with open(os.path.join(MODEL_DIR, "label_fallback.pkl"), "wb") as f:
        pickle.dump(le, f)

    print(f"✅ Model fallback selesai dilatih ({len(titles)} pasal, vocab {len(tokenizer.word_index)})")
    return {"pasal": len(titles), "vocab": len(tokenizer.word_index)}


# ==============================================================
# 🔹 TRAIN KEDUANYA SEKALIGUS
# ==============================================================
def retrain_all():
    print("\n🧠 Melatih ulang model utama dari Dataset...")
    retrain_main_from_db()
    print("\n📘 Melatih ulang model fallback dari Peraturan...")
    retrain_fallback_from_db()
    print("\n✅ Semua model berhasil dilatih dan disimpan di folder model/.")


if __name__ == "__main__":
    retrain_all()