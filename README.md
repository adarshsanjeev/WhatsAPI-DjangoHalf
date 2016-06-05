## Installation
Clone the repo 

    git clone --recursive git@github.com:adarshsanjeev/WhatsAPI-DjangoHalf.git

Cd into it
	
Run the django production server

    python manage.py runserver

## Usage

Open 127.0.0.1:8000/

You need to register the first time you access the page. After that, when accessing it for the first time, it creates a new driver and returns the QR code. On scanning, simply refresh the page, and you will be directed to a form. Using the form, one can send and receive messages.

To get unread messages, go to 127.0.0.1:8000/unread/ to see all unread messages.
