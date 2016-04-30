#! /usr/bin/env python

from app.main import app as prog

prog.run(debug=True,host='0.0.0.0',port=8080)
