# SmartPark – Complete Project Brain Document

This document serves as the absolute and exhaustive "Brain" for **SmartPark - Smart Parking Management System**, developed as an MCA 1st Semester Minor Project. It details everything that has been used, planned, and implemented across the entire lifecycle of the project, from the initial frontend design to the final database integration.

---

## 1. Project Overview & Goal
**SmartPark** is a full-stack, production-ready Smart Parking Management System. It handles the complete lifecycle of a parking session:
- **Users** can discover parking areas, reserve slots, generate secure digital QR tickets, manage vehicles, download PDF receipts, and track payment history.
- **Admins** manage the entire platform, including parking infrastructure (areas and slots), user accounts, real-time check-in/out via QR scanning, dynamic fee policies, and financial ledgers.

The platform uses a **parking-session fee only** model (no website subscriptions). All fees are dynamically calculated based on Admin-configured policies (e.g., hourly, daily rates, grace periods) and timestamps.

---

## 2. Comprehensive Technology Stack

### Backend Technologies
- **Python 3.10+**: Core programming language.
- **Flask 3.1**: The main web framework, utilizing the Application Factory Pattern and Blueprints for modularity.
- **Werkzeug**: Used for secure PBKDF2 password hashing.
- **Jinja2**: HTML templating engine.
- **python-dotenv**: For managing environment variables securely.

### Database & ORM
- **SQLite (Local) / PostgreSQL (Neon in Production)**: The relational databases used.
- **SQLAlchemy & Flask-SQLAlchemy**: Object-Relational Mapper (ORM) used to interact with the database without writing raw SQL.
- **psycopg2-binary**: PostgreSQL adapter for production deployment.

### Frontend Technologies
- **HTML5 & CSS3**: Core markup and styling. Uses custom CSS variables for complete theming.
- **Vanilla JavaScript**: Used for all DOM manipulation, fetch/AJAX requests, and interactivity. No heavy JS frameworks (React/Vue) were used to maintain maximum performance.
- **Bootstrap 5.3 & Bootstrap Icons**: Core UI framework for responsiveness and components.
- **Chart.js**: Used to render analytics and statistics on the Admin Dashboard.
- **PWA (Progressive Web App)**: Configured with a web manifest and service workers, making the app installable on mobile devices.

### Specialized Libraries & Utilities
- **Flask-Login**: Manages user sessions, remember-me functionality, and role-based access.
- **Flask-WTF & WTForms**: Secures all forms against CSRF attacks and provides backend validation.
- **Flask-Mail**: Handles SMTP email dispatch (with a graceful fallback if SMTP is unavailable).
- **qrcode & Pillow**: Used dynamically in the backend to generate secure QR pass images.
- **ReportLab**: Used dynamically to generate professional PDF parking receipts.

### Deployment & Infrastructure
- **Vercel**: Serverless platform used for live deployment.
- **Neon**: Serverless Postgres hosting.
- **GitHub**: Version control.

---

## 3. Project Development Phases

The project was meticulously developed in three distinct phases to ensure scalability and clean architecture.

### Phase 1: Frontend & UI/UX Design
**Goal:** Build the complete visual foundation.
- **What was done:** Created a highly professional, SaaS-style interface. Instead of a basic template, a custom design system was built using CSS variables to support dynamic **Light and Dark modes**.
- **Key Deliverables:** 
  - Landing pages, User Dashboards, and Admin Dashboards.
  - Interactive "Find Parking" flows with filters.
  - Visual parking slot grid (showing Available, Reserved, Occupied).
  - Multi-step booking UI, digital ticket UI, and receipt UI.
  - Fully responsive components (Modals, Toasts, Tables, Cards).

### Phase 2: Flask Backend & Application Logic
**Goal:** Connect the UI to a robust Python backend.
- **What was done:** The Phase 1 HTML/CSS/JS was converted into Jinja2 templates. The application was restructured into Flask Blueprints (`auth`, `user`, `parking`, `booking`, `admin`, etc.).
- **Key Deliverables:**
  - Integrated `Flask-Login` for Admin and User role separation.
  - Built backend services (`fee_service.py`, `qr_service.py`, `pdf_service.py`) to handle complex business logic outside of routes.
  - Implemented secure CSRF protection on all forms using `Flask-WTF`.
  - Created the logic to generate real QR tokens and PDF files dynamically.
  - Implemented logic for calculating parking duration and fees.

