import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import requests

# Load .env
load_dotenv()
WP_API_URL = os.getenv("WP_API_URL")
WP_USER = os.getenv("WP_USER")
WP_PASS = os.getenv("WP_PASS")

def ambil_tabel_sgp():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            url = "http://146.190.92.226/data-keluaran-singapore/"

            # Tambahkan retry maksimal 3x
            for attempt in range(3):
                try:
                    print(f"🌐 Akses ke {url} (percobaan {attempt + 1})")
                    page.goto(url, timeout=90000, wait_until="load")
                    page.wait_for_selector("table.baru", timeout=10000)
                    break  # sukses, keluar dari loop
                except Exception as e:
                    print(f"🔁 Gagal buka halaman (percobaan {attempt + 1}): {e}")
                    if attempt == 2:
                        raise  # kalau 3x gagal, lempar error

            html = page.content()
            browser.close()

            soup = BeautifulSoup(html, "html.parser")
            tabel_list = soup.find_all("table", class_="baru")

            if not tabel_list:
                print("❌ Tidak ada tabel ditemukan.")
                return None

            hasil = []

            for table in tabel_list:
                heading = table.find_previous(["h2", "h3", "h4"])
                if heading:
                    hasil.append(f"<{heading.name}>{heading.text.strip()}</{heading.name}>")

                # Ubah warna lama ke warna baru
                table_html = str(table).replace("#68a225", "#29bfe5").replace("#265c00", "#30257d")
                hasil.append(table_html)

            print(f"✅ Ditemukan {len(tabel_list)} tabel + judul.")
            return "\n".join(hasil)

    except Exception as e:
        print(f"❌ Error ambil data: {e}")
        return None


def gabungkan_ke_template(tabel_html):
    try:
        bagian_atas = """
<article id="post-4704" class="single-view post-4704 post type-post status-publish format-standard hentry category-data-sgp tag-data-sgp tag-keluaran-sgp tag-paito-sgp tag-pengeluran-sgp tag-result-sgp" itemprop="blogPost" itemscope="" itemtype="http://schema.org/BlogPosting">
<header class="entry-header cf">
<h1 class="entry-title" itemprop="headline"><a href="./">Data Keluaran Singapore 2025</a></h1>
</header>
<div class="entry-byline cf">	
</div>
<div class="entry-content cf" itemprop="text">
<p><strong>Data Keluaran Singapore 2025, Data SGP 2024, Angka Pengeluaran SGP Terlengkap</strong></p>
<p>Rekapan Data <span style="text-decoration: underline;"><a href="./"><strong>Pengeluaran singapore</strong></a></span> merupakan kumpulan Result sgp 2025 setiap harinya yang di kumpulkan dalam tabel paito singapore. Hasil keluaran sgp sendiri mempunyai performa yang baik bagi pemain dalam permusan angka atau sekedar mengecek pengeluaran singapura hari ini.</p>
<p><span style="text-decoration: underline;"><strong>Data singapore 2025</strong></span> atau Rekap sgp adalah perkakas yang sangat penting untuk mencari angka tarikan paito terbaik. Sehingga Kami telah merangkum keluaran singapura mulai dari tahun 2019 sd 2025 untuk mempermudah anda mendapatkan hasil result togel singapore terbaru.</p>
<div id="attachment_4732" style="width: 1010px" class="wp-caption alignnone"><p id="caption-attachment-4732" class="wp-caption-text">Data Keluaran Singapore 2025, Data Sgp pools terbaru</p></div>
<table>
<tbody>
<tr>
<td>Data Keluaran togel singapore 2025, jam result sgp adalah pukul 17.40 WIB langsung dari situs resminya www.singaporepools.com</td>
</tr>
</tbody>
"""

        bagian_bawah = """
<p>Data tabel <a href="./"><span style="text-decoration: underline;"><strong>Keluaran singapore 2025</strong></span></a> untuk hari ini. Data sgp ini kami update secara Manual melalui situs resmi keluaran sgp. <strong>Data SGP 2025</strong>&nbsp;kami tampilkan dalam bentuk tabel yang simpel dan mudah untuk di pahami oleh para pengguna togel mania singapore.</p>
<blockquote><p>Kamu mungkin juga membutuhkan <a href="https://result.gbg-coc.org/data-pengeluaran-macau/"><strong>Data Macau 2025</strong></a></p></blockquote>
<p>Nomor Keluaran singapore terbaru, Hasil <a href="./">result sgp</a> tercepat, angka pengeluaran toto sgp terlengkap mulai tahun 2019 sampai dengan sekarang. Mempermudah dalam pemecahan rumus pemutaran angka dengan menggunakan <strong>data keluaran singapore 2025</strong>.</p>
<h3>Data SGP terbaru 2025</h3>
<p>Anda yang ingin mendapatkan keluaran singapore tercepat pada hari ini adalah dengan mengunjungi datakeluaran.org saja anda akan mendapatkan nomor keluaran singapore terbaru.</p>
<p>Dengan adanya <strong>Data keluaran singapore 2025</strong>&nbsp;ini semoga dapat membantu sobat hari ini, Jangan lupa untuk share juga prediksi anda dalam komentar. Berkunjunglah kemari lagi untuk menemukan <strong><em>Data SGP 2025</em></strong>&nbsp;terbaru.</p>
<h4>Incoming search terms:</h4><ul><li>Data sgp 2024</li><li>Togel sgp 2024</li><li>Data Sgp 2023</li><li>Data pengeluaran sgp 2024</li><li>Data togel sgp 2024</li><li>pengeluaran sgp 2024</li><li>data togel sgp</li><li>Data pengluaran sgp</li><li>togel singapor 2001/2024</li><li>pengeluaran sgp 2023</li></ul>	
</div>
<footer class="entry-footer cf">
</footer>
</article>
"""

        hasil_html = bagian_atas + tabel_html + bagian_bawah

        with open("result_sgp.html", "w", encoding="utf-8") as f:
            f.write(hasil_html)

        print("✅ result_sgp.html berhasil dibuat.")
        return hasil_html
    except Exception as e:
        print(f"❌ Error saat gabung template: {e}")
        return None

def post_ke_wordpress(html_content):
    if not WP_API_URL or not WP_USER or not WP_PASS:
        print("❌ Data .env tidak lengkap.")
        return

    headers = {"Content-Type": "application/json"}
    data = {
        "title": "",
        "content": html_content,
        "status": "publish"
    }

    try:
        r = requests.post(WP_API_URL, json=data, auth=(WP_USER, WP_PASS), headers=headers)
        if r.status_code in [200, 201]:
            print("✅ Berhasil posting ke WordPress.")
            print(f"🔗 Link: {r.json().get('link')}")
        else:
            print(f"❌ Gagal post: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"❌ Error saat post ke WordPress: {e}")

if __name__ == "__main__":
    tabel_html = ambil_tabel_sgp()
    if tabel_html:
        full_html = gabungkan_ke_template(tabel_html)
        if full_html:
            post_ke_wordpress(full_html)
