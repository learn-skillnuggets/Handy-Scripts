from flask import Flask, request, render_template
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = []
    search_string = ""
    if request.method == "POST":
        search_string = request.form.get("search_string", "").strip().lower()
        if search_string:
            folder_path = os.getcwd()  # Current working directory
            files = [f for f in os.listdir(folder_path) if f.endswith('.cfg')]
            
            for file in files:
                # Check if the search string is in the file name
                if search_string in file.lower():
                    result.append({"file_name": file, "reason": "Found in file name"})
                    continue  # Stop further processing for this file
                
                # Check if the search string is in the file content
                file_path = os.path.join(folder_path, file)
                try:
                    with open(file_path, 'r') as f:
                        for line in f:
                            if search_string in line.lower():
                                result.append({"file_name": file, "reason": "Found in file content"})
                                break  # Stop reading this file once a match is found
                except Exception as e:
                    result.append({"file_name": file, "reason": f"Error reading file: {str(e)}"})

    return render_template("index.html", result=result, search_string=search_string)

@app.route("/view/<file_name>")
def view_file(file_name):
    try:
        folder_path = os.getcwd()  # Current working directory
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as f:
            content = f.read()
        return render_template("view_file.html", file_name=file_name, content=content)
    except Exception as e:
        return f"Error opening file: {str(e)}"

if __name__ == "__main__":
    app.run(port=5001, debug=True)  # Use port 5001 to avoid conflicts
