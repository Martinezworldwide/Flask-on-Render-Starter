import os

# Directory containing the project files
project_dir = os.path.dirname(__file__)

def print_dropdown(file_path):
    rel_path = os.path.relpath(file_path, project_dir)
    print(f"<details>")
    print(f"<summary><code>{rel_path}</code></summary>\n")
    print("```")
    with open(file_path, 'r', encoding='utf-8') as f:
        print(f.read())
    print("```")
    print("</details>\n")

if __name__ == "__main__":
    for root, dirs, files in os.walk(project_dir):
        for file in files:
            if file.endswith((".py", ".txt", ".yaml", ".html", ".md")) and file != "code.py":
                print_dropdown(os.path.join(root, file))
