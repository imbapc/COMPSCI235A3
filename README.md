# COMPSCI235A3
This is the instruction to how to establish visual environment on Windows

STEP 1, open terminal windows in IDE or windows with python installed. Then, type: py -m pip install --upgrade pip If an error raise saying: ERROR: Could not find a version that satisfies the requirement upgrade (from versions: none) Use the command stated in the warning to upgrade.

If you have python 3.3 or newer, jump to STEP 3 Step 2, install the vituralenv by typing: py -m pip install --user virtualenv

Step 3, create virtualenv by typing: py -m venv env

Step 4, activate the virtualenv by typing: .\env\Scripts\activate Then check you are in virtualenv by typing: where python If the result is .../env/bin/python.exe or Then you are in virtual environment

Step 5, install requirements Using command: pip install -r requirements.txt

Step 6, run unit test, integration test Type in terminal windows flask run for running the website in development mode python –m pytest for running tests
