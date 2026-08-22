# SmartPark

SmartPark is a professional smart parking management system built for an MCA minor project. It provides a database-backed workflow for discovering parking spaces, reserving a slot, issuing a secure QR parking pass, checking vehicles in and out, recording payments, and generating receipts.

The project is intentionally built with understandable Flask and SQLite components, while presenting a polished SaaS-style experience for a project demonstration or viva.

## Highlights

- Responsive SmartPark interface for desktop, tablet, and mobile screens
- Branded landing page with animated marquee, live lot preview, CTA sections, and responsive footer
- Light and dark themes with a persisted browser preference
- Installable Progressive Web App with manifest, service worker, and install prompt
- SEO metadata, canonical URLs, Open Graph metadata, structured data, robots file, and sitemap
- User registration, secure password hashing, login, remember-me sessions, and logout
- Role-based authorization for regular users and administrators
- Vehicle registration and default vehicle selection
- Parking area and slot discovery with search and slot-type filters
- Server-side slot validation and reservation locking
- Booking reference generation and secure, non-sensitive QR tokens
- Automatic reservation expiry and slot release
- Admin check-in and check-out workflow
- Configurable hourly and additional-hour fee calculation
- Payment records with transaction IDs
- In-app notifications and unread notification counts
- Downloadable QR images and PDF parking receipts
- Configurable SMTP email service with graceful local fallback
- Friendly error pages and flash notifications
- Automated regression test for authentication and booking persistence

## Technology Stack

### Backend

- Python 3.13+
- Flask application factory
- Flask-SQLAlchemy and SQLite
- Flask-Login
- Flask-WTF CSRF protection
- Flask-Mail
- Werkzeug password hashing
- Jinja2 templates

### Frontend

- HTML5 and semantic templates
- CSS3 custom design system
- Bootstrap 5.3
- Bootstrap Icons
- Vanilla JavaScript
- CSS animations, transitions, responsive breakpoints, and reduced-motion support

### Supporting Libraries

- `qrcode` and Pillow for QR image generation
- ReportLab for PDF receipt generation
- `python-dotenv` for environment configuration
- `email-validator` for email validation support
- Pytest for automated tests

## System Requirements

- Python 3.10 or newer
- A modern browser such as Chrome, Edge, Firefox, or Safari
- PowerShell, Command Prompt, or a Unix-compatible shell
- Internet access during first install if dependencies are not cached

## Installation

Clone or open the project folder, then create a virtual environment:

```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create local environment settings by copying `.env.example` to `.env`. The application works without SMTP credentials; email delivery is skipped safely when mail settings are empty.

## Database Setup and Demo Data

Create the SQLite tables and demo records:

```powershell
python seed.py
```

The database is stored at `instance/smartpark.db`. The seed script is idempotent for the demo accounts and initial parking data.

## Run the Application

```powershell
python run.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in a browser.

For a fresh database, run `python seed.py` before starting the server. During development, Flask debug reload is enabled by `run.py`.

## Demo Credentials

| Role          | Email                 | Password    |
| ------------- | --------------------- | ----------- |
| Administrator | `admin@smartpark.com` | `Admin@123` |
| User          | `user@smartpark.com`  | `User@123`  |

Change demo passwords before using the project outside a classroom or local demonstration.

## Main User Flow

1. Register or sign in.
2. Add a vehicle from **Vehicles**.
3. Open **Find parking** and filter available spaces.
4. Select **Reserve this slot**.
5. Choose the vehicle and expected entry and exit times.
6. Confirm the reservation.
7. Open the booking from the dashboard to view the QR pass.
8. An administrator verifies the QR token or booking ID.
9. The administrator checks the vehicle in and later checks it out.
10. Checkout releases the slot, records payment, creates a PDF receipt, and adds a notification.

## Administrator Flow

Administrators can access the protected operations area to:

- View users and activate or deactivate accounts
- Create and review parking areas
- Monitor slot availability
- Verify QR references
- Check vehicles in and out
- Record completed payment transactions
- Review recent booking activity and operational metrics

## Project Structure

