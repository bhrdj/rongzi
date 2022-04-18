# cd to the root of the rongzi repo to run this in linux


# THIS SECTION IS RUN ONLY ON INSTALLATION
# sudo apt update
# sudo apt install fonts-noto
# # MAYBE NEED TO RESTART
# python3 -m pip install --upgrade pip
# python3 -m venv ./venv
# echo venv/ >> .gitignore
# cd venv/bin
# chmod +x activate
# cd ..
# source bin/activate
# cd ..
# pip install -r requirements.txt
# pip install streamlit

cd ~/git/rongzi/venv
source bin/activate
cd -

streamlit run streamlit_app.py --server.port 8052
