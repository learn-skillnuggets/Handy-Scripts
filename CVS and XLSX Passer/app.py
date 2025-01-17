from flask import Flask, request, render_template
import os
import pandas as pd
import re

app = Flask(__name__)

def normalize_text(text):
    """Normalize text by removing spaces and special characters, and converting to lowercase."""
    if pd.isna(text):  # Handle NaN values
        return ""
    return re.sub(r'\W+', '', str(text).replace(" ", "").lower())

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        search_string = request.form.get("search_string")
        if search_string:
            folder_path = os.getcwd()  # Current working directory
            files = [f for f in os.listdir(folder_path) if f.endswith('.csv') or f.endswith('.xlsx')]
            search_string_normalized = normalize_text(search_string)
            matches = []

            for file in files:
                file_path = os.path.join(folder_path, file)
                try:
                    # Read files
                    if file.endswith('.csv'):
                        df = pd.read_csv(file_path, dtype=str)
                    elif file.endswith('.xlsx'):
                        df = pd.read_excel(file_path, dtype=str, engine='openpyxl')
                    
                    df.fillna("", inplace=True)
                    for index, row in df.iterrows():
                        if any(search_string_normalized in normalize_text(cell) for cell in row):
                            # Create a dictionary of non-empty fields for human-readable output
                            non_empty_fields = {col: row[col] for col in row.index if row[col]}
                            match_info = f"File: {file}, Row {index + 1} -> {non_empty_fields}"
                            matches.append(match_info)
                except Exception as e:
                    matches.append(f"Error reading file {file}: {e}")

            if matches:
                result = "\n\n".join(matches)
            else:
                result = f"No matches found for '{search_string}'."
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
