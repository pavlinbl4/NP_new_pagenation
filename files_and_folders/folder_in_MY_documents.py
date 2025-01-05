from pathlib import Path

icloud_folder = Path().home() / 'Library/Mobile Documents/com~apple~CloudDocs/'

def make_documents_folder(name):

    # (Path.home() / f"{name}/{name}").mkdir(parents=True, exist_ok=True)
    # (icloud_folder / f"{name}/{name}").mkdir(parents=True, exist_ok=True)
    (icloud_folder / name).mkdir(parents=True, exist_ok=True)
    return icloud_folder  / name


if __name__ == '__main__':
    print(make_documents_folder(input("Enter the folder name\n\n")))
