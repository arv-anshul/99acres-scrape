.ONESHELL:

SHELL := /bin/bash

STREAMLIT_APP = Fetch_Properties_Data.py

streamlit: $(STREAMLIT_APP)  ## Run the streamlit app
	streamlit run $<

venv:  ## Create a new virtual environment, with default name '.venv'.
	@$(PYTHON) -m venv "$(PYTHON_VENV)" || (echo "Failed to create virtual environment" && exit 1); \
	echo >&2 "Created venv in '$(PYTHON_VENV)'"; \
	echo -e "Activate your env with the command:"; \
	echo -e "\033[1;32m$$\033[0m \033[31msource $(PYTHON_VENV)/bin/activate\033[0m"; \
