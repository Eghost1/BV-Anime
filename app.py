from animeflv import AnimeFLV
import streamlit as st 
import json
from PIL import Image

logo= Image.open("assets/IMG/Logo BVAnime.jpeg"

# Configuración de la página
st.set_page_config(page_title='APP Anime', page_icon='logo', layout='centered')

# Aplicar estilos CSS para centrar y asegurar que el iframe mantenga el tamaño
st.markdown(
    """
    <style>
    .center-iframe {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    iframe {
        width: 1280px;
        height: 720px;
        max-width: 100%;
        border: none;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Mostrar banner
st.image('assets/IMG/banner-img.png')
st.title('APP Anime')

animeFlv= AnimeFLV()


# Cargar desde archivo si existe
try:
    with open('anime_titulos.json', 'r') as f:
        titulos = json.load(f)
except FileNotFoundError:
    titulos = []

# Lógica para agregar nuevos títulos si el archivo está vacío
if not titulos:
    for i in range(1, 250):
        anime_list = animeFlv.list(page=i)
        #print(anime_list)
        titulos.extend(anime.title for anime in anime_list)
        print(titulos)
        print("\n")

    # Guardar los nuevos títulos en un archivo
    with open('anime_titulos.json', 'w') as f:
        json.dump(titulos, f)



# Input para buscar un anime sin un primer elemento
anime = st.selectbox('Buscador de anime', ['Selecciona un anime'] + titulos)



with st.spinner('Buscando anime...'):
    if anime != 'Selecciona un anime':  # Verificar que se ha seleccionado un anime válido
        try:
            # Realizar la búsqueda del anime ingresado
            animeResult = animeFlv.search(anime)
            print(f"anime buscado = {anime}")
            print(f"animeResult: {animeResult}")
            print("\n")

            if not animeResult:
                st.write('No se encontraron resultados para la búsqueda.')
            else:
                # Verificar que animeResult[0] tiene un título
                if animeResult[0] and animeResult[0].title:  
                    # Obtener el índice del anime seleccionado
                    index = titulos.index(animeResult[0].title)
                    animeInfo = animeFlv.get_anime_info(animeResult[0].id)
                    print(f"animeInfo: {animeInfo}") 
                    print("\n")

                    # Verificar que animeInfo tiene episodios
                    if animeInfo.episodes:
                        animeInfo.episodes.reverse()
                        
                        # Mostrar los capítulos disponibles
                        idEpisodios = [episode.id for episode in animeInfo.episodes]
                        seleccionEpisodio = st.selectbox('Selecciona el episodio que quieres ver', idEpisodios)

                        # Mostrar la selección de servidores
                        if seleccionEpisodio:
                            idAnime = animeInfo.id
                            links = animeFlv.get_video_servers(idAnime, seleccionEpisodio)

                            # Validar que 'links' es una lista con al menos un elemento
                            if isinstance(links, list) and len(links) > 0 and isinstance(links[0], list):
                                links = links[0]  # Accedemos a la primera lista dentro de links
                                
                                # Extraer la información de los servidores correctamente
                                serverTitle = [link['server'] for link in links]
                                seleccionServidor = st.selectbox('Selecciona el servidor que quieres ver', serverTitle)

                                if seleccionServidor:
                                    # Obtener el link seleccionado
                                    linkSeleccionado = [link['code'] for link in links if link['server'] == seleccionServidor][0]
                                    
                                    # Incluir el iframe dentro de un div con clase centrada
                                    st.markdown(
                                        f"""
                                        <div class="center-iframe">
                                            <iframe src="{linkSeleccionado}" frameborder="0" allowfullscreen></iframe>
                                        </div>
                                        """, 
                                        unsafe_allow_html=True
                                    )
                                    
                                    st.write(f'Link seleccionado: {linkSeleccionado}')
                            else:
                                st.write('No se encontraron servidores o el formato de datos es incorrecto.')
                    else:
                        st.write('No hay episodios disponibles para este anime.')
                else:
                    st.write('No se encontró un título válido para el anime.')

        except Exception as e:
            st.error(f"Ocurrió un error al buscar el anime: {e}")
    else:
        st.write('Selecciona un anime para comenzar.')
