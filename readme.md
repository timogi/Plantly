# setup

## clone this repository

```bash
git clone
```

## install dependencies

```bash
pip3 install -r requirements.txt
```

### you may use a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

(make sure to adjust the cron job below)

## create the cron job

make code 
```bash
crontab -e
```

add this line


```bash
0 * * * * python3 [path/to/directory]/update.py >> [path/to/directory]/update.log 2>&1
```

cronjob for the virtual environment

```bash
0 * * * * source [path/to/directory]/venv/bin/activate && python3 [path/to/directory]/update.py >> [path/to/directory]/update.log 2>&1
```



