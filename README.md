This assingment solution provides a Flask-based web service for processing receipts and calculating points based on the projects decription

1. clone my forked repo

2. install flask:
    Bash:pip install Flask


2. create the virtual environment:
    Bash: python3 -m venv venv

3. install testing dependencies
    Bash: pip install -r requirements-test.txt

4. run the application:
    python app.py

5. Run the testsm and checks for coverage:
    pytest tests/ -v --cov=app