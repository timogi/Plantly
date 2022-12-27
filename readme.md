# setup

## clone this repository

```bash
git clone
```

## install dependencies

```bash
pip3 install -r requirements.txt
```

hint: if you are using a virtual environment, you can create one with

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## add the .env file containing the following variables

```bash
BEE_HOME_TOKEN = [your token]
BEE_HOME_ENDPOINT = [your endpoint]
```

## create the cron job

make code 
```bash
crontab -e
```

add this line if you are using a global python environment


```bash
0 * * * * python3 [path/to/directory]/update.py >> [path/to/directory]/update.log 2>&1
```

add this line if you are using a virtual environment

```bash
0 * * * * source [path/to/directory]/venv/bin/activate && python3 [path/to/directory]/update.py >> [path/to/directory]/update.log 2>&1
```



