# show scopes
00:
	python -m cliauth.google scopes

# auth
01:
	python -m cliauth.google auth --skip-verify -s https://www.googleapis.com/auth/spreadsheets.readonly -s https://www.googleapis.com/auth/drive.readonly --force

# token-info
02:
	python -m cliauth.google token_info

# get access token from refresh_token
03:
	python -m cliauth.google access_token

# revoke token
04:
	python -m cliauth.google revoke_token

# listing spreadsheet ( use python-google-api-client )
10:
	python $@*.py
11:
	python $@*.py
12	:
	python $@*.py

