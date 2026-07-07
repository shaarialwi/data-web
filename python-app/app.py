"""
PRN Dewan Negeri Johor Ke-16 — Senarai Calon & Pengundi Mengikut DUN
A small Flask website. Viewers can browse all 56 DUN, search, and see the
candidates contesting each seat plus the total registered voters.

Run:
    pip install -r requirements.txt
    python app.py
Then open http://127.0.0.1:5000
"""
from flask import Flask, render_template, request, jsonify, abort

app = Flask(__name__)

# --- Party / coalition colours -------------------------------------------
COLORS = {
    "BN": "#1c4fa3", "PH": "#c62828", "PN": "#0f766e",
    "BERSAMA": "#6d28d9", "MUDA": "#c026d3", "BEBAS": "#64748b",
    "PSM": "#9d174d", "ASLI": "#a16207",
}

def coalition(party):
    return party.split("-")[0]

def label(party):
    p = party.split("-")
    return f"{p[0]} · {p[1]}" if len(p) > 1 else p[0]

def color(party):
    return COLORS.get(coalition(party), "#64748b")

def fmt(n):
    return f"{n:,}"

# --- Data (SPR, Daftar Pemilih April 2026) --------------------------------
# Each seat: code, name, registered voters, candidates [(name, party)], 2022 incumbent.
DATA = [
    {"code": "N.01", "name": "Buloh Kasap", "voters": 28973, "cands": [("Datuk Zahari Sarip", "BN-UMNO"), ("Noraziah Mohd Razit", "PH-PKR")], "inc": ("Datuk Zahari Sarip", "BN-UMNO")},
    {"code": "N.02", "name": "Jementah", "voters": 41137, "cands": [("Saifullah Abdul Wahab", "PN-PAS"), ("See Ann Giap", "BN-MCA"), ("Ng Kor Sim", "PH-DAP")], "inc": ("Ng Kor Sim", "PH-DAP")},
    {"code": "N.03", "name": "Pemanis", "voters": 30458, "cands": [("Anuar Abd Manap", "BN-UMNO"), ("Dr A. Ariventharan", "PN-MIPP"), ("Jalex Lee En Xiang", "PH-PKR")], "inc": ("Anuar Abd Manap", "BN-UMNO")},
    {"code": "N.04", "name": "Kemelah", "voters": 35365, "cands": [("K. Raven Kumar", "BN-MIC"), ("Mohd Afif Abd Hamid", "PH-AMANAH"), ("Uzzair Ismail", "PN-BERSATU")], "inc": ("N Saraswati", "BN-MIC")},
    {"code": "N.05", "name": "Tenang", "voters": 22616, "cands": [("Siti Aisyah Zobir", "BEBAS"), ("Normala Sudirman", "PN-PAS"), ("Elia Nadira Sabudin", "PH-AMANAH"), ("Mohd Azahar Ibrahim", "BN-UMNO")], "inc": ("Haslinda Salleh", "BN-UMNO")},
    {"code": "N.06", "name": "Bekok", "voters": 27317, "cands": [("Tan Chong", "BN-MCA"), ("Tay Yok Jiuen", "PH-DAP")], "inc": ("Tan Chong", "BN-MCA")},
    {"code": "N.07", "name": "Bukit Kepong", "voters": 37683, "cands": [("C. Subramani", "PH-PKR"), ("Ahmad Syar'e Yusof", "BN-UMNO"), ("Datuk Dr Sahruddin Jamal", "PN-BERSATU")], "inc": ("Datuk Dr Sahruddin Jamal", "PN-BERSATU")},
    {"code": "N.08", "name": "Bukit Pasir", "voters": 34142, "cands": [("Mohd Idzharruddin Mohd Nasirruddin", "PN-BERSATU"), ("Muhd Najib Lep", "PH-AMANAH"), ("Mohamad Fazli Mohamad Salleh", "BN-UMNO")], "inc": ("Mohamad Fazli Mohamad Salleh", "BN-UMNO")},
    {"code": "N.09", "name": "Gambir", "voters": 30326, "cands": [("Sahrihan Jani", "BN-UMNO"), ("Mohd Nor Mohd Yusof", "PH-PKR"), ("Suraya Sulaiman", "PN-PEJUANG")], "inc": ("Sahrihan Jani", "BN-UMNO")},
    {"code": "N.10", "name": "Tangkak", "voters": 36955, "cands": [("Haw Chin Teck", "BN-MCA"), ("Ee Chin Li", "PH-DAP")], "inc": ("Ee Chin Li", "PH-DAP")},
    {"code": "N.11", "name": "Serom", "voters": 40172, "cands": [("Nadhirah Afiqah Abdull Rahim", "BN-UMNO"), ("Mahfidz Omar", "PN-BERSATU"), ("Ahmad Nazari Abd Hamid", "PH-AMANAH")], "inc": ("Khairin-Nisa Ismail @ Md On", "BN-UMNO")},
    {"code": "N.12", "name": "Bentayan", "voters": 34205, "cands": [("Ng Yak Howe", "PH-DAP"), ("Chua Lee Huat", "BN-MCA")], "inc": ("Ng Yak Howe", "PH-DAP")},
    {"code": "N.13", "name": "Simpang Jeram", "voters": 41975, "cands": [("Nazri Abd Rahman", "PH-AMANAH"), ("Datuk Azman Ismail", "BN-UMNO"), ("Ainie Haziqah Shafii", "MUDA"), ("Arshed Yahya @ Awang", "PN-PAS")], "inc": ("Datuk Seri Salahuddin Ayub", "PH-AMANAH")},
    {"code": "N.14", "name": "Bukit Naning", "voters": 23002, "cands": [("S. Jeghanaathan", "BEBAS"), ("Md Ysahrudin Kusni", "PH-PKR"), ("Mohd Ghazali Sabari @ Atan", "BN-UMNO"), ("Iskandar Md Alias", "BERSAMA"), ("Mohd Radzi Amin", "PN-BERSATU")], "inc": ("Datuk Mohd Fuad Tukirin", "BN-UMNO")},
    {"code": "N.15", "name": "Maharani", "voters": 40040, "cands": [("Mohamad Anuar Hayan", "PN-PAS"), ("Datuk Ashari Md Sarip", "BN-UMNO"), ("Muhammad Amir Fiqri", "MUDA"), ("Muhammad Taqiuddin Cheman", "PH-AMANAH")], "inc": ("Abdul Aziz Talib", "PN-PAS")},
    {"code": "N.16", "name": "Sungai Balang", "voters": 31039, "cands": [("Selamat Takim", "BN-UMNO"), ("Muhammad Amin Sailan", "PN-PAS"), ("Ayna Soraya Badaruddin", "PH-PKR")], "inc": ("Selamat Takim", "BN-UMNO")},
    {"code": "N.17", "name": "Semerah", "voters": 47431, "cands": [("Mohd Fared Mohd Khalid", "BN-UMNO"), ("Halim Kepol", "PN-PAS"), ("Mohd Khuzzan Abu Bakar", "PH-PKR")], "inc": ("Mohd Fared Mohd Khalid", "BN-UMNO")},
    {"code": "N.18", "name": "Sri Medan", "voters": 33875, "cands": [("Ahmad Rosdi Bahari", "PN-PAS"), ("Datuk Zulkurnain Kamisan", "BN-UMNO"), ("Hishamuddin Ishak", "PH-PKR")], "inc": ("Datuk Zulkurnain Kamisan", "BN-UMNO")},
    {"code": "N.19", "name": "Yong Peng", "voters": 34023, "cands": [("Ling Tian Soon", "BN-MCA"), ("Yong Hui Yi", "PH-DAP")], "inc": ("Ling Tian Soon", "BN-MCA")},
    {"code": "N.20", "name": "Semarang", "voters": 28753, "cands": [("Muhammad Syafiq Abdul Aziz", "PN-BERSATU"), ("Datuk Samsolbari Jamali", "BN-UMNO"), ("Ramli Abd Hamid", "PH-AMANAH")], "inc": ("Datuk Samsolbari Jamali", "BN-UMNO")},
    {"code": "N.21", "name": "Parit Yaani", "voters": 44741, "cands": [("Datuk Mohamad Najib Samuri", "BN-UMNO"), ("Md Ezam Md Taslim", "PH-AMANAH")], "inc": ("Datuk Mohamad Najib Samuri", "BN-UMNO")},
    {"code": "N.22", "name": "Parit Raja", "voters": 38159, "cands": [("Shazwan Zdainal Abidin", "PH-DAP"), ("Dr Mohamed Maliki Mohamed Rapiee", "PN-BERSATU"), ("Nor Rashidah Ramli", "BN-UMNO")], "inc": ("Nor Rashidah Ramli", "BN-UMNO")},
    {"code": "N.23", "name": "Penggaram", "voters": 70294, "cands": [("Poh Rui Ling", "PH-DAP"), ("Boo Chin Liong", "BN-MCA")], "inc": ("Gan Peck Cheng", "PH-DAP")},
    {"code": "N.24", "name": "Senggarang", "voters": 38576, "cands": [("Datuk Mohd Rashid Hasnon", "PN-BERSATU"), ("Onn Abu Bakar", "PH-PKR"), ("Mohd Yusla Ismail", "BN-UMNO")], "inc": ("Mohd Yusla Ismail", "BN-UMNO")},
    {"code": "N.25", "name": "Rengit", "voters": 27608, "cands": [("Syed Mohamad Syed Alwi", "PN-BERSATU"), ("Zaidi Japar", "BN-UMNO"), ("Mohamad Yazid Bakri", "PH-AMANAH")], "inc": ("Datuk Dr Mohd Puad Zarkashi", "BN-UMNO")},
    {"code": "N.26", "name": "Machap", "voters": 35206, "cands": [("Nor Hafiz Roslan", "PH-AMANAH"), ("Datuk Onn Hafiz Ghazi", "BN-UMNO")], "inc": ("Datuk Onn Hafiz Ghazi", "BN-UMNO")},
    {"code": "N.27", "name": "Layang-Layang", "voters": 25181, "cands": [("Guna Balakrishnan", "PH-PKR"), ("Abd Mutalip Abd Rahim", "PN-BERSATU"), ("Chua Jian Boon", "BN-MCA")], "inc": ("Abd Mutalip Abd Rahim", "BN-UMNO")},
    {"code": "N.28", "name": "Mengkibol", "voters": 68457, "cands": [("Yap Zhi Peng", "BN-MCA"), ("Chu Poh Yee", "PH-DAP")], "inc": ("Chew Chong Sin", "PH-DAP")},
    {"code": "N.29", "name": "Mahkota", "voters": 67562, "cands": [("Abd Hamid Ali", "BERSAMA"), ("Syed Hussien Syed Abdullah", "BN-UMNO"), ("Dr Ahmad Zuhan Md Zain", "PH-AMANAH")], "inc": ("Datuk Sharifah Azizah Datuk Syed Zain", "BN-UMNO")},
    {"code": "N.30", "name": "Paloh", "voters": 25419, "cands": [("G. Kamaleswaren", "BEBAS"), ("Dr A. Ruban", "PH-DAP"), ("Lee Ting Han", "BN-MCA"), ("D. Jeevakumar", "PN-MIPP")], "inc": ("Lee Ting Han", "BN-MCA")},
    {"code": "N.31", "name": "Kahang", "voters": 29814, "cands": [("V. Rugendran", "BN-MIC"), ("Mohd Sabri Abd Kadir", "PH-AMANAH"), ("Mazlan Bujang", "PN-PAS")], "inc": ("R Vidyananthan", "BN-MIC")},
    {"code": "N.32", "name": "Endau", "voters": 28767, "cands": [("Hasnul Hakimi Hussien", "PN-PAS"), ("Jati Awang", "ASLI"), ("Saiful Nizam Samat", "PH-PKR"), ("Alwiyah Talib", "BN-UMNO")], "inc": ("Alwiyah Talib", "PN-BERSATU")},
    {"code": "N.33", "name": "Tenggaroh", "voters": 39001, "cands": [("Muhamad Amerul Muhamad", "PN-BERSATU"), ("Mohd Youzaimi Yusof", "BN-UMNO"), ("Md Yusof Dawam", "PH-PKR")], "inc": ("Raven Kumar Krishnasamy", "BN-MIC")},
    {"code": "N.34", "name": "Panti", "voters": 41407, "cands": [("Dr Muhammad Naqib Md Ghazali", "BN-UMNO"), ("Alias Rasman", "PN-BERSATU"), ("Ahmad Daniel Sharudin", "PH-AMANAH")], "inc": ("Hahasrin Hashim", "BN-UMNO")},
    {"code": "N.35", "name": "Pasir Raja", "voters": 29818, "cands": [("Datuk Seri Adham Baba", "BN-UMNO"), ("Yuhanita Yunan", "PN-PAS"), ("Mohd Fakharuddin Moslim", "PH-PKR")], "inc": ("Rashidah Ismail", "BN-UMNO")},
    {"code": "N.36", "name": "Sedili", "voters": 29090, "cands": [("Amirul Huzni Onn", "PH-AMANAH"), ("Muszaide Makmor", "BN-UMNO"), ("Rasman Ithnain", "PN-BERSATU")], "inc": ("Muszaide Makmor", "BN-UMNO")},
    {"code": "N.37", "name": "Johor Lama", "voters": 32716, "cands": [("Aisah Esa", "PN-BERSATU"), ("Danish Hossman Abd Rahman", "PH-PKR"), ("Norlizah Noh", "BN-UMNO")], "inc": ("Norlizah Noh", "BN-UMNO")},
    {"code": "N.38", "name": "Penawar", "voters": 31112, "cands": [("Fauziah Misri", "BN-UMNO"), ("Mohd Sawaludin Salleh", "PH-AMANAH"), ("Fairulnizar Rahmat", "PN-BERSATU")], "inc": ("Fauziah Misri", "BN-UMNO")},
    {"code": "N.39", "name": "Tanjung Surat", "voters": 26943, "cands": [("Faizul Abdul Ghani", "PH-PKR"), ("Aznan Tamin", "BN-UMNO")], "inc": ("Aznan Tamin", "BN-UMNO")},
    {"code": "N.40", "name": "Tiram", "voters": 117496, "cands": [("Datuk Abdul Halim Suleiman", "BN-UMNO"), ("Nor Zulaila Abd Ghani", "PH-DAP"), ("Dr Harith Fakhrudin Abdul Malek", "BERSAMA"), ("Khirul Muntanazar Ismail", "PN-PAS")], "inc": ("Azizul Bachok", "BN-UMNO")},
    {"code": "N.41", "name": "Puteri Wangsa", "voters": 128723, "cands": [("Nicholas Paul Vincent", "BERSAMA"), ("Wang Wee Siong", "BEBAS"), ("Dr Maszlee Malik", "PH-PKR"), ("Rashifa Aljunied", "MUDA"), ("Teow Chia Ling", "BN-MCA")], "inc": ("Amira Aisya Abd Aziz", "MUDA")},
    {"code": "N.42", "name": "Johor Jaya", "voters": 97685, "cands": [("Lim Hun Peaw", "BEBAS"), ("Lau Yi Leong", "BERSAMA"), ("Chan San San", "BN-MCA"), ("Lee Wern Yiing", "PH-DAP")], "inc": ("Liow Cai Tung", "PH-DAP")},
    {"code": "N.43", "name": "Permas", "voters": 113963, "cands": [("Baharudin Mohamed Taib", "BN-UMNO"), ("Teo Siew Hui", "PH-AMANAH"), ("Dr Zamil Najwah", "BERSAMA"), ("T. Vela", "PN-MIPP")], "inc": ("Baharudin Mohamed Taib", "BN-UMNO")},
    {"code": "N.44", "name": "Larkin", "voters": 76662, "cands": [("Norsinah Abu", "BERSAMA"), ("Suhaizan Kayat", "PH-AMANAH"), ("Mohd Hairi Mad Shah", "BN-UMNO")], "inc": ("Mohd Hairi Mad Shah", "BN-UMNO")},
    {"code": "N.45", "name": "Stulang", "voters": 60029, "cands": [("Andrew Chen Kah Eng", "PH-DAP"), ("Stanley Tan", "BERSAMA"), ("Lim Chin Eng @ Roland Lim", "PN-BERSATU"), ("Bong Seng Heng", "BN-MCA")], "inc": ("Andrew Chen Kah Eng", "PH-DAP")},
    {"code": "N.46", "name": "Perling", "voters": 109992, "cands": [("P. Pannir Selvam", "BN-MIC"), ("Alan Tee Boon Tsong", "PH-DAP"), ("Boo Wei Han", "BERSAMA")], "inc": ("Liew Chin Tong", "PH-DAP")},
    {"code": "N.47", "name": "Kempas", "voters": 64244, "cands": [("Datuk Ramlee Bohani", "BN-UMNO"), ("Muhammad Faezuddin Mohd Puad", "PH-PKR"), ("Salamahafifi Mohd Yusnaieny", "BERSAMA")], "inc": ("Datuk Ramlee Bohani", "BN-UMNO")},
    {"code": "N.48", "name": "Skudai", "voters": 106805, "cands": [("Tan Hiang Kee", "BN-MCA"), ("Kartiyaini Jeyapalan", "PH-DAP"), ("Eugene Chua Meng Chong", "BERSAMA"), ("Amir Syafiq Ameer Soekre", "PSM")], "inc": ("Marina Ibrahim", "PH-DAP")},
    {"code": "N.49", "name": "Kota Iskandar", "voters": 132579, "cands": [("S. Anna Pravina", "PN-MIPP"), ("Dzulkefly Ahmad", "PH-AMANAH"), ("Datuk Pandak Ahmad", "BN-UMNO"), ("Sahrudin Omar", "BERSAMA")], "inc": ("Datuk Pandak Ahmad", "BN-UMNO")},
    {"code": "N.50", "name": "Bukit Permai", "voters": 44819, "cands": [("Muhammad Aidil Riduan Mohd Yusof", "BERSAMA"), ("Datuk Mohd Jafni Md Shukor", "BN-UMNO"), ("Mohamad Shafwan Ani", "PH-DAP"), ("M. Lina Manoh", "PN-MIPP")], "inc": ("Datuk Mohd Jafni Md Shukor", "BN-UMNO")},
    {"code": "N.51", "name": "Bukit Batu", "voters": 49963, "cands": [("R. Kumaran", "BN-MIC"), ("Kamaruzaman Ali", "BEBAS"), ("G. Tamili", "BERSAMA"), ("Chiong Sen Sern", "PH-PKR"), ("M. Premanand", "MUDA")], "inc": ("Chiong Sen Sern", "PH-PKR")},
    {"code": "N.52", "name": "Senai", "voters": 66635, "cands": [("Tai Chee Chee", "BN-MCA"), ("Wong Bor Yang", "PH-DAP"), ("Tew Chien How", "BERSAMA")], "inc": ("Wong Bor Yang", "PH-DAP")},
    {"code": "N.53", "name": "Benut", "voters": 28798, "cands": [("Datuk Mohd Sumali Reduan", "BN-UMNO"), ("Abd Razak Ismail", "PH-AMANAH")], "inc": ("Datuk Seri Hasni Mohammad", "BN-UMNO")},
    {"code": "N.54", "name": "Pulai Sebatang", "voters": 47651, "cands": [("Haniff @ Ghazali Hosman", "PH-PKR"), ("Hasrunizah Hassan", "BN-UMNO")], "inc": ("Hasrunizah Hassan", "BN-UMNO")},
    {"code": "N.55", "name": "Pekan Nanas", "voters": 37556, "cands": [("Yeo Tung Siong", "PH-DAP"), ("Tan Eng Meng", "BN-MCA")], "inc": ("Tan Eng Meng", "BN-MCA")},
    {"code": "N.56", "name": "Kukup", "voters": 34968, "cands": [("Md Israk Abdullah", "BN-UMNO"), ("Cheah Chee Hong", "PH-PKR")], "inc": ("Datuk Jefridin Atan", "BN-UMNO")},
]

