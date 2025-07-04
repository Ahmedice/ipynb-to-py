import nbformat
from nbconvert import PythonExporter
import sys
import os

def convert_notebook_to_script(notebook_path):
    if not notebook_path.endswith(".ipynb"):
        print("❌ the file is not in .ipynb extention")
        return

    output_path = notebook_path.replace(".ipynb", ".py")

    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)

        exporter = PythonExporter()
        script, _ = exporter.from_notebook_node(notebook)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(script)

        print(f"✅ sucssefully : {output_path}")

    except Exception as e:
        print(f"❌ Error  {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("⚠️ enter the Notebook path")
    else:
        notebook_path = " ".join(sys.argv[1:])  # يدعم المسارات والأسماء بالفراغات
        convert_notebook_to_script(notebook_path)
