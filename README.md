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

![image](https://github.com/sigmaray/pyqtsnake/assets/1594701/a87373d8-b459-4ec0-a6ca-a9067a08d2dd)

![image](https://github.com/sigmaray/pyqtsnake/assets/1594701/48ff9b3c-2e32-4e4e-ab82-a5e988c6b918)

![image](https://github.com/sigmaray/pyqtsnake/assets/1594701/a0b8a22d-3722-4b5d-aad1-d46dd06d4c2e)


