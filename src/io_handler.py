import os
from pathlib import Path
import shutil
from file_object import FileObject

__public_path = Path().cwd() / "public/"
def get_public_path():
    return __public_path
__static_path = Path().cwd() / "static/"
def get_static_path():
    return __static_path
__content_path = Path().cwd() / "content/"
def get_content_path():
    return __content_path
__template_path = Path().cwd() / "template.html"
def get_template_path():
    return __template_path

def check_read_directories() -> bool:
    """Checks the static directory to ensure it is present.

    Returns
    -------
    bool
        Returns true if both directories are present, and false if not.
    """

    content_dir_exists = os.path.exists(__content_path)
    stat_dir_exists = os.path.exists(__static_path)

    if not content_dir_exists:
        return False
    if not stat_dir_exists:
        return False
    
    return True

def read_all_content_files(files=None, path=None, retval=None) -> list[FileObject]:
    if not files:
        files = __get_all_content_files()

    if not path:
        path = __content_path

    # files = __get_all_content_files()
    if not retval:
        retval = []

    print("\nReading all content files\n")
    
    for file_path in files:
        if os.path.isfile(file_path):
            print(f"FILE: {file_path}")
            file_content = get_file_contents(file_path)
            retval.append(FileObject(file_content, file_path))
            # print(retval)
        else:
            new_path = Path(file_path)
            new_folder = path / file_path.stem

            dest_folder_string = f"{new_folder}"
            dest_folder_string = dest_folder_string.replace("/content", "/static")
            print(f"DEST FOLDER: {dest_folder_string}")
            new_folder = Path(dest_folder_string)

            if not os.path.exists(new_folder):
                print(f"Creating dir: {new_folder}")
                os.mkdir(new_folder)
            else:
                print(f"Folder already exists ({new_folder}).")
            read_all_content_files(files=get_all_files_for_given_path(new_path), path=new_folder, retval=retval)
            # push_public(get_all_files_for_given_path(new_path), new_folder)
    
    return retval

def __get_all_content_files() -> list:
    return list(__content_path.iterdir())

def __get_all_static_files() -> list:
    return list(__static_path.iterdir())

def clean_public_directory():
    if not os.path.exists(__public_path):
        return
    shutil.rmtree(__public_path)
    

def get_all_files_for_given_path(path):
    return list(path.iterdir())

def push_public(files=None, path=None):
    if not files:
        files = __get_all_static_files()

    if not os.path.exists(__public_path):
        os.mkdir(__public_path)

    if not path:
        path = __public_path
    
    for file in files:
        if os.path.isfile(file):
            if file.suffix == ".md":
                continue
            
            dest = path / file.name
            try:
                shutil.copy(file, dest)
                print("File copied successfully.")
            
            # If source and destination are same
            except shutil.SameFileError:
                print("Source and destination represents the same file.")
            
            # If there is any permission issue
            except PermissionError:
                print("Permission denied.")
            
            # For other errors
            except:
                print("Error occurred while copying file.")
        else:
            new_path = Path(file)
            new_folder = __public_path / file.stem
            if not os.path.exists(new_folder):
                print(f"Creating dir: {new_folder}")
                os.mkdir(new_folder)
            else:
                print("Folder already exists.")
            push_public(get_all_files_for_given_path(new_path), new_folder)

def get_file_contents(path: Path) -> str:
    # file_path = __content_path / file_name
    contents = ""

    try:
        contents = path.read_text()
    except FileNotFoundError:
        print("No such thing.")

    return contents