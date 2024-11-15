from io_handler import get_file_contents, read_all_content_files, get_template_path
from pathlib import Path
from nodehandlers import markdown_to_html_node, extract_title, strip_title

def generate_page(from_path:Path, template_path:Path, dest_path:Path):
    print(f"\nGenerating page from \n{from_path} \nto \n{dest_path} \nusing \n{template_path}")

    md_contents = get_file_contents(from_path)
    template = get_file_contents(template_path)
    title = extract_title(md_contents)
    
    contents = markdown_to_html_node(md_contents)

    titled_html = template.replace("{{ Title }}", title)
    full_html = titled_html.replace("{{ Content }}", contents)
    

    
    html_contents = markdown_to_html_node(full_html)
    dest_path.write_text(html_contents)


def generate_pages_recursive():
    all_files = read_all_content_files()

    # print(f"Sending files to {dest_dir_path}")
    

    for obj in all_files:
        path_string = f"{obj.path}"
        # print(path_string)
        path_string = path_string.replace("/content", "/static")
        # print(f"REL: {path_string}")

        write_path = Path(path_string).with_suffix('.html')
        # print(f"OBJ PATH: {obj.path.parent}")
        print(f"File would go at {write_path}")
        # print(f"\n{obj.text}")
        # write_path.write_text(obj.text)

        # md_contents = get_file_contents(from_path) #obj.text
        template = get_file_contents(get_template_path())
        title = extract_title(obj.text)
        
        contents = markdown_to_html_node(obj.text)

        titled_html = template.replace("{{ Title }}", title)
        full_html = titled_html.replace("{{ Content }}", contents)
        

        
        html_contents = markdown_to_html_node(full_html)
        write_path.write_text(html_contents)

