# NativeSQL_to_BigQuary
Convert Native SQL scripts to Google BigQuary 

# Snowflake SQL to BigQuery SQL Converter

This codebase contains a Python script for converting Snowflake SQL queries to BigQuery SQL queries. The script processes a collection of complex SQL files, performs the necessary conversions, and generates corresponding BigQuery-compatible SQL files. It also creates diff files to highlight the differences between the original and converted SQL.

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [License](#license)

## Overview

The codebase comprises several Python scripts that work together to perform the SQL conversion:

- `function_convert.py`: Contains functions for mapping Snowflake functions to BigQuery functions.
- `pre_process.py`: Handles preprocessing tasks, such as transforming double colons to standard cast expressions.
- `convert_sql.py`: The main conversion logic resides here, including function mapping, SQL conversion, file saving, and diff generation.
- `main.py`: The script that orchestrates the entire conversion process. It reads Snowflake SQL files from a specified directory, applies the conversion, and generates corresponding BigQuery SQL files.

## Setup

1. Clone this repository to your local machine.
2. Ensure you have Python 3.x installed.
3. Install the required Python packages by running:
   ```
   pip install pandas
   ```

## Usage

1. Place your Snowflake SQL files in the `Complex_SQL` directory.
2. Modify the `file_path`, `out_file_path`, and `diff_file_path` variables in `main.py` to match your file paths.
3. Run the conversion script by executing:
   ```
   python main.py
   ```

## File Structure

The structure of the codebase is as follows:

```
SQL_To_BigQ_Converter/
|-- function_convert.py
|-- pre_process.py
|-- convert_sql.py
|-- main.py
|-- Complex_SQL/
|   |-- sql_file_1.sql
|   |-- sql_file_2.sql
|   |-- ...
|-- Output_Complex/
|   |-- converted_sql_file_1.sql
|   |-- converted_sql_file_2.sql
|   |-- ...
|-- diffs/
|   |-- sql_file_1_diff.txt
|   |-- sql_file_2_diff.txt
|   |-- ...
|-- venv/
|   |-- Func_Dict/
|       |-- sql_file_1.csv
|       |-- sql_file_2.csv
|       |-- ...
|-- README.md
```

## Contributing

Contributions are welcome! If you have improvements or bug fixes, feel free to submit a pull request. For major changes, please open an issue to discuss your ideas first.

## License

This project is licensed under the [MIT License](LICENSE).

---

Feel free to customize this README to include more specific information about your project, such as details about the conversion rules, Snowflake and BigQuery function mappings, and any other relevant information.
