#!/bin/bash

# Deploy apis(backend) to gunicorn wsgi server
gunicorn -b 127.0.0.1:5000 app:create_app --log-level debug --timeout 90 -w 4
