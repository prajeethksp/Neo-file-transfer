---

# NEO: Secure Cloud File Transfer System

A web application built with Django for secure file transfer and management. This project enables users to register, log in, upload, download, and transfer files between accounts, with a user-friendly dashboard and robust authentication.

## Features

- User registration and authentication
- Dashboard for managing files
- Secure file upload and download
- File transfer between users
- Success and error notifications
- Responsive UI with custom templates

## Project Structure

```
matrix/
├── manage.py
├── matrix/                # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── neo/                   # Main app: models, views, forms, migrations
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── ...
├── static/                # Static files (images, CSS, JS)
│   └── images/
├── templates/             # HTML templates
│   └── neo/
│       ├── base.html
│       ├── dashboard.html
│       ├── login.html
│       ├── registration.html
│       ├── upload.html
│       ├── download_file.html
│       └── ...
└── requirements.txt       # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.8+
- Django (see requirements.txt)
- (Optional) Virtual environment

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/prajeethksp/Neo-file-transfer.git
   cd Neo-file-transfer/matrix
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Apply migrations:
   ```sh
   python manage.py migrate
   ```

4. Run the development server:
   ```sh
   python manage.py runserver
   ```

5. Access the app at [http://localhost:8000/](http://localhost:8000/)

### Usage

- Register a new account or log in.
- Upload files from the dashboard.
- Download or transfer files to other users.
- View transfer status and notifications.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.

---
