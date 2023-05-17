# Snake game in Python/QT

## How to install
```
python3 -m venv .venv # optional
source .venv/bin/activate # optional

pip install --upgrade pip
pip install -r requirements.txt 
```

## How to run game rendered with checkboxes
```
python snake.py
```

## How to run game rendered with canvas
```
python snakeg.py
```

## How to launch game using docker compose

```
docker-compose up
```

Open http://localhost:8080/ in browser. Click on `vnc_auto.html`

## How to launch game using docker

```
# It will do this: docker build -t pyqtsnake . && docker run -it -p 8080:8080 pyqtsnake
make docker-build-and-run 
```

## Screenshots

![image](https://github.com/sigmaray/pyqtsnake/assets/1594701/e95b340b-d4ea-4124-9200-0893e0e148e6)

![image](https://github.com/sigmaray/pyqtsnake/assets/1594701/9a0c3649-7e41-47f1-9578-ae8e1960fad5)

![image](https://github.com/sigmaray/pyqtsnake/assets/1594701/4b1cec67-fb40-42d5-b0d9-afec82a4da1a)
