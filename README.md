telehealth_project/
│
├── telehealth_project/
│ ├── **init**.py
│ ├── settings.py
│ ├── urls.py
│ ├── asgi.py
│ └── wsgi.py
│
├── accounts/ # Handles user authentication, profile, and roles (patients, doctors)
│ ├── migrations/
│ ├── **init**.py
│ ├── admin.py
│ ├── apps.py
│ ├── forms.py
│ ├── models.py
│ ├── urls.py
│ ├── views.py
│ └── templates/
│ └── accounts/
│ ├── login.html
│ ├── signup.html
│ └── profile.html
│
├── appointments/ # Manages booking, scheduling, and appointments
│ ├── migrations/
│ ├── **init**.py
│ ├── admin.py
│ ├── apps.py
│ ├── forms.py
│ ├── models.py
│ ├── urls.py
│ ├── views.py
│ └── templates/
│ └── appointments/
│ ├── book_appointment.html
│ ├── appointment_list.html
│ └── appointment_detail.html
│
├── consultations/ # Manages video consultations, chat, and related functionalities
│ ├── migrations/
│ ├── **init**.py
│ ├── admin.py
│ ├── apps.py
│ ├── forms.py
│ ├── models.py
│ ├── urls.py
│ ├── views.py
│ └── templates/
│ └── consultations/
│ ├── video_call.html
│ ├── chat.html
│ └── consultation_history.html
│
├── medical_records/ # Manages patient medical records and history
│ ├── migrations/
│ ├── **init**.py
│ ├── admin.py
│ ├── apps.py
│ ├── forms.py
│ ├── models.py
│ ├── urls.py
│ ├── views.py
│ └── templates/
│ └── medical_records/
│ ├── record_list.html
│ ├── record_detail.html
│ └── upload_record.html
│
├── payments/ # Handles billing and payment processing
│ ├── migrations/
│ ├── **init**.py
│ ├── admin.py
│ ├── apps.py
│ ├── forms.py
│ ├── models.py
│ ├── urls.py
│ ├── views.py
│ └── templates/
│ └── payments/
│ ├── payment.html
│ └── invoice.html
│
├── static/ # CSS, JS, and other static files
│ ├── css/
│ ├── js/
│ └── images/
│
├── templates/ # Base templates
│ └── base.html
│
├── manage.py
└── requirements.txt
