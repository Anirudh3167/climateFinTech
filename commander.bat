@echo off

Title "COMMANDER"

echo Running the commander.

set /p cmd= ">>>"

if %cmd%==git (CALL :git) 
if %cmd%==django (CALL :django)

pause
exit
:git
	echo commander is set to git
	set /p cmd= "git:-"
	if %cmd%==auto (CALL :autogit)
	goto :eof

:django
	echo commander is set to django
	set /p cmd= "django:-"
	if %cmd%==auto (CALL :autodjango)
	if %cmd%==server (CALL :djangoserver)
	goto :eof

:autogit
	echo taking files from repo to local folder.
	git pull
	echo\
	echo sending files from local folder to repo.
	git add .
	echo\
	set /p msg= "commit messge:"
	git commit -m "%msg%"
	git push
	echo\
	echo sucessfully pushed. :)
	goto :eof

:autodjango
	cd ClimateFintech
	echo checking for migrations.
	python manage.py makemigrations
	echo\ 
	echo migrating the models.
	python manage.py migrate
	echo\
	echo building the server
	start http://127.0.0.1:8000
	python manage.py runserver
	
	goto :eof

:djangoserver
	cd ClimateFintech
	echo\
	echo building the server
	start http://127.0.0.1:8000
	python manage.py runserver
	
	goto :eof
	
