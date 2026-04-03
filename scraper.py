import requests
from bs4 import BeautifulSoup
import json
import time

headers = {"User-Agent": "Mozilla/5.0"}

# 🔥 Pakai link artikel langsung (bukan search)
links = [
    "https://www.cnnindonesia.com/otomotif/20260402191659-603-1343841/panduan-singkat-beralih-ke-mobil-listrik-bagi-pemula",
    "https://www.cnnindonesia.com/ekonomi/20230303123945-85-920000/harga-bbm-dunia-naik-akibat-perang-rusia-ukraina",
]

data_list = []

for link in links:
    try:
        res = requests.get(link, headers=headers)

        if res.status_code != 200:
            print("Gagal akses:", link)
            continue

        soup = BeautifulSoup(res.text, "html.parser")

        # =====================
        # AMBIL JUDUL
        # =====================
        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else "Tidak ada judul"

        # =====================
        # AMBIL ISI ARTIKEL
        # =====================
        content_div = soup.find("div", class_="detail-text")

        if content_div:
            paragraphs = content_div.find_all("p")
            content = " ".join([p.get_text(strip=True) for p in paragraphs])
        else:
            content = "Isi tidak ditemukan"

        # =====================
        # SIMPAN DATA
        # =====================
        data = {
            "title": title,
            "content": content,
            "link": link
        }

        data_list.append(data)

        print("✅ Berhasil:", title)

        time.sleep(1)

    except Exception as e:
        print("❌ Error:", link)

# =====================
# SIMPAN KE JSON
# =====================
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data_list, f, indent=4, ensure_ascii=False)

print("\n🔥 SELESAI! Data sudah masuk ke data.json")