# Acres99

## Features

- [x] Add `logging` in every steps.
- [x] Solve `drop_duplicates=True` issue.
- [x] Understand why `drop_duplicates=True` does not remove the newer duplicate rows from the DataFrames. For reference see [logs](../logs).
- [x] If `expand=False` check that CSV file is not exists. If exists raise **`FileExistsError`**.
- [x] Also, add a parameter to `export_dfs` method which rewrite the **facets DataFrames**.
- [x] ~~Create a function which fetches the data from website and store them in CSV formate periodically.~~
- [x] Handle exceptions for validation of Pydantic.
- [ ] Make the code more comprehensive and modular. Now it is more coupled and not easy to use individually and understand.
- [x] If any error occurs after fetching the data show a button to download the un-cleaned data and then create a page to upload those data to clean.
- [x] Add a button to download the raw response (without validating through Pydantic).
- [x] Add new features to `SRP` class to get a better data for model building and data analysis.
- [x] Check **how to identify the rental apartments/properties**.
- [x] ~~Show the logging into the app.~~

# New objectives

Now I want to convert this project into Streamlit app.

- [x] Find all the cities id to create URLs.
- [x] Create a separate module which handles the DataFrames operations.
- [x] Create class to deal with API requests.
- [x] Add a parameter to pass the city ID.

## TODO

- [x] Improve logging.

  - Only one logging file will be there.
  - More comprehensive logging message.

- [x] Tackle with first data saving error. (No column to parse in the csv file.)
