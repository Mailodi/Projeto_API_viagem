import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from tkinter import Listbox, Scrollbar, SINGLE
from API_funcao import get_unsplash_image, get_weather_info, get_pontos_de_inter, obter_coordenadas, mostrar_no_mapa

UNSPLASH_API_KEY = ''
OPENWEATHERMAP_API_KEY = ''
GOOGLE_PLACES_API_KEY = ''
api_key_mapquest = ''  

# janela principal
root = tk.Tk()
root.title("Gerador de Imagens e Clima")
root.geometry("700x550")  
root.config(bg="white")
root.resizable(False, False)
style = Style(theme="sandstone")

def display_city_image(city_name):
    photo = get_unsplash_image(city_name, UNSPLASH_API_KEY)
    label.config(image=photo)
    label.image = photo
    display_weather_info(city_name)

def display_weather_info(city_name):
    info = get_weather_info(city_name, OPENWEATHERMAP_API_KEY)
    weather_label.config(text=info)

def enable_button(*args):
    generate_button.config(state="normal" if city_entry.get() != "" else "disabled")

def nova_janela(): # Cria uma nova janela 
    city_name = city_entry.get()
    points_of_interest = get_pontos_de_inter(city_name, GOOGLE_PLACES_API_KEY)

    new_window = tk.Toplevel(root)
    new_window.title("Pontos de Interesses")
    new_window.geometry("500x400")
    new_window.config(bg="white")

    listbox = Listbox(new_window, selectmode=SINGLE)
    listbox.pack(padx=10, pady=10, expand=True, fill="both")

    for poi in points_of_interest:
        listbox.insert(tk.END, f"{poi['nome']} - {poi['endereco']}")

    def search_selected_item():
        selected_index = listbox.curselection()
        if selected_index:
            selected_poi = points_of_interest[selected_index[0]]
            display_selected_info(selected_poi)

    search_button = ttk.Button(new_window, text="Pesquisar", command=search_selected_item)
    search_button.pack(pady=10)

    def show_on_map():
        selected_index = listbox.curselection()
        if selected_index:
            selected_poi = points_of_interest[selected_index[0]]
            endereco = selected_poi['endereco']
            latitude, longitude = obter_coordenadas(api_key_mapquest, endereco)
            mostrar_no_mapa(latitude, longitude)

    map_button = ttk.Button(new_window, text="Mostrar no Mapa", command=show_on_map)
    map_button.pack(pady=10)
    
def display_selected_info(selected_poi):
    city_name = selected_poi['nome']
    photo = get_unsplash_image(city_name, UNSPLASH_API_KEY)

    # Cria uma nova janela 
    result_window = tk.Toplevel(root)
    result_window.title(f"Resultado para {city_name}")
    result_window.geometry("600x500")
    result_window.config(bg="white")
    
    image_label = tk.Label(result_window, image=photo, background="white")
    image_label.pack(pady=10)

# elementos da interface gráfica
def create_gui():
    global city_entry, generate_button, label, weather_label

    city_entry = ttk.Entry(root)
    city_entry.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Botão para gerar imagem
    generate_button = ttk.Button(text="Gerar Imagem", state="disabled", command=lambda: display_city_image(city_entry.get()))
    generate_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    # exibir a imagem
    label = tk.Label(root, background="white")
    label.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    # informações climáticas
    weather_label = tk.Label(root, background="white", font=("Helvetica", 12))
    weather_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    
    # Botão para abrir a janela "Pontos de Interesses"
    new_window_button = ttk.Button(text="Pontos de Interesses", command=nova_janela)
    new_window_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    city_entry.bind("<KeyRelease>", enable_button)

    # Torne as colunas/linhas expansíveis
    root.columnconfigure([0, 1], weight=1)
    root.rowconfigure([1, 2], weight=1)
    root.mainloop()

if __name__ == '__main__':
    create_gui()
