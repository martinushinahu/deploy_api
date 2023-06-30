from fastapi import FastAPI
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pydantic import BaseModel
from fastapi import HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


# Crear la aplicación FastAPI
app = FastAPI()

# Obtener la ruta absoluta del directorio actual
base_dir = os.path.dirname(os.path.abspath(__file__))

# Construir la ruta absoluta de los archivos de datos
movies_file = os.path.join(base_dir, 'data', 'movies_final.csv')
credits_file = os.path.join(base_dir, 'data', 'credits_final.csv')

# Leer los archivos CSV
dataset = pd.read_csv(movies_file, low_memory=False)
df_actor_and_director = pd.read_csv(credits_file, low_memory=False)




'''Endpoint para la función def cantidad_filmaciones_mes( Mes )'''
# Filtrar las filas que contienen datos no válidos en la columna 'release_date'
dataset = dataset[dataset['release_date'].apply(lambda x: isinstance(x, str) and len(x) == 10)]

# Convertir la columna 'release_date' al formato de fecha
dataset['release_date'] = pd.to_datetime(dataset['release_date'])

# Extraer el mes de la columna 'release_date'
dataset['mes_estreno'] = dataset['release_date'].dt.month


# Diccionario para mapear números de mes a nombres de mes
nombres_meses = {
    1: "enero",
    2: "febrero",
    3: "marzo",
    4: "abril",
    5: "mayo",
    6: "junio",
    7: "julio",
    8: "agosto",
    9: "septiembre",
    10: "octubre",
    11: "noviembre",
    12: "diciembre"
}

# 1.Función para contar la cantidad de películas estrenadas en un mes específico
def contar_peliculas_mes(mes):
    # Obtener el número de mes correspondiente al nombre del mes
    numero_mes = None
    for key, value in nombres_meses.items():
        if mes.lower() == value:
            numero_mes = key
            break

    if numero_mes is None:
        raise ValueError(f"Nombre de mes inválido: {mes}")

    cantidad = len(dataset[dataset['mes_estreno'] == numero_mes])
    return cantidad, mes.capitalize()






# Endpoint para obtener la cantidad de películas estrenadas en un mes
@app.get('/cantidad_filmaciones_mes')
def cantidad_filmaciones_mes(mes: str):
    cantidad, nombre_mes = contar_peliculas_mes(mes)
    return {'mensaje': f'{cantidad} cantidad de películas fueron estrenadas en el mes de {nombre_mes}'}

'''Ahora hacemos el Endpoint para la sigue que es def cantidad_filmaciones_dia( Dia )'''

# Diccionario para mapear nombres de día a números de día
nombres_dias = {
    "lunes": 0,
    "martes": 1,
    "miercoles": 2,
    "jueves": 3,
    "viernes": 4,
    "sabado": 5,
    "domingo": 6
}

# 2. Función para contar la cantidad de películas estrenadas en un día específico
def contar_peliculas_dia(dia):
    # Obtener el número de día correspondiente al nombre del día
    numero_dia = nombres_dias.get(dia.lower())
    if numero_dia is None:
        raise ValueError(f"Nombre de día inválido: {dia}")

    cantidad = len(dataset[dataset['release_date'].dt.dayofweek == numero_dia])
    return cantidad, dia.capitalize()

# Endpoint para obtener la cantidad de películas estrenadas en un día
@app.get('/cantidad_filmaciones_dia')
def cantidad_filmaciones_dia(dia: str):
    cantidad, nombre_dia = contar_peliculas_dia(dia)
    return {'mensaje': f'{cantidad} cantidad de películas fueron estrenadas en los días {nombre_dia}'}

'''Ahora el Endpoint def score_titulo( titulo_de_la_filmación ) '''

#3. Función para obtener el título, el año de estreno y el score de una filmación
def score_titulo(titulo_de_la_filmacion):
    fila = dataset.loc[dataset['title'] == titulo_de_la_filmacion]
    if fila.empty:
        return {"mensaje": "No se encontró ninguna filmación con ese título"}
    
    titulo = fila['title'].values[0]
    año_estreno = fila['release_year'].values[0]
    score = fila['popularity'].values[0]
    
    return {"mensaje": f"La película {titulo} fue estrenada en el año {año_estreno} con un score/popularidad de {score}"}

@app.get('/score_titulo')
def obtener_score_titulo(titulo_de_la_filmacion: str):
    resultado = score_titulo(titulo_de_la_filmacion)
    return resultado



'''4.Ahora el Endpoint def votos_titulo( titulo_de_la_filmación ):'''

''' verificamos si se encontró alguna filmación con el título proporcionado. Si 
no se encuentra ninguna coincidencia, se devuelve un mensaje indicando que no se encontró ninguna filmación.'''

def votos_titulo(titulo_de_la_filmacion):
    fila = dataset.loc[dataset['title'] == titulo_de_la_filmacion]
    if fila.empty:
        return {"mensaje": "No se encontró ninguna filmación con ese título"}

    votos = int(fila['vote_count'].values[0])
    promedio_votos = fila['vote_average'].values[0]

    if votos < 2000:
        return {"mensaje": "La filmación no cumple con la cantidad mínima de valoraciones"}

    titulo = fila['title'].values[0]

    return {
        "mensaje": f"La película {titulo} cuenta con un total de {votos} votos y un promedio de {promedio_votos} votos."
    }


