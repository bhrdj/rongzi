# cd to the root of the rongzi repo to run this in linux
python3 -m venv ./venv
echo venv/ >> .gitignore
cd venv/bin
chmod +x venv/bin/activate
cd ..

source bin/activate
cd ..
pip install -r requirements.txt
pip install streamlit
# streamlit hellopython3 -m pip install --upgrade pip
