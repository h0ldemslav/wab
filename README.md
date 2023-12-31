# Webové aplikace backend (WAB 2023) - Mendelu

### Použité technologie:
- [FastAPI](https://fastapi.tiangolo.com)
- [pdm](https://pdm-project.org/latest/) - moderní Python package manager

### Založení projektu pomocí pdm
Instalace pdm
```shell
pip install --user pdm
```

Vytvoření projeku. Vygeneruje základní strukturu projektu, popis projektu a dependencies je v souboru `pyproject.toml`, který je podobný `package.json`
```shell
pdm init
```

Přidání dependency
```shell
pdm add fastapi
pdm add "uvicorn[standard]"
```

Přidání development dependency (nebude součástí produkčního buildu)
```shell
pdm add -dG test pytest
```

Pak `pyproject.toml` bude vypadat
```shell
[tool.pdm.dev-dependencies]
test = ["pytest"]
```

Mazání dependency
```shell
pdm remove requests
# Development dependency
pdm remove -dG test pytest
```

Přidání scriptů (soubor `pyproject.toml`)
```shell
[tool.pdm.scripts]
dev = "uvicorn main:app --reload"
test = "pytest"
```

Spuštění scriptu
```shell
pdm run dev
```

Přidání dependencies (použije se soubor `pdm.lock`, případně `pyproject.toml`, kde máš seznam dependecies)
```shell
pdm install
```

**Kam se instalují ty dependencies?** Z dokumentace:

**Virtual environments will be used if the project interpreter (the interpreter stored in `.pdm-python`, which can be checked by `pdm info`) is from a virtualenv.** ([zdroj](https://pdm-project.org/latest/usage/venv/))
