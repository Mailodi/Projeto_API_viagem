import requests
import folium
from PIL import Image, ImageTk
import io

def get_unsplash_image(city_name, api_key):
    url = f"https://api.unsplash.com/photos/random?query={city_name}&orientation=landscape&client_id={api_key}"
    data = requests.get(url).json()
    img_data = requests.get(data["urls"]["regular"]).content
    photo = ImageTk.PhotoImage(Image.open(io.BytesIO(img_data)).resize((500, 300), resample=Image.LANCZOS))
    return photo

def get_weather_info(city_name, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
    response = requests.get(url)
    data = response.json()

    if 'main' not in data:
        return f'Não foi possível obter as informações climáticas para {city_name}'

    temperatura = data['main']['temp'] - 273.15
    descricao = data['weather'][0]['description']

    return f'Temperatura: {temperatura:.2f}°C\nDescrição: {descricao}'

def get_pontos_de_inter(city_name, google_places_api_key):
    url_places = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query=pontos+de+interesse+em+{city_name}&key={google_places_api_key}'
    response_places = requests.get(url_places)
    data_places = response_places.json()

    if 'results' not in data_places:
        return [{'erro': 'Não foi possível obter os pontos de interesse para a cidade fornecida'}]

    points_of_interest = [{'nome': lugar['name'], 'endereco': lugar['formatted_address']} for lugar in data_places['results']]
    return points_of_interest

def obter_coordenadas(api_key, endereco):
    url = f"http://www.mapquestapi.com/geocoding/v1/address?key={api_key}&location={endereco}"
    
    response = requests.get(url)
    data = response.json()

    latlng = data['results'][0]['locations'][0]['latLng']
    latitude = latlng['lat']
    longitude = latlng['lng']

    return latitude, longitude

# Criar um mapa Folium com as coordenadas fornecidas
def mostrar_no_mapa(latitude, longitude):
    
    mapa = folium.Map(location=[latitude, longitude], zoom_start=15)

    folium.Marker([latitude, longitude], popup='Local').add_to(mapa)

    mapa.save('mapa.html')
    print("Mapa gerado com sucesso. Abra o arquivo 'mapa.html' em seu navegador.")