#Endpointdef votos_titulo( titulo_de_la_filmación ):
@app.get('/votos_titulo')
def obtener_votos_titulo(titulo_de_la_filmacion: str):
    resultado = votos_titulo(titulo_de_la_filmacion)
    return resultado


'''5.Continuamos con el Endpoint de get_actores'''

def get_actor(nombre_actor):
    actor_filmaciones = df_actor_and_director[df_actor_and_director['name_cast'] == nombre_actor]
    
    if actor_filmaciones.empty:
        return {"mensaje": f"No se encontró al actor {nombre_actor} en ninguna filmación."}
    
    actor_movies_id = actor_filmaciones['movies_id'].tolist()
    actor_peliculas = dataset[dataset['movies_id'].isin(actor_movies_id)]
    cantidad_filmaciones = len(actor_peliculas)
    
    # Filtrar los valores numéricos de la columna 'return' y convertirlos a tipo float
    actor_peliculas['return'] = actor_peliculas['return'].apply(lambda x: float(x) if x.replace('.', '', 1).isdigit() else 0)
    
    retorno_total = actor_peliculas['return'].sum()
    retorno_promedio = retorno_total / cantidad_filmaciones if cantidad_filmaciones > 0 else 0  
    retorno_total = round(retorno_total, 2)  # Redondear a 2 decimales
    retorno_promedio = round(retorno_promedio, 2)  # Redondear a 2 decimales
    
    return {
        "mensaje": f"El actor {nombre_actor} ha participado en {cantidad_filmaciones} filmaciones. "
                   f"Ha obtenido un retorno total de ${retorno_total} millones de dólares con un promedio de ${retorno_promedio} millones dólares por filmación."
    }


@app.get('/get_actor')
def obtener_info_actor(nombre_actor: str):
    resultado = get_actor(nombre_actor)
    return resultado

'''6.ahora con def get_director( nombre_director )'''


def get_director(nombre_director):
    # Filtrar el dataset df_actor_and_director para obtener las filas correspondientes al director
    director_filas = df_actor_and_director[(df_actor_and_director['name_crew'] == nombre_director) & (df_actor_and_director['job'] == 'Director')]

    # Obtener la lista de movies_id del director filtrado
    director_movies_id = director_filas['movies_id'].tolist()

    # Filtrar el dataset dataset utilizando los movies_id obtenidos
    director_peliculas = dataset[dataset['movies_id'].isin(director_movies_id)]

    # Crear una lista de diccionarios con la información requerida para cada película del director
    peliculas_info = []
    for _, fila in director_peliculas.iterrows():
        fecha_lanzamiento = pd.to_datetime(fila['release_date']).strftime("%Y-%m-%d")  # Convertir a formato de fecha deseado

        pelicula_info = {
            'titulo': fila['title'],
            'fecha_lanzamiento': fecha_lanzamiento,
            'retorno_individual': fila['return'],
            'costo': fila['budget'],
            'ganancia': fila['revenue']
        }
        peliculas_info.append(pelicula_info)

    # Retornar el resultado con la información del éxito del director y la lista de información de películas
    return {
        'director': nombre_director,
        'exito': len(director_peliculas),
        'peliculas': peliculas_info
    }


@app.get('/get_director')
def obtener_info_director(nombre_director: str):
    resultado = get_director(nombre_director)
    return resultado



'''proceso de machine learning'''

# Preprocesar los datos y obtener la matriz de características TF-IDF
tfidf = TfidfVectorizer(stop_words='english')
dataset['overview'] = dataset['overview'].fillna('')
tfidf_matrix = tfidf.fit_transform(dataset['overview'])
# Calcular la similitud coseno entre las películas
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)



'''MachineLearnig'''

# Función para obtener las películas recomendadas
def obtener_recomendaciones(titulo, cosine_sim, movies_data):
    indices = pd.Series(movies_data.index, index=movies_data['title']).drop_duplicates()
    idx = indices[titulo]

    scores = list(enumerate(cosine_sim[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in scores[1:6]]
    recomendaciones = movies_data['title'].iloc[top_indices].tolist()

    return recomendaciones

class TituloPelicula(BaseModel):
    titulo: str

@app.get('/recomendar_peliculas')
def recomendar_peliculas(titulo_pelicula: str = Query(..., description='Título de la película')):
    if titulo_pelicula in dataset['title'].values:
        recomendaciones = obtener_recomendaciones(titulo_pelicula, cosine_sim, dataset)
        return {
            'titulo_pelicula': titulo_pelicula,
            'recomendaciones': recomendaciones
        }
    else:
        raise HTTPException(status_code=404, detail='La película no fue encontrada en la base de datos.')



# Ruta estática para los archivos CSS
static_dir = os.path.join(os.getcwd(), "style")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

images_dir = os.path.join(os.getcwd(),  "img")
app.mount("/img", StaticFiles(directory=images_dir), name="images")

@app.get("/", response_class=HTMLResponse)
def read_index():
    with open(os.path.join(os.getcwd(),  "templates", "index.html"), "r", encoding="utf-8") as file:
        content = file.read()
    return content

'''
cantidad_filmaciones_mes?mes={mes}
cantidad_filmaciones_dia?ia={dia}
score_titulo?titulo_de_la_filmacion={titulo}
votos_titulo?titulo_de_la_filmacion={titulo}
get_actor?nombre_actor={nombre_actor}
get_director?nombre_director={nombre_director}
recomendar_peliculas?titulo_pelicula=
'''
