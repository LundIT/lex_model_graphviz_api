import os
import subprocess

# This part implements the section in the beginning, where we have to import the foreign keys



def get_import_for_foreign_keys(json, columns):
    imports = []
    #columns = json['models'][class_name]['columns']
    for line in columns:
        if line['data_type'] == 'ForeignKey':
            to_class = line['to']
            for model in json['models']:
                if model['class']['name'] == to_class:
                    file_path_of_to_class = model['class']['settings']['file_path']
                    imports.append(f"from generic_app.submodels.{json['settings']['project_name']}.{file_path_of_to_class}.{to_class} import {to_class}")

    return imports

# As we have to take care of python indent, we have to create indent ourselves. This function defines one 4 space indent
def indent():
    return "    "

# This function takes a defined json, a class name, the classes columns, its settings and the general project settings and creates the string for of the class as a Django Python module
def class_to_lex_file(json, class_name, columns, settings, project_settings):
    is_dependency_analysis_mixin = settings['is_dependency_anlysis_mixin'] if 'is_dependency_anlysis_mixin' in settings else None
    is_upload_model = settings['is_upload_model'] if 'is_upload_model' in settings else None
    is_calculated_model = settings['is_calculatable'] if 'is_calculatable' in settings else None
    defining_fields = settings['defining_fields'] if 'defining_fields' in settings else None

    lines = []
    lines.append("from generic_app.models import *\n")
    lines += get_import_for_foreign_keys(json, columns)
    lines.append(f"class {class_name}("
                 f"{'DependenyAnalsisMixin, ' if is_dependency_analysis_mixin else ''}"
                 f"{'UploadModelMixin, ' if is_upload_model else ''}"
                 f"{'CalculatedModelMixin, ' if is_calculated_model else ''}"
                 f"Model):")
    class_lines = []
    class_lines.append(indent())
    for line in columns:

        if line['data_type'] == 'ForeignKey':
            class_lines.append(f"{line['column_name']} = {line['data_type']}(to={line['to']}, on_delete={line['on_delete']})")
        else:
            class_lines.append(f"{line['column_name']} = {line['data_type']}(default={line['default_value']})")
    class_lines.append("")
    if is_dependency_analysis_mixin:
        class_lines.append("def directly_dependent_entries(self):")
        class_lines.append(f"{indent()}# TODO please return the objects that should be updated once the model is saved")
        class_lines.append(f"{indent()}return []\n")

    if is_upload_model:
        class_lines.append("def update(self):")
        class_lines.append(f"{indent()}# TODO specify what you want to do once the model has been saved")
        class_lines.append(f"{indent()}pass\n")

    if is_calculated_model:
        class_lines.append(f"defining_fields = {defining_fields}\n")
        class_lines.append(f"def get_selected_key_list(key):")
        key_lines = []
        key_lines.append(f"{indent()}")
        for key in defining_fields:
            key_lines.append(f"if key == '{key}':")
            key_lines.append(f"{indent()}# Define objects that will initialize the field {key} e.g.")
            key_lines.append(f"{indent()}# return Class.objects.all()")
            key_lines.append(f"{indent()}pass\n")
        class_lines.append(f"\n{indent()}{indent()}".join(key_lines))
        class_lines.append(f"def calculate(self):")
        class_lines.append(f"{indent()}]# TODO specify what you want to do once the model has been saved")
        class_lines.append(f"{indent()}pass\n")

    lines.append(f"\n{indent()}".join(class_lines))

    return "\n".join(lines)

# the git function enables use to run specific git processes in the console.
def git(*args):
    return subprocess.check_call(['git'] + list(args))

# This function clonse a given repository, creates the directories and files, adds and commits the files to git and pushes the repository
def convert_json_to_lex_files(json):
    print("Cloning Git Repository exited with", git('clone', json['settings']['github_repository']))

    project_name = json['settings']['project_name']
    os.chdir(project_name)
    for model in json['models']:
        file_string = class_to_lex_file(json=json, class_name=model['class']['name'], columns=model['class']['columns'], settings=model['class']['settings'], project_settings=json['settings'])
        class_name = model['class']['name']
        print(f"New File String for {class_name}")
        file_path = model['class']['settings']['file_path'].replace('.', '/')

        os.makedirs(f"{file_path}",exist_ok=True)

        with open(f"{file_path}/{class_name}.py", "w") as model_file:
            model_file.write(file_string)
        print(f"Adding {file_path}/{class_name}.py to Git exited with", git('add', f'{file_path}/{class_name}.py'))

    print('Commiting to Git exited with', git('commit', '-m', 'Initial Commit'))
    print('Pushing to git exited with', git('push'))

if __name__ == '__main__':

    convert_json_to_lex_files(input_json_1)
