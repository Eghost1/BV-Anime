from animeflv import AnimeFLV
import streamlit as st 

# Configuración de la página
st.set_page_config(page_title='APP Anime', page_icon=':sushi:', layout='centered')

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

# Instanciar la clase AnimeFLV
animeFlv = AnimeFLV()

# Inicializar el estado de la sesión si no existe
if 'animeInfo' not in st.session_state:
    st.session_state.animeInfo = None
if 'selectedAnime' not in st.session_state:
    st.session_state.selectedAnime = None
if 'selectedEpisodio' not in st.session_state:
    st.session_state.selectedEpisodio = None
if 'selectedServidor' not in st.session_state:
    st.session_state.selectedServidor = None

# Función para reiniciar la búsqueda
def reset_search():
    st.session_state.animeResult = None
    st.session_state.animeInfo = None
    st.session_state.selectedAnime = None
    st.session_state.selectedEpisodio = None
    st.session_state.selectedServidor = None

# Botón para reiniciar la búsqueda
if st.button('Reiniciar Búsqueda'):
    reset_search()

# Input para buscar un anime
anime = st.text_input('Buscador de anime', value=st.session_state.selectedAnime or '')

# Si ya se ha buscado un anime anteriormente y el texto de búsqueda es el mismo, usa los datos almacenados
if st.session_state.animeInfo and anime == st.session_state.selectedAnime:
    animeInfo = st.session_state.animeInfo
    
    # Mostrar selección de episodios
    idEpisodios = [episode.id for episode in animeInfo.episodes]
    seleccionEpisodio = st.selectbox('Selecciona el episodio que quieres ver', idEpisodios, index=idEpisodios.index(st.session_state.selectedEpisodio) if st.session_state.selectedEpisodio in idEpisodios else 0)
    
    # Mostrar la selección de servidores
    if seleccionEpisodio:
        idAnime = animeInfo.id
        links = animeFlv.get_video_servers(idAnime, seleccionEpisodio)
        
        # Mostrar los links obtenidos para ver cómo está estructurado el objeto
        #st.write("Links:", links)  # Para depuración
        
        # Asumimos que `links` es una lista de listas
        if isinstance(links, list) and len(links) > 0 and isinstance(links[0], list):
            links = links[0]  # Accedemos a la primera lista dentro de `links`
        
        # Extraer la información de los servidores correctamente
        serverTitle = [link['server'] for link in links]
        serverUrl = [link['code'] for link in links]
        
        seleccionServidor = st.selectbox('Selecciona el servidor que quieres ver', serverTitle, index=serverTitle.index(st.session_state.selectedServidor) if st.session_state.selectedServidor in serverTitle else 0)
    
        if seleccionServidor:
            linkSeleccionado = [link['code'] for link in links if link['server'] == seleccionServidor][0]
            st.write(f'Link seleccionado: {linkSeleccionado}')
            
            # Incluir el iframe dentro de un div con clase centrada
            st.markdown(
                f"""
                <div class="center-iframe">
                    <iframe src="{linkSeleccionado}" frameborder="0" allowfullscreen></iframe>
                </div>
                """, 
                unsafe_allow_html=True
            )
else:
    if anime:
        with st.spinner('Buscando anime...'):
            with AnimeFLV() as af:
                # Realizar la búsqueda del anime ingresado
                animeResult = af.search(anime)
                
                # Iterar sobre los resultados y extraer los títulos
                if animeResult:
                    animeTitulos = [resultado.title for resultado in animeResult]
                    seleccionAnime = st.selectbox('Selecciona el Anime que quieres ver', animeTitulos, index=animeTitulos.index(st.session_state.selectedAnime) if st.session_state.selectedAnime in animeTitulos else 0)
                    
                    if seleccionAnime:
                        # Obtener el índice del anime seleccionado
                        index = animeTitulos.index(seleccionAnime)
                        # Obtener la información detallada del anime seleccionado
                        animeInfo = af.get_anime_info(animeResult[index].id)
                        animeInfo.episodes.reverse()
                        
                        # Almacenar la información del anime en el estado de la sesión
                        st.session_state.animeInfo = animeInfo
                        st.session_state.selectedAnime = seleccionAnime
                        
                        # Mostrar los capítulos disponibles 
                        idEpisodios = [episode.id for episode in animeInfo.episodes]
                        seleccionEpisodio = st.selectbox('Selecciona el episodio que quieres ver', idEpisodios, index=idEpisodios.index(st.session_state.selectedEpisodio) if st.session_state.selectedEpisodio in idEpisodios else 0)
                        
                        # Mostrar la selección de servidores
                        if seleccionEpisodio:
                            idAnime = animeInfo.id
                            links = af.get_video_servers(idAnime, seleccionEpisodio)
                            
                            # Mostrar los links obtenidos para ver cómo está estructurado el objeto
                            #st.write("Links:", links)  # Para depuración
                            
                            # Asumimos que `links` es una lista de listas
                            if isinstance(links, list) and len(links) > 0 and isinstance(links[0], list):
                                links = links[0]  # Accedemos a la primera lista dentro de `links`
                            
                            # Extraer la información de los servidores correctamente
                            serverTitle = [link['server'] for link in links]
                            serverUrl = [link['code'] for link in links]
                            
                            seleccionServidor = st.selectbox('Selecciona el servidor que quieres ver', serverTitle, index=serverTitle.index(st.session_state.selectedServidor) if st.session_state.selectedServidor in serverTitle else 0)
                        
                            if seleccionServidor:
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
                    st.write('No se encontraron animes')