TOTAL_CALON = sum(len(d["cands"]) for d in DATA)
TOTAL_PENGUNDI = 2727926
LEGEND = [
    ("BN", "Barisan Nasional"), ("PH", "Pakatan Harapan"), ("PN", "Perikatan Nasional"),
    ("BERSAMA", "Bersama"), ("MUDA", "Muda"), ("BEBAS", "Bebas"),
    ("PSM", "PSM"), ("ASLI", "Asli"),
]


def matches(d, q):
    if not q:
        return True
    if q in d["name"].lower() or q in d["code"].lower():
        return True
    return any(q in n.lower() or q in p.lower() for n, p in d["cands"])


@app.context_processor
def helpers():
    return dict(color=color, label=label, fmt=fmt, coalition=coalition)


@app.route("/")
def index():
    q = request.args.get("q", "").strip()
    ql = q.lower()
    sel_code = request.args.get("dun")

    filtered = [d for d in DATA if matches(d, ql)]
    selected = next((d for d in DATA if d["code"] == sel_code), None)
    if selected is None:
        selected = filtered[0] if filtered else DATA[0]

    return render_template(
        "index.html",
        duns=filtered,
        selected=selected,
        q=q,
        result_label=(f"{len(filtered)} kawasan dijumpai" if q else "56 kawasan DUN"),
        total_calon=TOTAL_CALON,
        total_pengundi=TOTAL_PENGUNDI,
        legend=[(k, n, color(k)) for k, n in LEGEND],
    )


@app.route("/api/duns")
def api_duns():
    """JSON feed of every seat — handy if you build a separate frontend."""
    return jsonify([
        {
            "code": d["code"], "name": d["name"], "voters": d["voters"],
            "candidates": [{"name": n, "party": p} for n, p in d["cands"]],
            "incumbent_2022": {"name": d["inc"][0], "party": d["inc"][1]},
        }
        for d in DATA
    ])


@app.route("/api/duns/<code>")
def api_dun(code):
    d = next((x for x in DATA if x["code"].lower() == code.lower()), None)
    if d is None:
        abort(404)
    return jsonify({
        "code": d["code"], "name": d["name"], "voters": d["voters"],
        "candidates": [{"name": n, "party": p} for n, p in d["cands"]],
        "incumbent_2022": {"name": d["inc"][0], "party": d["inc"][1]},
    })


if __name__ == "__main__":
    app.run(debug=True)
