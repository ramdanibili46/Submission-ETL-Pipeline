from unittest.mock import patch, Mock
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import datetime

from utils import *

# --- Test fetching_page ---
@patch("utils.extract.requests.Session.get")
def test_fetching_page_success(mock_get):
    """
    Test fungsi fetching_page saat berhasil mendapatkan respon dari URL.
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b"<html><body>Mock Page</body></html>"
    mock_get.return_value = mock_response

    content = fetching_page("http://example.com")
    assert content == b"<html><body>Mock Page</body></html>"

@patch("utils.requests.Session.get")
def test_fetching_page_failure(mock_get):
    """
    Test fungsi fetching_page saat terjadi exception (gagal koneksi).
    Fungsi diharapkan mengembalikan None.
    """
    mock_get.side_effect = RequestException("Connection error")

    content = fetching_page("http://example.com")
    assert content is None


# --- Test extract_product_info ---
def test_extract_product_info_complete():
    """
    Test extract_product_info dengan data produk lengkap
    termasuk harga di dalam tag <span class='price'>.
    """
    html = """
    <div class='product-details'>
        <h3>Product 1</h3>
        <span class='price'>$19.99</span>
        <p style='font-size: 14px; color: #777;'>4.5 stars</p>
        <p style='font-size: 14px; color: #777;'>Red</p>
        <p style='font-size: 14px; color: #777;'>L</p>
        <p style='font-size: 14px; color: #777;'>Unisex</p>
    </div>
    """
    soup = BeautifulSoup(html, 'html.parser')
    product = soup.find('div', class_='product-details')

    result = extract_product_info(product)
    assert result['Title'] == "Product 1"
    assert result['Price'] == "$19.99"
    assert result['Rating'] == "4.5 stars"
    assert result['Colors'] == "Red"
    assert result['Size'] == "L"
    assert result['Gender'] == "Unisex"
    assert isinstance(result['Timestamp'], datetime.datetime)


def test_extract_product_info_price_in_p_tag():
    """
    Test extract_product_info dengan harga berada pada tag <p class='price'>,
    bukan di <span class='price'>.
    """
    html = """
    <div class='product-details'>
        <h3>Product with P Price</h3>
        <p class='price'>$15.99</p>
        <p style='font-size: 14px; color: #777;'>3 stars</p>
        <p style='font-size: 14px; color: #777;'>Black</p>
        <p style='font-size: 14px; color: #777;'>S</p>
        <p style='font-size: 14px; color: #777;'>Women</p>
    </div>
    """
    soup = BeautifulSoup(html, 'html.parser')
    product = soup.find('div', class_='product-details')

    result = extract_product_info(product)
    assert result['Title'] == "Product with P Price"
    assert result['Price'] == "$15.99"


def test_extract_product_info_incomplete():
    """
    Test extract_product_info dengan data produk tidak lengkap,
    khususnya tanpa informasi harga.
    Harga diharapkan menjadi "-" dan field lain disesuaikan.
    """
    html = """
    <div class='product-details'>
        <h3>Product 2</h3>
        <!-- Harga dan beberapa detail tidak ada -->
        <p style='font-size: 14px; color: #777;'>4 stars</p>
    </div>
    """
    soup = BeautifulSoup(html, 'html.parser')
    product = soup.find('div', class_='product-details')

    result = extract_product_info(product)
    assert result['Title'] == "Product 2"
    assert result['Price'] == "-"
    assert result['Rating'] == "4 stars"
    assert result['Colors'] is None


# --- Test scrape_product ---
@patch("utils.extract.fetching_page")
@patch("time.sleep", return_value=None)  # Supaya delay saat test dihilangkan
def test_scrape_product(mock_sleep, mock_fetching_page):
    """
    Test fungsi scrape_product dengan memanfaatkan mock untuk halaman HTML.
    - Halaman pertama mengandung 1 produk dan tombol next page.
    - Halaman kedua mengandung 1 produk dan tidak ada tombol next page (akhir).
    """
    html_page_1 = """
    <html>
      <body>
        <div class='product-details'>
            <h3>Product A</h3>
            <span class='price'>$10</span>
            <p style='font-size: 14px; color: #777;'>5 stars</p>
            <p style='font-size: 14px; color: #777;'>Blue</p>
            <p style='font-size: 14px; color: #777;'>M</p>
            <p style='font-size: 14px; color: #777;'>Men</p>
        </div>
        <li class="page-item next"><a class="page-link" href="#">Next</a></li>
      </body>
    </html>
    """

    html_page_2 = """
    <html>
      <body>
        <div class='product-details'>
            <h3>Product B</h3>
            <p class='price'>$20</p>
            <p style='font-size: 14px; color: #777;'>4 stars</p>
            <p style='font-size: 14px; color: #777;'>Green</p>
            <p style='font-size: 14px; color: #777;'>L</p>
            <p style='font-size: 14px; color: #777;'>Women</p>
        </div>
      </body>
    </html>
    """

    # Side effect: setiap kali fetching_page dipanggil, kembalikan konten mock yang berbeda (html_1/html_2)
    mock_fetching_page.side_effect = [html_page_1.encode('utf-8'), html_page_2.encode('utf-8')]

    base_url = "http://fakeurl.com/products/"

    results = scrape_product(base_url, start_page=1, delay=0)

    assert len(results) == 2
    assert results[0]['Title'] == "Product A"
    assert results[0]['Price'] == "$10"
    assert results[1]['Title'] == "Product B"
    assert results[1]['Price'] == "$20"
