## Running without Docker
### Setup
```
git clone https://github.com/GoncaloBFM/mma2024
cd mma2024
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run
On the root directory of the project run:
```
export PYTHONPATH="$PYTHONPATH:$PWD"
python src/main.py
```

After the Dash server is running open http://127.0.0.1:8050/ on your browser.

## (Alternative) Running with Docker
### Setup
1) Install Docker
2) Run:
```
git clone https://github.com/GoncaloBFM/mma2024
cd mma2024
docker buildx build . -t mma2024
```

### Run
On the root directory of the project run:
```
docker run --net=host -v ./dataset:/usr/src/app/dataset/  mma2024
```

After the Dash server is running open http://127.0.0.1:8050/ on your browser.

## Plotly and Dash tutorials
- Dash in 20 minutes: https://dash.plotly.com/tutorial
- Plotly plots gallery: https://plotly.com/python/
