import os
import time

work_dir = os.getenv("BASE_DIR")

# Modify conf.py
conf_path = os.path.join(work_dir, 'docs', 'conf.py')
with open(conf_path, 'r') as original:
    data = original.read()

# Prepend sys.path modification
sys_path_mod = "import os\nimport sys\nsys.path.insert(0, os.path.abspath('..'))\n\n"
if "sys.path.insert(0," not in data:
    data = sys_path_mod + data

# Ensure extensions and exclude_patterns are correctly modified
if "extensions = [" not in data:
    data += "\nextensions = ['sphinx.ext.autodoc', 'sphinx.ext.todo', 'sphinx.ext.viewcode']"
else:
    for ext in ["'sphinx.ext.autodoc'", "'sphinx.ext.todo'", "'sphinx.ext.viewcode'"]:
        if ext not in data:
            data = data.replace("extensions = [", f"extensions = [{ext}, ")

if "exclude_patterns = [" not in data:
    data += "\nexclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']"
else:
    for pattern in ["'_build'", "'Thumbs.db'", "'.DS_Store'"]:
        if pattern not in data:
            data = data.replace("exclude_patterns = [", f"exclude_patterns = [{pattern}, ")

# Update the HTML theme
data = data.replace("html_theme = 'alabaster'", "html_theme = 'sphinx_rtd_theme'")
# Remove 'todo_include_todos = True' if present
data = data.replace("todo_include_todos = True\n", "")
with open(conf_path, 'w') as modified:
    modified.write(data)

# Modify index.rst
index_path = os.path.join(work_dir, 'docs', 'index.rst')
with open(index_path, 'r') as original:
    lines = original.readlines()

insert_line = ':caption: Contents:'
insert_index = None

# Search for the caption line to insert after
for i, line in enumerate(lines):
    if insert_line in line:
        insert_index = i + 1
        break

if insert_index is not None and '   modules\n' not in lines:
    lines.insert(insert_index, '\n   modules\n')
    with open(index_path, 'w') as modified:
        modified.writelines(lines)
else:
    print(f"Warning: Did not find the line '{insert_line}' to insert 'modules' or 'modules' already present.")


time.sleep(2)