from flask import Flask, jsonify
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os

app = Flask(__name__)

@app.route('/run-notebook', methods=['GET'])
def run_notebook():
    notebook_filename = "notebook.ipynb"

    with open(notebook_filename, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    executor = ExecutePreprocessor(timeout=600, kernel_name="python3")
    executor.preprocess(notebook)

    # Extract output from the last cell
    for cell in notebook.cells:
        if cell.cell_type == "code" and "outputs" in cell:
            for output in cell.outputs:
                if "text" in output:
                    return jsonify({"output": output["text"]})

                if "data" in output and "text/plain" in output["data"]:
                    return jsonify(json.loads(output["data"]["text/plain"]))

    return jsonify({"error": "No output found"})

if __name__ == "__main__":
    app.run(debug=True)
