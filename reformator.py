import sys
import os
import json
import shutil
import glob
import re

development = True 
configuration_file = os.path.sep.join(("data", "configurations.json"))

def load_configurations():
    location_current_script = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    configuration_path = os.path.join(location_current_script, configuration_file)
    with open(configuration_path) as json_file:
        data_json = json.load(json_file)
        
        return data_json
    return None

def get_file_name_with_extension(input_file_path):
    return input_file_path.rsplit(os.sep,1)[-1]

def get_file_name_without_extension(input_file_path):
    return os.path.splitext(input_file_path.rsplit(os.sep,1)[-1])[0]

def get_file_name_extension(input_file_path):
    return os.path.splitext(input_file_path.rsplit(os.sep,1)[-1])[1]

def get_file_backup_path(input_file_path, output_folder_path, addendum = None):
    addendum_string = addendum or ""
    new_file_name = get_file_name_without_extension(input_file_path) + str(addendum_string) + get_file_name_extension(input_file_path)
    backup_path = os.path.join(output_folder_path, new_file_name)

    return backup_path

def clean_up_path(path):
    os.chdir(path)
    files_search_string = os.path.sep.join((path, "*.*"))
    file_list = glob.glob(files_search_string)
    for f in file_list:
        os.remove(f)

def get_addendum(id):
    zeros = 5 - len(str(id))
    return "_" + str(id).zfill(zeros)

def main():
    configurations = load_configurations()

    for configuration in configurations:
        clean_up_path(configuration["output_folder_path"])
        file_backup_path = get_file_backup_path(configuration["input_file_path"], configuration["output_folder_path"], get_addendum(0))
        shutil.copy(configuration["input_file_path"], file_backup_path)
        text = ""
        with open(configuration["input_file_path"], mode = "r", encoding = "utf-8") as input_file:
            text = input_file.read()
        if text:
            id = 0
            for transformation in configuration["transformations"]:
                regex = re.compile(transformation["oldvalue"])
                text = regex.sub(transformation["newvalue"], text)
                id += 1
                file_transformation_path = get_file_backup_path(configuration["input_file_path"], configuration["output_folder_path"], get_addendum(id))
                with open(file_transformation_path, mode = "w", encoding = "utf-8") as output_file:
                    output_file.write(text)

if __name__ == "__main__":
    main()

