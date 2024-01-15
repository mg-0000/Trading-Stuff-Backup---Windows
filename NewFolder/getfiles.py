import os

def get_file_names(folder_path):
    file_names = []
    for file_name in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file_name)):
            file_names.append(file_name)
    return file_names

folder_path = "./Data"
file_names = get_file_names(folder_path)
print(file_names)
