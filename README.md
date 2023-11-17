# AI-Messenger

QT GUI for large language models

Uses LLaMA.cpp and ExLLaMA V2 as backends.

**Installation:**

First make sure Python (3.10+ recommended) and GIT are installed. Then:
```
git clone https://github.com/shinomakoi/AI-Messenger
cd AI-Messenger
```
Optionally create a virtual environment (recommended)

```
python -m venv .venv
source ./.venv/bin/activate ### For Linux
.\.venv\Scripts\activate ## For Windows
```
```
pip install -r requirements.txt
```
**llama.cpp**

To use the LLaMA.cpp backend run the server in the LLaMA.cpp directory, e.g.:
```
.\server -m "models/model.gguf" -t 6 -ngl 18 -c 4096
```
**ExLLaMA V2**

To use the ExLLaMa backend run ```ws-server.py``` in the ExLLaMA directory

**Usage:**

To launch the app, use: 
```
python main.py
```

Uses https://github.com/UN-GCPDS/qt-material for themes
