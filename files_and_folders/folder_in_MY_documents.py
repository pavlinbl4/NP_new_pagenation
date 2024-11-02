from pathlib import Path


def make_documents_folder(name):
    # (Path.home() / "Documents" / f"{name}").mkdir(parents=True, exist_ok=True)
    x = (Path.home() / f"{name}/{name}").mkdir(parents=True, exist_ok=True)

    # return Path.home() / "Documents" / f"{name}"
    return Path.home() / f"{name}*2/{name}"

if __name__ == '__main__':
    print(make_documents_folder(input("Enter the folder name\n\n")))
