from flask import Blueprint, request, jsonify
import os, pickle, numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from backend.config import MODEL_DIR, db, app
from backend.db.models import ChatHistory
from flask_cors import cross_origin

chat_bp = Blueprint("chat_bp", __name__)

# --- Load models & tokenizers ---
MAIN_MODEL_PATH = os.path.join(MODEL_DIR, "main_model.h5")
FALLBACK_MODEL_PATH = os.path.join(MODEL_DIR, "fallback_model.h5")
TOKEN_MAIN = os.path.join(MODEL_DIR, "tokenizer_main.pkl")
LABEL_MAIN = os.path.join(MODEL_DIR, "label_main.pkl")
TOKEN_FB = os.path.join(MODEL_DIR, "tokenizer_fallback.pkl")
LABEL_FB = os.path.join(MODEL_DIR, "label_fallback.pkl")

main_model = load_model(MAIN_MODEL_PATH) if os.path.exists(MAIN_MODEL_PATH) else None
fallback_model = load_model(FALLBACK_MODEL_PATH) if os.path.exists(FALLBACK_MODEL_PATH) else None
tokenizer_main = pickle.load(open(TOKEN_MAIN, "rb")) if os.path.exists(TOKEN_MAIN) else None
le_main = pickle.load(open(LABEL_MAIN, "rb")) if os.path.exists(LABEL_MAIN) else None
tokenizer_fallback = pickle.load(open(TOKEN_FB, "rb")) if os.path.exists(TOKEN_FB) else None
le_fallback = pickle.load(open(LABEL_FB, "rb")) if os.path.exists(LABEL_FB) else None

THRESHOLD = 0.6

# ================================
# ROUTE CHAT
# ================================
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from backend.config import MODEL_DIR, db
from backend.db.models import ChatHistory, TopicStats
from datetime import datetime
from sqlalchemy import func
import os, pickle, numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# ======================
# BLUEPRINT CHATBOT
# ======================
chat_bp = Blueprint("chat_bp", __name__)

# ======================
# LOAD MODEL & TOKENIZER
# ======================
MAIN_MODEL_PATH = os.path.join(MODEL_DIR, "main_model.h5")
FALLBACK_MODEL_PATH = os.path.join(MODEL_DIR, "fallback_model.h5")
TOKEN_MAIN = os.path.join(MODEL_DIR, "tokenizer_main.pkl")
LABEL_MAIN = os.path.join(MODEL_DIR, "label_main.pkl")
TOKEN_FB = os.path.join(MODEL_DIR, "tokenizer_fallback.pkl")
LABEL_FB = os.path.join(MODEL_DIR, "label_fallback.pkl")

main_model = load_model(MAIN_MODEL_PATH) if os.path.exists(MAIN_MODEL_PATH) else None
fallback_model = load_model(FALLBACK_MODEL_PATH) if os.path.exists(FALLBACK_MODEL_PATH) else None
tokenizer_main = pickle.load(open(TOKEN_MAIN, "rb")) if os.path.exists(TOKEN_MAIN) else None
le_main = pickle.load(open(LABEL_MAIN, "rb")) if os.path.exists(LABEL_MAIN) else None
tokenizer_fallback = pickle.load(open(TOKEN_FB, "rb")) if os.path.exists(TOKEN_FB) else None
le_fallback = pickle.load(open(LABEL_FB, "rb")) if os.path.exists(LABEL_FB) else None

THRESHOLD = 0.6


# ======================
# ROUTE CHAT
# ======================
@chat_bp.route("/chat", methods=["POST"])
@cross_origin()
def chat():
    data = request.json
    question = data.get("pertanyaan", "")
    npm = data.get("npm", None)

    if not question:
        return jsonify({"error": "Pertanyaan kosong"}), 400

    answer, source, confidence = "", "", 0.0

    # === MAIN MODEL ===
    if main_model and tokenizer_main and le_main:
        seq = tokenizer_main.texts_to_sequences([question])
        pad = pad_sequences(seq, maxlen=main_model.input_shape[1], padding="post")
        pred = main_model.predict(pad, verbose=0)
        confidence = float(np.max(pred))

        if confidence >= THRESHOLD:
            label = int(np.argmax(pred))
            answer = le_main.inverse_transform([label])[0]
            source = "dataset"
        else:
            # === FALLBACK MODEL ===
            if fallback_model and tokenizer_fallback and le_fallback:
                seq_fb = tokenizer_fallback.texts_to_sequences([question])
                pad_fb = pad_sequences(seq_fb, maxlen=fallback_model.input_shape[1], padding="post")
                pred_fb = fallback_model.predict(pad_fb, verbose=0)
                label_fb = int(np.argmax(pred_fb))
                answer = le_fallback.inverse_transform([label_fb])[0]
                source = "peraturan"
            else:
                answer = "⚠️ Model fallback belum tersedia."
                source = "none"
    else:
        answer = "⚠️ Model utama belum tersedia. Silakan minta admin untuk retrain."
        source = "none"

    # ======================
    # SIMPAN KE DATABASE
    # ======================
    try:
        # Simpan chat history
        new_chat = ChatHistory(
            npm=npm,
            question=question,
            answer=answer,
            source=source,
            confidence=confidence
        )
        db.session.add(new_chat)

        # Tentukan topik berdasarkan pertanyaan, bukan jawaban
        topic_name = question[:100]  # biar gak kepanjangan

        # Update atau tambahkan topik
        existing_topic = TopicStats.query.filter(
            func.lower(TopicStats.topic_name) == func.lower(topic_name)
        ).first()

        if existing_topic:
            existing_topic.mention_count += 1
            existing_topic.last_updated = datetime.utcnow()
        else:
            new_topic = TopicStats(
                topic_name=topic_name,
                mention_count=1,
                last_updated=datetime.utcnow()
            )
            db.session.add(new_topic)

        db.session.commit()
    except Exception as e:
        print("❌ Gagal menyimpan ChatHistory atau TopicStats:", e)
        db.session.rollback()

    # ======================
    # RESPONSE KE FRONTEND
    # ======================
    return jsonify({
        "jawaban": answer,
        "sumber": source,
        "confidence": confidence
    })
