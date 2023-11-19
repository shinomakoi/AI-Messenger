# AI-Messenger

QT GUI for large language models, for Windows, Linux and Mac.

Features:
- LLama.cpp and Exllama V2 as backends
- LLaVA multimodal support
- Chat, completion, notebook modes
- Model paramater presets
- Instruct presets + V2 Tavern character cards
- Save chat sessions

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

To use the ExLLaMa backend run ```python examples/ws-server.py --model "model_path"``` in the ExLLaMA directory

**Usage:**

To launch the app, use: 
```
python main.py
```

**Character cards**

Place V2 character cards (such as from Chub.ai) in the presets/Cards directory

![image](https://github.com/shinomakoi/AI-Messenger/assets/112139428/3cbc7185-80b6-4241-8e3e-6cd3c123a534)

Uses https://github.com/UN-GCPDS/qt-material for themes
