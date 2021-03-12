FROM python:3-alpine
WORKDIR /usr/src/appIMC
EXPOSE 5080
COPY instala.txt .
RUN pip install -qr instala.txt
COPY appIMC .
CMD [ "python", "./imc.py" ]