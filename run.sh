#!/bin/bash
python3 -m unittest test_crud.py test_email_analyzer.py test_vocabulary_creator.py
coverage run -m unittest test_crud.py test_email_analyzer.py test_vocabulary_creator.py
coverage report
coverage html
cmd.exe