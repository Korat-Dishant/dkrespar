# steps of development :
1. create a spacy mode (add load en_core_web_sm)
2. using fastAPI create a api for accessing python program
3. use uvicorn to deploy and check api locally
4. deploy api using any web service provider !

## checkout -

(heroku or deta or render)
- right now i am using render because at this time its the only free option !

NOTE : you can also use any cloud based virtual mathine to host your python based app !
for this you would require settingup NGINX

## render 
if you also want to host your api on render, follow the steps below ...
1. create [render account](https://render.com/) for free 
2. click on "new web service"
3. connect your github and select the branch where you have pushed your code
4. fillout detaisl 
  - in start command insert "uvicorn main:app --host 0.0.0.0 --port 10000"
5. create web service
6. once render completes installing dependencies from requirements.txt your api would be live

NOTE : you would requre to mention all of yor projrcts dependencies in "requirements.txt" 
use command ` pip freeze > requirements.txt `

## live api
- you can access my api using :-
https://dkrespar.onrender.com
- use /docs to see swagger documentation
https://dkrespar.onrender.com/docs

## application
here are some screenshot of working application :


<img width="960" alt="Screenshot 2023-04-20 184139" src="https://user-images.githubusercontent.com/86142546/233378156-a12b6fc8-1302-4c62-a85a-3530ba9735eb.png">


postman :


<img width="716" alt="Screenshot 2023-04-20 183916" src="https://user-images.githubusercontent.com/86142546/233378169-aa067f97-685c-4014-8703-0e16fbbbf749.png">
