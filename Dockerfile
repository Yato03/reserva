# Usa una imagen base de Python
FROM python:3.9

RUN apt-get update && apt-get install -y locales \
    && echo "es_ES.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen es_ES.UTF-8 \
    && update-locale LANG=es_ES.UTF-8 

ENV LANG es_ES.UTF-8 
ENV LANGUAGE es_ES:es 
ENV LC_ALL es_ES.UTF-8

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo requirements.txt y lo instala
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia el resto del código
COPY . .

# Expone el puerto
EXPOSE 8000

# Comando por defecto para ejecutar el servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
