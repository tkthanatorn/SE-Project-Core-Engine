# Centiment Engine
Console application for scrapping cryptocurrency news from other sites with xpath and predict sentimental of those article by tokenize article into sentences and predicted sentimental by Machine Learning then use majority scoring to score and find the result of those article. all of scrapping data those process in this application will save into SQL database for let's others application to take them to show.

## Setup
1. Install specific dependencies of this project.
```
pip install -r requirements.txt
```
2. Install compatible [***ChromeDriver***](https://chromedriver.chromium.org/downloads) version with Google Chrome Browser version.
3. Comment this code section in [luancher.py](https://github.com/aisudev/SE-Project-Core-Engine/blob/main/src/luancher.py) for your first execution.
```
self.db.execute_commit(f"""
            DROP TABLE Source_Configs;
        """)
```
4. Edit database config in [***config.yaml***](https://github.com/aisudev/SE-Project-Core-Engine/blob/main/src/config/config.yaml) ( your database shoud be Postgresql. If it's not, you should to [install](https://dev.to/shree_j/how-to-install-and-run-psql-using-docker-41j2) it first. )
```
database:
  # database dev config
  dev:
    host: # host IP
    port: # host Port
    username: # database username
    password: # database password
    dbname: # database name
# end database config
```
5. Start Engine
```
python main.py
```
