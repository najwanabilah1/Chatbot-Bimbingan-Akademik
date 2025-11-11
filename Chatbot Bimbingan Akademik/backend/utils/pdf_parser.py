import fitz  # PyMuPDF
import os
import re

# ==============================
# KONFIGURASI FOLDER
# ==============================
PDF_DIR = os.path.join("backend", "uploads", "pdfs")
TEXT_DIR = os.path.join("backend", "uploads", "texts")
os.makedirs(TEXT_DIR, exist_ok=True)


def save_pdf_to_txt(pdf_path: str) -> str:
    """
    Ekstrak teks dari PDF ke file .txt dan pecah per pasal.
    Digunakan oleh admin_routes saat upload PDF baru.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"❌ File PDF tidak ditemukan: {pdf_path}")

    print(f"📘 Membaca PDF: {pdf_path}")
    doc = fitz.open(pdf_path)
    pasal_list = []
    current_pasal = ""
    isi_pasal = []

    # Gabung teks dari semua halaman
    full_text = ""
    for i, page in enumerate(doc):
        full_text += "\n" + page.get_text("text")
    doc.close()

    # Pisahkan berdasarkan 'Pasal' (regex fleksibel)
    lines = full_text.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        match = re.match(r"^(Pasal\s+\d+)", line, flags=re.IGNORECASE)
        if match:
            # Simpan pasal sebelumnya
            if current_pasal:
                pasal_list.append((current_pasal, "\n".join(isi_pasal).strip()))
                isi_pasal = []
            current_pasal = match.group(1)
        else:
            isi_pasal.append(line)
    if current_pasal:
        pasal_list.append((current_pasal, "\n".join(isi_pasal).strip()))

    # Simpan hasil ke file teks
    txt_filename = os.path.splitext(os.path.basename(pdf_path))[0] + ".txt"
    txt_path = os.path.join(TEXT_DIR, txt_filename)
    with open(txt_path, "w", encoding="utf-8") as f:
        for pasal, isi in pasal_list:
            f.write(f"{pasal}\n{isi}\n\n")

    print(f"✅ PDF berhasil diubah ke teks dan disimpan: {txt_path}")
    print(f"📄 Total pasal ditemukan: {len(pasal_list)}")
    return txt_path


if __name__ == "__main__":
    # 🔹 Contoh manual testing
    filename = "Peraturan-Rektor-No-25-Tahun-2020-Tentang-Penyelenggaraan-Kegiatan-Akademik-SEARCHABLE.pdf"
    full_path = os.path.join(PDF_DIR, filename)
    save_pdf_to_txt(full_path)
