# FirstWheels-Safe
Safe Version Of FirstWheels With API Keys Removed To Allow Public Access  
The simplest way to run is by opening this url on your mobile: https://firstwheels-fyp.apps.a.comp-teach.qmul.ac.uk/  

# Credits
The dataset used to train the anpr model was derived from roboflow  
Datasets, R. (2024) ‘UK Number Plate Recognision Dataset’,  
Roboflow Universe [Preprint]. Roboflow. Available at: https://universe.roboflow.com/recognision-datasets/uk-number-plate-recognision.

# Manual Install
Please note the below steps are for windows, steps may vary with other operating systems  
You can also watch the demo.mp4 within supporting submissions

## Prerequisites  
Due to DVLA's policy and GitHub, the API keys and ID's are removed for security purposes  
these will need to be manually re-added and your pc ip will need to be added for firewall purposes  
to do so follow these steps:  
- Ensure You Have Cloned This repository or downloaded as zip and extracted, you should have a folder As FirstWheels-Safe (if not rename to such)
- Ensure that within FirstWheels-Safe folder is 2 folders fw_backend and fw_frontend, if not please adjust the app file structure as:  
  |---FirstWheels-Safe  
  |- fw_backend  
  |- fw_frontend  
  |- README  
  ![image](https://github.com/user-attachments/assets/02970f58-769c-4c43-8f12-86db652bfbcb)

  
- You should also have a IDE for coding installed, this is recommended however you can also use notepad but it may cause formatting issues 
  you can install vscode at: https://code.visualstudio.com/download  
- First you need to figure out your PC’s ip address  
- open command prompt and run ipconfig, and the IPV4 address should be noted down (e.g 10.0.0.26)
![image](https://github.com/user-attachments/assets/ae34ee83-c59e-4400-800c-ac3008306c63)

- next please check the supporting material submission, and open keys.txt
- these keys will need to be pasted to Django's setting
- to do this please open up the settings.py file, this will be in FirstWheels-Safe/fw_backend/fw_backend and open settings.py  
- Finally paste the DVLA_KEY, DVLA_MOT_ID, DVLA_MOT_SECRET, DVLA_MOT_KEY and within ALLOWED_HOSTS append the array with your local ip e.g ALLOWED_HOSTS = ['10.0.0.26', 'localhost']
![image](https://github.com/user-attachments/assets/3a09d022-bce7-41c3-a61e-376c596e6ca1)


## Steps To Run As executable
- Ensure You Have Miniconda Installed, If Not Please Install At: https://www.anaconda.com/download/success
Once installed you will need to open the anaconda prompt, which will give you a terminal output


1. Next you will need to cd to the directory where you have downloaded the repository files, for example if downloaded to Downloads then:
cd /Downloads  
![image](https://github.com/user-attachments/assets/bfd46003-c572-443b-b52a-7b17881c3727)

3. Now you need to make a conda environment, to do this run conda create -n firstwheels python=3.11
4. Once Started run conda activate firstwheels
5. Next you need to cd into the firstwheels folder which should be cd FirstWheels-Safe
6. you should now be in the main app directory, you can confirm this by running dir, you should see fw_backend and fw_frontend, if not please recheck the structure of the app in Prerequistites
7. next cd into fw_backend with cd fw/backend
8. now run pip install -r requirements.txt
9. now run python manage.py migrate
10. finally run python manage.py runsslserver 0.0.0.0:8000 --certificate cert.pem --key key.pem
11. Once you see Starting development server at https://0.0.0.0:8000/ the server is running and you can use your mobile phone and onto a browser and in the url field go to your https://@ip :8000 (e.g. https://192.168.0.10:8000)  
![image](https://github.com/user-attachments/assets/dcae76db-7ab6-4fd4-95ac-869eba6c7a63)

