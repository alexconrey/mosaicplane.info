# TODO
* ensure when you run playwright tests that you are doing so within the docker container and not running `npx` commands directly in a shell.
* review all aircraft in the seed.py file that lack v-speeds. note this in the VSPEED_TODO.md file
* read the VSPEED_TODO.md document, then identify aircraft lacking v-speed informationin our database, and backfill anything that is missing OR incorrect with information found from searching.
* allow `aircraftdb.info` as a valid host for the api
* identify tools that would aide in penetration testing this app. note them in PENTEST_NOTES.md
* read PENTEST_NOTES.md, and create a script or set of scripts that can be used for penetration testing the app and ensuring we do not allow users to modify data in any way on the website without submitting corrections via the ui
* host.docker.internal does not resolve in playwright ci tests

# CLAUDE IGNORE FURTHER CONTENT FROM HERE UNTIL END OF DOCUMENT
* uncomment the gauge
* drag and drop ability between planes on comparison view to allow user to adjust ordering