```text
SmartPark/
├── app/
│   ├── __init__.py             # Flask factory and extensions
│   ├── models.py               # SQLAlchemy entities and relationships
│   ├── routes/                 # Public, auth, user, parking, booking, admin routes
│   ├── services/               # Fees, notifications, QR, PDF, and email services
│   ├── templates/              # Shared, user, booking, parking, and admin views
│   ├── static/
│   │   ├── css/                # Base, brand, responsive, and experience styles
│   │   ├── js/                 # Theme, install, form, and reveal interactions
│   │   ├── images/             # SmartPark logo assets
│   │   └── generated/          # Runtime-generated files
│   └── utils/                  # Authorization helpers
├── instance/                   # Local SQLite database
├── tests/                      # Automated regression tests
├── config.py                  # Environment-based configuration
├── seed.py                    # Demo data initialization
├── run.py                     # Development entry point
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variable template
└── README.md
```

## Important Routes and APIs

| Route                    | Purpose                                  |
| ------------------------ | ---------------------------------------- |
| `/`                      | SmartPark landing page                   |
| `/auth/register`         | User registration                        |
| `/auth/login`            | User login                               |
| `/user/dashboard`        | User booking dashboard                   |
| `/user/vehicles`         | Vehicle management                       |
| `/user/notifications`    | Notification center                      |
| `/parking`               | Live parking search                      |
| `/parking/api/slots`     | Slot availability JSON endpoint          |
| `/bookings/new`          | Create a reservation                     |
| `/bookings/<id>`         | View a booking pass                      |
| `/bookings/<id>/qr`      | Download a booking QR image              |
| `/bookings/<id>/receipt` | Download a PDF receipt                   |
| `/admin/dashboard`       | Protected admin dashboard                |
| `/admin/users`           | Protected user management                |
| `/admin/areas`           | Protected area management                |
| `/admin/verify`          | Protected QR/manual booking verification |
| `/health`                | Application health response              |
| `/sw.js`                 | Root-scoped PWA service worker           |

## Environment Variables

Supported settings are documented in `.env.example`:

```env
SECRET_KEY=replace-with-a-long-random-value
DATABASE_URL=sqlite:///instance/smartpark.db
MAIL_SERVER=
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_DEFAULT_SENDER=noreply@smartpark.local
```

Never commit real secret keys, SMTP passwords, or production credentials.

## Testing

Run the automated tests from the project root:

```powershell
python -m pytest -q
```

The current regression test verifies login, authenticated booking creation, database persistence, and slot reservation state. Additional test cases can be added in `tests/` as new modules are introduced.

## Security Notes

- Passwords are stored using Werkzeug password hashes.
- Mutating forms are protected with Flask-WTF CSRF tokens.
- SQLAlchemy ORM is used instead of interpolated SQL.
- Admin operations require authentication and the `ADMIN` role.
- Booking detail, QR, and receipt access is owner- or admin-authorized.
- SMTP credentials are read from environment variables only.
- Invalid or unavailable booking inputs are rejected server-side.
- User-facing 403, 404, and 500 responses use friendly templates.

## Screenshots

Add project screenshots here for the final academic report or viva presentation:

1. Landing page and live lot preview
2. User dashboard
3. Parking search and filter view
4. Digital QR parking pass
5. Admin operations dashboard
6. Mobile responsive view

## Current Scope and Future Enhancements

The current build focuses on the complete local demonstration path: authentication, vehicles, parking search, reservation, QR pass, admin verification, check-in/out, payment record, notification, and PDF receipt.

Future extensions can add password-reset email flows, full slot and pricing CRUD screens, richer reporting and analytics charts, profile photo uploads, production payment gateway integration, background expiry jobs, and database migrations. These should be added without exposing credentials or weakening the existing authorization rules.

## Academic Project Note

SmartPark is suitable for an MCA first-semester minor project demonstration. It demonstrates MVC-style Flask organization, ORM relationships, authentication, authorization, validation, database integrity, service separation, responsive frontend design, QR generation, PDF generation, and test-driven verification of a core business flow.

## IN Future Add this things

Isme abhi ye add karna hai ki Admin kya contol karega aur user kya kya karega.
