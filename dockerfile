# Vyrobi image Pythonu
FROM python:3.11

# Nainstalujeme pdm
RUN pip install pdm

# Vypisu si korenovy adresar; udela pri spusteni kontejneru
CMD ls -al