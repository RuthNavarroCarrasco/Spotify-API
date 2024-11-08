PYTHON := python3
APP_PATH := src/app/app.py

.PHONY: setup
setup:
	# Instala pyenv si no está instalado
	command -v pyenv >/dev/null 2>&1 || { echo >&2 "pyenv no está instalado. Instalando pyenv..."; curl https://pyenv.run | bash; }
	
	# Usa pyenv para establecer la versión correcta de Python
	pyenv install -s 3.10.0
	pyenv local 3.10.0
	
	# Instala poetry si no está instalado
	command -v poetry >/dev/null 2>&1 || { echo >&2 "Poetry no está instalado. Instalando Poetry..."; curl -sSL https://install.python-poetry.org | python3 -; }
	
	# Instala las dependencias con poetry
	poetry install

.PHONY: shell
shell:
	poetry shell

.PHONY: run
run:
	$(PYTHON) $(APP_PATH)

.PHONY: clean
clean:
	rm -rf src/app/__pycache__
	rm -rf .venv

.PHONY: all
all: setup
