import os
import re
from shutil import rmtree, copy
from markdown_handler import markdown_to_html_node


def copy_static(path: str = "static", dest: str = "public") -> None:
    """
    A recursive function that copies the contents of the given folder to a public folder.
    By default the static folder at root is used.

    Args:
        path: path of the folder to copy
    """

    if os.path.exists(dest):
        rmtree(dest)

    os.mkdir(dest)

    if os.path.exists(path):
        items = os.listdir(path)
        for item in items:
            item_path = os.path.join(path, item)
            dest_path = os.path.join(dest, item)

            if os.path.isdir(item_path):
                copy_static(item_path, dest_path)
            else:
                copy(item_path, dest_path)


def extract_title(markdown: str) -> str:
    """
    Extracts the title from the given markdown string.
    Raises an exception if the title is not found.

    Args:
        markdown: markdown string to extract title from

    Raises:
        Exception: when no h1 title is found

    Returns: title as string

    """
    title = re.search(r"^# (.+)", markdown, re.MULTILINE)
    if title:
        return title.group(1)

    raise Exception("Title not found")


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:

    if not os.path.exists(dir_path_content):
        raise Exception("source file does not exist")

    if not os.path.exists(template_path):
        raise Exception("template file does not exist")

    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)

        if os.path.isdir(item_path):
            dest_folder_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(item_path, template_path, dest_folder_path)
        elif item.endswith(".md"):
            item_name = os.path.splitext(item)[0]
            dest_path = os.path.join(dest_dir_path, item_name + ".html")

            with open(item_path, "r", encoding="utf-8") as file:
                content = file.read()
                title = extract_title(content)
                html = markdown_to_html_node(content)

                with open(template_path, "r", encoding="utf-8") as template_file:
                    template = template_file.read()
                    template = template.replace("{{ Title }}", title)
                    template = template.replace("{{ Content }}", html.to_html())

                    with open(dest_path, "w", encoding="utf-8") as output_file:
                        output_file.write(template)




def main():
    """Main function for the program"""
    copy_static()
    generate_pages_recursive("content", "template.html", "public")


main()
