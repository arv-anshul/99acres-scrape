# Scrape 99Acres

> [!IMPORTANT]
>
> **DISCLAIMER:** This project is only for education purpose.

### Why this project?

I am working on a real estate project. So I need real-time data for that so I write a program to gather the data for this project and convert it into a web-app using streamlit.

Check out my Data Analysis on the scrapped data [here](https://github.com/arv-anshul/campusx-project-notebooks).

### Documentation

Documentation for this project is available in [🗒️ wiki](https://github.com/arv-anshul/99acres-scrape/wiki) section.

### Techs

1. Python>=3.11
2. Asynchronous Programming
3. Streamlit
4. Http Requests
5. Pydantic

### Setup

1. Install all the required packages.

```sh
pip install -r requirements.txt
```

### Usage

1. Run the streamlit app.

```sh
streamlit run app.py
```

2. Goto URL `http://localhost:8501/`.
3. Fill the form: **Select the city** which you want to scrape and submit.
4. After some backend processing; **a download button** will appear, click it to download the scrapped data.

### Disclaimer

As I wanted to scrape the data from 99Acres website. I am ensuring that I am not performing any illegal activity using this data. I used this data in my project to build some ML model and perform some data analysis.
