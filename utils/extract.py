import time
import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def fetching_page(url):
    """
    Mengambil konten HTML dari sebuah URL.

    Args:
        url (str): Alamat URL halaman web.

    Returns:
        bytes | None: Konten HTML jika berhasil, None jika gagal.
    """
    session = requests.Session()
    try:
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"❌ Error saat mengambil url {url} : {e}")
        return None

def extract_product_info(product):
    """
    Mengekstrak informasi produk dari elemen HTML.

    Args:
        product (bs4.element.Tag): Elemen HTML dari produk.

    Returns:
        dict: Informasi produk (title, price, rating, dst).
    """
    try:
        title = product.find('h3').text
        price_span = product.find('span', class_='price')
        price = price_span.text.strip() if price_span else (
            product.find('p', class_='price').text.strip()
            if product.find('p', class_='price') else "-"
        )

        details = product.find_all('p', style='font-size: 14px; color: #777;')
        rating = details[0].text.strip() if len(details) > 0 else None
        colors = details[1].text.strip() if len(details) > 1 else None
        size = details[2].text.strip() if len(details) > 2 else None
        gender = details[3].text.strip() if len(details) > 3 else None
        timestamp = datetime.datetime.now()

        return {
            'Title': title,
            'Price': price,
            'Rating': rating,
            'Colors': colors,
            'Size': size,
            'Gender': gender,
            'Timestamp': timestamp
        }

    except Exception as e:
        print(f"❌ Gagal mengekstrak produk: {e}")
        return {}

def scrape_product(base_url, start_page=1, delay=2):
    """
    Melakukan web scraping terhadap daftar produk dari halaman web.

    Args:
        base_url (str): URL dasar halaman produk.
        start_page (int): Nomor halaman awal untuk scraping.
        delay (int): Delay (dalam detik) antar halaman untuk menghindari blokir.

    Returns:
        list: List berisi dict informasi produk.
    """
    data = []
    page_number = start_page

    while True:
        url = base_url if page_number == 1 else f"{base_url}page{page_number}"
        print(f"🔄 Scraping halaman ke {page_number}: {url}")
        content = fetching_page(url)

        if not content:
            print("❌ Gagal memuat halaman, berhenti.")
            break

        try:
            soup = BeautifulSoup(content, 'html.parser')
            products = soup.find_all('div', class_='product-details')
            if not products:
                print("⚠️ Tidak ada produk ditemukan di halaman ini.")
                break

            for product in products:
                product_info = extract_product_info(product)
                if product_info:
                    data.append(product_info)

            next_button = soup.select_one('li.page-item.next a.page-link')
            if not next_button:
                print("✅ Halaman terakhir ditemukan. Scraping selesai.")
                break

            page_number += 1
            time.sleep(delay)

        except Exception as e:
            print(f"❌ Terjadi kesalahan saat memproses halaman: {e}")
            break

    return data