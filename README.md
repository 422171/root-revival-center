# Root Revival Center

A Flask-powered web application for plant enthusiasts to list, edit, and adopt plants.

## Features

- User authentication (sign up, login, logout)
- Create, view, edit, and delete plant listings
- Image upload and storage for each plant
- Responsive, modern UI with Flexbox and inline forms
- Client and server validation with flash messaging
- Dashboard showing your own plant listings

## Installation

1. Clone the repository:
   ```bash
   git clone <repo-url> root-revival-center
   cd root-revival-center
   ```
2. Create and activate a virtual environment (Windows PowerShell):
   ```powershell
   python -m venv flaskenv
   .\flaskenv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Initialize the database:
   ```bash
   flask shell
   >>> from app import db
   >>> db.create_all()
   >>> exit()
   ```
5. Run the app:
   ```bash
   flask run
   ```

## Usage

- Browse home page to see all plants.
- Sign up or log in to create your own listings.
- View details, edit, or delete plants you posted.
- Request adoption of available plants.

## Future Improvements

- **Notification System**: Send email or in-app notifications to plant owners when someone requests adoption.
- **Adoption Tracking**: Allow users to view and manage the plants they requested in their dashboard.
- **User Profiles**: Let users customize profiles with bio, avatar, and adoption history.
- **Search & Filters**: Add search, categories, and filtering by plant type or availability.
- **Pagination**: Implement pagination on home and dashboard for large datasets.
- **Access Control**: Admin panel for site moderators to approve or reject plant listings.
- **REST API**: Expose API endpoints for integrating with mobile or third-party apps.
- **Image Optimization**: Resize and compress uploads for faster load times.
- **Testing**: Add unit and integration tests with coverage reporting.

---

*Created June 2025*
