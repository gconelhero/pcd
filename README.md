
# PCD Demo preview
PCD is an application that aims to demonstrate the resolution of problems related to the needs of a non-governmental organization aimed at serving people with disabilities

Objectives:
* Create a previous registration (user).
* Create a second registration related to the necessary data related to the services provided by the Org.
* Insert PDF files related to medical reports and medical prescriptions.
* Link this data to a card with a QR code linking to the PDF (medical report).

![2](https://github.com/gconelhero/pcd/assets/26088216/75354bdc-6c1a-464d-8771-5dd8475f0956)

Install and config MongoDB:<br>
```python3 -m pip venv pcd```<br>
```cd pcd```<br>
```source bin/activate```<br>
```git clone https://github.com/gconelhero/pcd```<br>
```cd pcd```<br>
```python -m pip install -r requirements```<br>
```python -m pip install -r requirements.txt```<br>
```python manage.py makemigrations cadastro```<br>
```python manage.py migrate```<br>
```python manage.py createsuperuser```<br>
```python manage.py runserver```<br>
