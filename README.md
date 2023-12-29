# PCD
PCD is an application that aims to demonstrate the resolution of problems related to the needs of a non-governmental organization aimed at serving people with disabilities

Objectives:
* Create a previous registration (user).
* Create a second registration related to the necessary data related to the services provided by the Org.
* Insert PDF files related to medical reports and medical prescriptions.
* Link this data to a card with a QR code linking to the PDF (medical report).

![2](https://github.com/gconelhero/brasileiro/assets/26088216/b3fa2bd3-bfa0-435f-a79a-6cde629a3cf1)

Install and config MongoDB:<br>
```python3 -m pip venv pcd```<br>
```cd pcd```<br>
```git clone https://github.com/gconelhero/pcd```<br>
```cd pcd```<br>
```source bin/activate```<br>
```python -m pip install -r requirements```<br>
```source bin/activate```<br>
```python -m pip install -r requirements.txt```<br>
```python manage.py makemigrations cadastro```<br>
```python manage.py migrate```<br>
```python manage.py createsuperuser```<br>
```python manage.py runserver```<br>
