import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin

URL = "https://tentaciones.info/load_products.php"

# Definí las ciudades y barrios que querés filtrar
ciudades = {
    'CABA': '1',
    'GBA': '2',
}

# Ejemplo de barrios para CABA (obtené más del sitio)
barrios_caba = ['Caballito_', 'Palermo_', 'Belgrano_', 'Recoleta_']

# Parámetros extra (vacíos para probar, llenalos si querés)
materiales = ['Gay_friendly','Parejas_Heterosexuales','Parejas_Heterosexuales_Y_Gay_friendly','Todo_tipo_de_parejas']  # ej. ['Pareja', 'Tríos', ...] según cómo se llamen
sizes = ['25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44']       # ej. ['1', '2', '3', '4', '5'] valoración Google
sorting_options = ['newest', 'low', 'high']

def scrapear_telos(category, brand, material='', size='', sorting='newest'):
    total_record = 0
    resultados = []

    while True:
        payload = {
            "totalRecord": str(total_record),
            "brand[]": [brand] if brand else [],
            "category[]": [category] if category else [],
            "material[]": [material] if material else [],
            "size[]": [size] if size else [],
            "sorting": sorting,
            "imagen": logo_url
        }

       
        if logo_url and logo_url.startswith('/'):
            logo_url = 'https://tentaciones.info' + logo_url
            logo_url = urljoin(BASE_URL, logo_url) if logo_url else None

        BASE_URL = "https://tentaciones.info/"
        logo_tag = articulo.img
        logo_url = logo_tag['src'] if logo_tag else ''

        # Elimina claves con listas vacías
        payload = {k: v for k, v in payload.items() if v}

        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Referer": "https://tentaciones.info/",
            "X-Requested-With": "XMLHttpRequest"
        }

        response = requests.post(URL, data=payload, headers=headers)
        if response.status_code != 200:
            print(f"Error en request: {response.status_code}")
            break

        try:
            data = response.json()  # si responde JSON
        except Exception as e:
            print("Error al parsear JSON:", e)
            break

        articulos_html = data.get("html", "")
        if not articulos_html.strip():
            # No quedan más resultados
            break

        soup = BeautifulSoup(articulos_html, 'html.parser')
        articulos = soup.select('article.col-md-4.col-sm-6')

        if not articulos:
            break

        for articulo in articulos:
            nombre = articulo.select_one('h3.product-name').get_text(strip=True)
            logo_url = articulo.img['src'] if articulo.img else None

            url = articulo.select_one('h3.product-name a')['href']
            barrio_nombre = articulo.select_one('h6 a').get_text(strip=True)
            resultados.append({
                'nombre': nombre,
                'url': url,
                'barrio': barrio_nombre,
                'category': category,
                'material': material,
                'size': size,
                'sorting': sorting,
                'imagen': logo_url
            })

        print(f"Scrapeados {len(articulos)} en {brand} offset {total_record} con filtros M:{material} S:{size} sort:{sorting}")

        total_record += len(articulos)
        time.sleep(1)

    return resultados
