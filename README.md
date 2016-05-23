## Installation
First create a django project

    django-admin startproject <project name>

Clone the repo inside the folder created.

    git clone git@github.com:adarshsanjeev/WhatsAPI-DjangoHalf.git

Inside the same directory, open the main app directory, and add it to the INSTALLED_APPS in the settings file. Also set the MEDIA_ROOT and MEDIA_URL variables.

    INSTALLED_APPS = [
    ...,
    'WhatsAPI', ]
    MEDIA_ROOT = os.path.join(BASE_DIR,'media/')
    MEDIA_URL = '/media/'

Set up the urls.py inside the main app directory to redirect requests to WhatsAPI.  Also set it up to serve media files. 

    from django.conf import settings
    from django.conf.urls.static import static  `
    urlpatterns = [
    ..., 
    url(r'', include('WhatsAPI.urls', namespace = "API")), ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

Inside the WhatsAPI repo, clone the actual WhatsAPI

    cd <WhatsAPI app>
    git clone git@github.com:mukulhase/WhatsAPI.git
    
Fianlly, run the django production server

    python manage.py runserver

## Usage

Open 127.0.0.1:8000/

You need to register the first time you access the page. After that, when accessing it for the first time, it creates a new driver and returns the QR code. On scanning, simply refresh the page, and you will be directed to a form. Using the form, one can send and receive messages.

To get unread messages, go to 127.0.0.1:8000/unread/ to see all unread messages.