### Phase 3: SQLite Database & Final Integration
**Goal:** Replace in-memory/mock data with a persistent SQLAlchemy relational database.
- **What was done:** Defined all database models, relationships, foreign keys, and constraints.
- **Key Deliverables:**
  - **Models:** `User`, `Vehicle`, `ParkingArea`, `ParkingSlot`, `Booking`, `Payment`, `PaymentPolicy`, `Notification`, and `SystemSetting`.
  - **Double Booking Prevention:** Implemented strict server-side checks to prevent two users from booking the same slot simultaneously.
  - **Automatic Expiry:** Logic to automatically expire bookings if a user fails to check-in on time, instantly freeing up the slot.
  - **Real-Time Consistency:** When an Admin checks a user in, the Booking turns `ACTIVE` and the Slot turns `OCCUPIED`. At check-out, the fee is calculated via DB policies, Payment is recorded, and the Slot returns to `AVAILABLE`.
  - **Seed Script:** Created `seed.py` to populate realistic demo data for immediate testing.

---

## 4. Detailed Database Schema

- **User:** `id`, `full_name`, `email`, `password_hash`, `role` (ADMIN/USER), `is_active`.
- **Vehicle:** `id`, `user_id` (FK), `vehicle_number`, `type` (Car, Bike, EV), `is_default`.
- **ParkingArea:** `id`, `name`, `location`, `operating_hours`, `floors`.
- **ParkingSlot:** `id`, `area_id` (FK), `slot_number`, `type` (Premium, Normal), `status` (Available, Occupied), `price`.
- **Booking:** The core transactional table. `id`, `user_id`, `vehicle_id`, `slot_id`. Tracks `entry_time`, `actual_entry_time`, `actual_exit_time`, `status`, and `qr_token`.
- **PaymentPolicy:** `id`, `hourly_rate`, `effective_from`, `effective_to`, `is_active`.
- **Payment:** `id`, `booking_id` (FK), `amount`, `method`, `transaction_id`.

---

## 5. Application Architecture

```text
SmartPark/
├── app/
│   ├── __init__.py              # Factory pattern, extensions init
│   ├── models.py                # SQLAlchemy Models
│   ├── routes/                  # Blueprints (Controllers)
│   │   ├── main.py              # Public routes
│   │   ├── auth.py              # Login/Register
│   │   ├── user.py              # Dashboard & Profiles
│   │   ├── parking.py           # Parking search API
│   │   ├── booking.py           # Reservation lifecycle
│   │   └── admin.py             # Admin dashboard & controls
│   ├── services/                # Business Logic
│   │   ├── fee_service.py       # Fee calculation logic
│   │   ├── qr_service.py        # qrcode generation
│   │   └── pdf_service.py       # ReportLab PDF creation
│   ├── static/                  # CSS, JS, Images, Generated assets
│   ├── templates/               # Jinja2 views
│   └── utils/
│       └── decorators.py        # @admin_required
├── instance/                    # SQLite Database
├── config.py                    # Environment configs
├── seed.py                      # Data seeder
├── run.py                       # App entry point
└── requirements.txt             # Python dependencies
```

---

## 6. Security & Error Handling
- **Authentication:** Passwords are never stored in plain text (Werkzeug PBKDF2 hashing).
- **Authorization:** strict `@admin_required` decorators protect sensitive routes. Booking details and receipts are protected so only the owner or an Admin can view them.
- **SQL Injection:** Entirely prevented by using SQLAlchemy ORM (no raw SQL).
- **CSRF:** Flask-WTF tokens on all POST endpoints.
- **Graceful Failures:** If SMTP (Email) is unconfigured, the app logs a warning but does not crash. Appropriate 403, 404, and 500 custom error pages are provided.

---

## 7. How to Run Locally

1. **Clone & Setup:**
   ```powershell
   git clone https://github.com/RajenderMohanVerma/SmartParking.git
   cd SmartParking
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
2. **Install Dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
3. **Environment:**
   Copy `.env.example` to `.env` and set a random string for `SECRET_KEY`.
4. **Initialize Database:**
   ```powershell
   python seed.py
   ```
5. **Run Application:**
   ```powershell
   python run.py
   ```
6. **Access:** Open `http://127.0.0.1:5000` in your browser.
   - Admin Login: `admin@smartpark.com` / `Admin@123`
   - User Login: `user@smartpark.com` / `User@123`
