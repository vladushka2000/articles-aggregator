#!/bin/bash
alembic upgrade head
python3 -u main.py
