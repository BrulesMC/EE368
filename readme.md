Work needed
Entries should store type, so api/me can expose it
needed to fix the reset password button if using github to not show up

Use endpoint /api/login_standard as request for normal

Use endpoint /api/login_github for github
The github will always give the full auth back so the endpoint needs to see if the user exists, and if not, make them as we will not ahve a register with github

Register needs no changes



Use python 3.12.3 for stablity
Use a venv
pip install -r requirments.txt should setup the needed packages
