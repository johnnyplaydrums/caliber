# Caliber - Monitor Road Quality

Caliber is a mobile app and web platform to monitor road quality around the world.

### Dev Setup

1. Clone repo 
```
$ git clone https://github.com/johnplaydrums/caliber && cd caliber
```
2. Create virtualenvs for each application (option)
```
$ virtualenv data_ingest/venv && virtualenv data_process/venv
```
3. Install requirements in each
```
$ source data_ingest/venv/bin/activate && pip install -r data_ingest/requirements.txt && deactivate
$ source data_process/venv/bin/activate && pip install -r data_process/requirements.txt
```
4. Enter `venv` and launch app
```
(venv) $ cd data_ingest && AWS_PROFILE=caliber python data_ingest.py
```
