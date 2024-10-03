echo "Exporting BASE_DIR..."
BASE_DIR=$(dirname  "$(pwd)")
echo "BASE_DIR: $BASE_DIR"
export BASE_DIR

echo "Installing Sphinx and sphinx-rtd-theme..."

sudo apt-get install -y python3-sphinx
sudo apt-get install -y python3-sphinx-rtd-theme 

echo "Installing LaTeX for PDF documentation generation..."
sudo apt-get install -y texlive-full
sudo apt-get install -y texlive latexmk

echo "Buildiing the python library..."
echo "Going to the root directory of the project..."
cd ../..
echo $(pwd)
echo "Installing the python library..."
pip install -e .
cd ${BASE_DIR}

echo "Creating the docs directory..."

sudo rm -r docs

mkdir docs
cd docs
sphinx-quickstart -q \
  -p "NextCloud Functionl Tests" \
  -a "Skander Lahbaiel" \
  -v 1.0 \
  --dot=_ \
  --extensions=sphinx.ext.autodoc,sphinx.ext.todo,sphinx.ext.viewcode \
  --makefile \
  --no-use-make-mode \
  


cd ${BASE_DIR}
echo "Executing sphinx-apidoc and make html in the directory: ${BASE_DIR}..."
sphinx-apidoc -o docs .
cd ${BASE_DIR}

echo "Modifying the conf.py file..."  
cd generate_documentation
sudo -E python3 modify_conf.py

cd ${BASE_DIR}/docs
make html

make latexpdf
echo "PDF documentation is ready at ${BASE_DIR}/docs/_build/latex/NextCloudFunctionlTests.pdf"

echo "Documentation is ready at ${BASE_DIR}/docs/_build/html/index.html"