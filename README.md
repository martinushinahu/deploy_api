#  API de Recomendación de Películas
- Desarrollado por Martin Ushinahua Quinteros.

Bienvenidos a La API de Recomendación de Películas, esta es una herramienta en un servicio web que te permite obtener recomendaciones de películas basadas en un título de película ingresado.
Utiliza un algoritmo de similitud coseno para encontrar películas similares y devuelve una lista de recomendaciones.
Este proyecto es 100% gratuito y de código abierto.

![](https://github.com/martinushinahu/deploy_api/blob/main/backend/screenshot/index.png)

## 🌟 Funciones
  - Cantidad de filmaciones por mes
  - Cantidad de filmaciones por día
  - Score por filmación
  - Votos por filmación
  - Participación del actor
  - Películas que ha dirigido el director
  - Recomendación de películas

Requisitos
- Python 3.7 o superior
- Bibliotecas de Python mencionadas en el archivo `requirements.txt`

## 📖 Modo de empleo:
Super sencillo el uso de la API, por eso la implementación de la interfaz, solo rellene
la casilla de la consulta que desea saber y le da en consultar, y el resultado se le mostrará
en la caja de la parte de abajo.

## 🛠️ Instalación

1. Clona este repositorio en tu máquina local.

2. Crea y activa un entorno virtual:

   ```shell
   python -m venv venv
    source venv/bin/activate  # En Linux/Mac
    venv\Scripts\activate  # En Windows

3. Instala las dependencias utilizando el archivo requirements.txt

   ```shell
    pip install -r requirements.txt

## 🖥️ Uso

 1. Inicia la API ejecutando el archivo main.py

    ```shell
      uvicorn main:app --reload

2. La API estará disponible en http://localhost:8000. Puedes acceder a la interfaz de la API desde tu navegador.

3. Interactúa con la API mediante los formularios disponibles:
   
  - Cantidad de filmaciones por mes: Ingresa un mes y obtén la cantidad de filmaciones realizadas en ese mes.
  - Cantidad de filmaciones por día: Ingresa un día y obtén la cantidad de filmaciones realizadas en ese día.
  - Score por filmación: Ingresa un título de película y obtén el score de esa película.
  - Votos por filmación: Ingresa un título de película y obtén la cantidad de votos de esa película.
  - Participación del actor: Ingresa el nombre de un actor y obtén las participaciones en películas de ese actor.
  - Películas que ha dirigido el director: Ingresa el nombre de un director y obtén las películas que ha dirigido.
  - Recomendación de películas: Ingresa el título de una película y obtén una lista de recomendaciones similares.


    
## 👥 Contribución
Las contribuciones son bienvenidas y alentadas! Si deseas contribuir a este proyecto, puedes seguir los siguientes pasos:

1. Haz un fork de este repositorio.
2. Clona tu repositorio fork en tu máquina local.
3. Crea una nueva rama para tu contribución:
     ```shell
     git checkout -b mi-nueva-funcionalidad
     
4. Realiza los cambios necesarios y realiza commits con mensajes descriptivos.
5. Empuja tus cambios a tu repositorio fork.
   ```shell
   git push origin mi-nueva-funcional

  
## 📜 Licencia










