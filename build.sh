#!/bin/bash
apt-get update && apt-get install -y default-libmysqlclient-dev
pip install -r requirements.txt