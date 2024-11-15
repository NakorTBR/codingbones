from io_handler import check_read_directories, clean_public_directory, push_public
from io_handler import get_content_path, get_static_path, get_public_path, get_template_path
from generator import generate_page, generate_pages_recursive

def main():
    if not check_read_directories():
        raise Exception("Read (content and static) directories not found!")
    clean_public_directory()

    content = get_content_path() / "index.md"
    dest = get_static_path() / "index.html"
    # generate_page(from_path=content, dest_path=dest, template_path=get_template_path())
    generate_pages_recursive()

    push_public()


main()