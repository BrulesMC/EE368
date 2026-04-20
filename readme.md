Made a default user for oauth user (was blank)
Fixed redirect bug where oauth would not sync
Made reset password only show up for standard user
Fixed typo in github ping and reformatted as it would run as a program

Still an issue
only one oauth user is made(visit to 5001/int_data is needed)
the secret is not exposed to shell, so db must be looked at for 5000 to have valid return from 5001 on request
