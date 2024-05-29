FROM ubuntu:latest

# Instalar Make y Python
RUN apt-get update && apt-get install -y \
    make \
    python3 \
    python3-pip

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias de Flask
COPY ./gateway/requirements.txt /app/gateway/requirements.txt
RUN pip3 install -r /app/gateway/requirements.txt

# Comando para lanzar tu backend Flask
CMD ["make", "-C", "gateway", "run"]