from uuid import uuid4
from fpdf import FPDF
import shutil
import pathlib
import os
import json

FILES_DIR = "files"
YAML_STR = """
---
 doe: "a deer, a female deer"
 ray: "a drop of golden sun"
 pi: 3.14159
 xmas: true
 french-hens: 3
 calling-birds:
   - huey
   - dewey
   - louie
   - fred
 xmas-fifth-day:
   calling-birds: four
   french-hens: 3
   golden-rings: 5
   partridges:
     count: 1
     location: "a pear tree"
   turtle-doves: two
"""


def get_dir_path(data_dir):
    """
    Generate parent (dummy) files dir
    """
    dir_path = get_files_dir(data_dir)
    # Create dir
    pathlib.Path(dir_path).mkdir(parents=True, exist_ok=True)
    return dir_path


def get_files_dir(data_dir):
    return os.path.join(data_dir, FILES_DIR)


def get_file_path(data_dir, extension=None):
    """
    Generate random file name
    """
    if extension:
        return os.path.join(get_dir_path(data_dir), uuid4().hex) + "." + extension
    else:
        return os.path.join(get_dir_path(data_dir), uuid4().hex)


def generate_txt_file(data_dir: str):
    """
    Generate random txt file
    """
    file_path = get_file_path(data_dir, extension="txt")
    return {"file_handle": open(file_path, "w+"), "file_type": "txt"}


def generate_zip_file(data_dir: str):
    """
    Generate zip file
    """
    zip_file_path = get_file_path(data_dir)
    # Create a zip file out of a dummy(empty) dir
    dummy_dir_path = os.path.join(get_files_dir(data_dir), "dummy")
    pathlib.Path(dummy_dir_path).mkdir(parents=True, exist_ok=True)
    # Create zip file
    file_name = shutil.make_archive(zip_file_path, "zip", dummy_dir_path)
    return {"file_handle": open(file_name, "r"), "file_type": "zip"}


def generate_pdf_file(data_dir: str):
    """
    Generate random pdf file
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_xy(0, 0)
    pdf.set_font("arial", "B", 13.0)
    pdf.cell(ln=0, h=5.0, align="L", w=0, txt="Hello", border=0)
    file_path = get_file_path(data_dir, extension="pdf")
    try:
        pdf.output(file_path, "F")
    except Exception as e:
        print(e)
    return {
        "file_handle": open(file_path, "r", encoding="utf-8", errors="ignore"),
        "file_type": "pdf",
    }


def generate_yaml_file(data_dir: str):
    """
    Generate yaml file
    """
    file_path = get_file_path(data_dir, extension="yaml")
    fp = None
    try:
        fp = open(file_path, "w+", encoding="utf-8")
        fp.write(YAML_STR)
        fp.close()
    except Exception as e:
        print(e)
    # finally:
    #     f.close()
    fp1 = open(file_path, "r")
    return {"file_handle": fp1, "file_type": "yaml"}


def generate_json_file(data_dir: str):
    """
    Generate json file
    """
    file_path = get_file_path(data_dir, extension="json")
    dicT = {"key": "value"}
    fp = None
    try:
        fp = open(file_path, "w")
        json.dump(dicT, fp)
        fp.close()
    except Exception as e:
        print(e)
    # finally:
    #     fp.close()
    fp1 = open(file_path, "r")
    return {"file_handle": fp1, "file_type": "json"}


def get_generated_file_handles(data_dir: str, file_type: str):
    """
    Generate and return file handles
    """
    all_file_handles = []
    if file_type == "json":
        return generate_json_file(data_dir)
    elif file_type == "txt":
        return generate_txt_file(data_dir)
    elif file_type == "yaml":
        return generate_yaml_file(data_dir)
    elif file_type == "zip":
        return generate_zip_file(data_dir)
    elif file_type == "pdf":
        return generate_pdf_file(data_dir)
    else:
        json_file_handle = generate_json_file(data_dir)
        all_file_handles.append(json_file_handle)
        yaml_file_handle = generate_yaml_file(data_dir)
        all_file_handles.append(yaml_file_handle)
        zip_file_handle = generate_zip_file(data_dir)
        all_file_handles.append(zip_file_handle)
        pdf_file_handle = generate_pdf_file(data_dir)
        all_file_handles.append(pdf_file_handle)

        return all_file_handles


if __name__ == "__main__":
    data_dir = "/home/shashank/Desktop/apihq/logs/test"
    generate_zip_file(data_dir)
