# Webserver

## SETUP

1. Install nginx and python3-venv:  
    ```sudo apt install nginx python3-venv```  
 
2. Extract the contents of Webserver folder into your project folder  

3. Grant execute permission to start.sh:  
    ```sudo chmod +x start.sh```

4. In **nginx/Grundlagenpraktikum**  
    ```[Line 18] Change path of static folder```  
    ```[Line 22] Change path of media folder```  

5. In **Grundlagenpraktikum/Grundlagenpraktikum/settings.py**  
    ``` [Line 16] Set ip and hostname ```

6. Create python virtual environment inside your project folder:  
    ```python3 -m venv venv```  
    
7. Activate virtual environment:  
    ```source venv/bin/activate```  
    
8. Install requierements:  
    ```pip install -r requirements.txt```  
    
9. Create 'secret_key' file and set file permissions:  
    ``` cd Grundlagenpraktikum && python3 -c 'import secrets; print(secrets.token_hex(100))' > secret_key.txt ```  
    ``` chmod 600 secret_key.txt ```  

10. Collect static files:  
    ```python3 manage.py collectstatic```  

11. Move .key and .crt file from **my_project/nginx/** to **/etc/nginx/**  

12. Move **my_project/nginx/Grundlagenpraktikum** to **/etc/nginx/sites-available/**

13. Create symlink of previous file in **/etc/nginx/sites-enabled/**:  
    ```sudo ln -s /etc/nginx/sites-available/Grundlagenpraktikum```

14. Delete the 'default' file in **/etc/nginx/sites-enabled/**:  
    ```rm -rf default```

## Filesystem

<img src="https://user-images.githubusercontent.com/85405690/159138442-67dcfa67-40c7-43a1-9b75-5a7ee76d48e2.png" height="400">  
  
## USAGE

### Start Nginx:  

    systemctl start nginx  
  
### Start gunicorn:  

    ./start.sh  
  
## COMMANDS

### Change password of all Praktikanten:  

    python3 manage.py praktikanten_pwd

## NOTES

Admin Credentials: admin:Betreuer
