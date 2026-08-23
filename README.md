<div align="center">

<img src="app/static/images/smartpark-logo.png" alt="SmartPark Logo" width="90" height="90" />

# SmartPark

### Smart Parking Management System

**Find a space · Reserve it · Park without friction**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-336791?style=flat-square&logo=postgresql&logoColor=white)](https://neon.tech)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=flat-square&logo=bootstrap&logoColor=white)](https://getbootstrap.com)
[![Vercel](https://img.shields.io/badge/Deployed-Vercel-000000?style=flat-square&logo=vercel&logoColor=white)](https://smart-parking-three-henna.vercel.app)
[![License](https://img.shields.io/badge/License-MIT-14ac52?style=flat-square)](LICENSE)

---

🌐 **Live Demo:** [smart-parking-three-henna.vercel.app](https://smart-parking-three-henna.vercel.app)

| Role | Email | Password |
|------|-------|----------|
| 👑 Admin | `admin@smartpark.com` | `Admin@123` |
| 👤 User | `user@smartpark.com` | `User@123` |

</div>

---

## What is SmartPark?

SmartPark is a full-stack parking management platform built as an MCA Minor Project. It covers the complete lifecycle of a parking session — from finding and reserving a slot, to getting a secure QR pass, checking in, parking, checking out, and receiving a digital receipt.

The system has two sides:

- **Users** discover live parking areas, reserve a slot, carry a digital QR pass, and track their history and payments.
- **Admins** manage parking areas and slots, verify QR passes at entry, check vehicles in and out, set fee rates and policies, and monitor the full payment ledger.

> Parking session fees only — no website subscription. Admin controls when fees are active and how much they are.

---

## Screenshots

| Landing Page | User Dashboard | Parking Search |
|:---:|:---:|:---:|
| Find spaces, see live lot preview | Your bookings, stats, live session | Browse areas, slot grid, book now |

| Booking Pass | Admin Dashboard | Admin Slots |
|:---:|:---:|:---:|
| QR pass + receipt download | Live stats, check-in/out controls | Bulk add slots, inline edit |

---

## Feature Overview

### User Features

| Feature | Details |
|---------|---------|
| 🔐 Authentication | Register, login, remember-me, forgot/reset password |
| 🚗 Vehicle Garage | Add multiple vehicles, set default, remove |
| 🅿️ Parking Search | Filter by area, slot type, live availability |
| 📅 Reservations | Pick slot, vehicle, entry/exit window, fee estimate |
| 📱 QR Pass | Secure QR generated on booking confirmation |
| 🧾 Digital Receipt | PDF receipt downloadable at any time |
| 📊 Dashboard | Booking history, live session banner, status filters |
| 🔔 Notifications | In-app alerts for bookings, payments, updates |
| 💳 Payment History | All parking fees with transaction IDs |
| 👤 Profile | Edit name, phone, address |
| 🌗 Dark / Light Mode | Persisted browser preference |
| 📲 PWA | Installable on mobile and desktop |

### Admin Features

| Feature | Details |
|---------|---------|
| 🏢 Area Management | Create, edit, activate/deactivate parking areas |
| 🗂️ Slot Management | Single or bulk-add slots (e.g. A01–A20 in one click) |
| 🔍 QR Verification | Scan or enter booking ID to verify pass |
| ✅ Check-in / Check-out | Start and end parking sessions |
| 💰 Payment Policies | Set fee rates, duration (months/years), activate/deactivate |
| 📋 Payment Ledger | Full history with date filter, totals, method badges |
| 🧑‍💼 User Management | View, search, activate/deactivate accounts |
| 📈 Reports | Revenue, occupancy, booking status charts |
| 🎛️ Fee Control | Toggle free parking globally (admin system setting) |

---

## User Flow

```
Register / Login
      │
      ▼
Add Vehicle (once)
      │
      ▼
Browse Parking → Filter by type/area
      │
      ▼
Reserve a Slot → Pick vehicle + time window
      │
      ▼
Booking Confirmed → QR Pass generated
      │
      ▼
Arrive → Admin scans QR → Check In
      │
      ▼
Park ── Live session tracked ──────────────┐
      │                                    │
      ▼                                    ▼
Admin: Check Out → Fee calculated     Download Receipt
      │
      ▼
Payment recorded → Notification sent
```

---

## Admin Flow

```
Admin Login → /admin/dashboard
      │
      ├── Areas → Create area (name, location, floors, hours)
      │      └── Slots → Bulk add A01–A20 in one click
      │
      ├── Verify QR → Scan booking QR → Check In
      │
      ├── Dashboard → See active sessions → Check Out
      │
      ├── Payment Policies → Set ₹30/hr rate, 6-month validity, activate
      │
      └── Payments → Full ledger, date filter, today's revenue
```

---

## Technology Stack

### Backend
- **Python 3.10+** with **Flask 3.1** (Application Factory pattern)
- **SQLAlchemy** ORM with **PostgreSQL** (Neon) in production, SQLite locally
- **Flask-Login** — session management and role-based access
- **Flask-WTF** — CSRF protection on all forms
- **Flask-Mail** — SMTP email with graceful local fallback
- **Werkzeug** — secure password hashing
- **qrcode + Pillow** — QR image generation
- **ReportLab** — PDF receipt generation
- **psycopg2-binary** — PostgreSQL adapter

### Frontend
- **Bootstrap 5.3** + **Bootstrap Icons**
- Custom CSS design system with CSS variables for light/dark theming
- Vanilla JavaScript — no framework overhead
- CSS animations, spring transitions, responsive breakpoints
- PWA — manifest, service worker, install prompt

### Infrastructure
- **Vercel** — serverless deployment
- **Neon** — serverless PostgreSQL
- **GitHub** — version control and CI/CD trigger

---

## Project Structure

```
SmartPark/
├── app/
│   ├── __init__.py              # Flask factory, extensions, context processors
│   ├── models.py                # All SQLAlchemy models
│   ├── routes/
│   │   ├── main.py              # Home, roles page
│   │   ├── auth.py              # Register, login, logout, password reset
│   │   ├── user.py              # Dashboard, vehicles, profile, notifications
│   │   ├── parking.py           # Parking search, slot API
│   │   ├── booking.py           # New booking, detail, QR, receipt, cancel
│   │   ├── admin.py             # Admin dashboard, areas, slots, payments, reports
│   │   ├── payment.py           # User payment history
│   │   └── notification.py      # Notification endpoints
│   ├── services/
│   │   ├── fee_service.py       # Fee calculation, free-parking toggle
│   │   ├── notification_service.py  # In-app notification creator
│   │   ├── email_service.py     # SMTP email dispatcher
│   │   ├── qr_service.py        # QR image generator
│   │   └── pdf_service.py       # PDF receipt generator
│   ├── templates/
│   │   ├── base.html            # Shared layout, nav, footer, theme toggle
│   │   ├── home.html            # Landing page
│   │   ├── auth/                # Login, register, forgot/reset password
│   │   ├── user/                # Dashboard, vehicles, profile, notifications, payments
│   │   ├── booking/             # New reservation, booking detail/QR pass
│   │   ├── parking/             # Live parking search
│   │   ├── admin/               # All admin pages
│   │   └── errors/              # 403, 404, 500 pages
│   ├── static/
│   │   ├── css/                 # Modular CSS files
│   │   ├── js/                  # app.js, experience.js
│   │   ├── images/              # Logo assets
│   │   └── generated/           # Runtime QR and PDF files
│   └── utils/
│       └── decorators.py        # @admin_required decorator
├── instance/                    # Local SQLite database (gitignored)
├── tests/
│   └── test_app.py              # Regression tests
├── config.py                    # Environment-based Config class
├── seed.py                      # Demo data initialization
├── run.py                       # App entry point + admin seed route
├── vercel.json                  # Vercel deployment config
├── requirements.txt             # Python dependencies
└── .env.example                 # Environment variable template
```

---

## Database Models

```
User ──────────── Vehicle
  │                  │
  │                  │
  └──── Booking ─────┘
           │
           ├── ParkingArea ──── ParkingSlot
           │
           └── Payment ──── PaymentPolicy

+ Notification (User)
+ Pricing (fee rate cards)
+ SystemSetting (free parking toggle)
+ PasswordResetToken
```

---

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| `GET` | `/` | Landing page |
| `GET/POST` | `/auth/register` | User registration |
| `GET/POST` | `/auth/login` | Login |
| `POST` | `/auth/logout` | Logout |
| `GET/POST` | `/auth/forgot-password` | Password reset request |
| `GET/POST` | `/auth/reset-password/<token>` | Set new password |
| `GET` | `/user/dashboard` | User booking dashboard |
| `GET/POST` | `/user/vehicles` | Vehicle management |
| `GET/POST` | `/user/profile` | Profile edit |
| `GET` | `/user/notifications` | Notification center |
| `GET` | `/parking` | Live parking search |
| `GET` | `/parking/api/slots` | Slot availability JSON |
| `GET` | `/parking/api/directory` | Area directory JSON |
| `GET/POST` | `/bookings/new` | Create reservation |
| `GET` | `/bookings/<id>` | Booking detail + QR pass |
| `GET` | `/bookings/<id>/qr` | Download QR image |
| `GET` | `/bookings/<id>/receipt` | Download PDF receipt |
| `POST` | `/bookings/<id>/cancel` | Cancel a booking |
| `GET` | `/admin/dashboard` | Admin operations dashboard |
| `GET/POST` | `/admin/areas` | Parking area management |
| `GET/POST` | `/admin/slots` | Slot management + bulk add |
| `GET/POST` | `/admin/payments` | Payment ledger with date filter |
| `GET/POST` | `/admin/pricing` | Fee rate cards |
| `GET/POST` | `/admin/payment-policies` | Fee policies |
| `GET` | `/admin/users` | User management |
| `GET` | `/admin/verify` | QR verification |
| `GET` | `/admin/reports` | Revenue and occupancy reports |
| `GET` | `/admin/seed-demo` | ⚙️ Seed demo parking data (admin only) |
| `GET` | `/payments` | User payment history |

---

## Local Setup

### Prerequisites
- Python 3.10 or newer
- Git

### Steps

```powershell
# 1. Clone the repo
git clone https://github.com/RajenderMohanVerma/SmartParking.git
cd SmartParking

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1     # Windows PowerShell
# source .venv/bin/activate    # Mac / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment
copy .env.example .env
# Edit .env — set SECRET_KEY at minimum

# 5. Seed demo data
python seed.py

# 6. Run
python run.py
```

Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## Environment Variables

```env
# Required
SECRET_KEY=your-long-random-secret-key

# Database (defaults to SQLite locally)
DATABASE_URL=sqlite:///instance/smartpark.db
# For PostgreSQL (Neon/Railway/Render):
# DATABASE_URL=postgresql://user:pass@host/db?sslmode=require

# Email (optional — app works without it)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your@gmail.com

# Vercel deployment marker
VERCEL=1
```

---

## Vercel Deployment

This project is deployed on **Vercel** with **Neon PostgreSQL**.

### Deploy your own

1. Fork this repo
2. Create a free database at [neon.tech](https://neon.tech)
3. Import repo on [vercel.com](https://vercel.com)
4. Add environment variables (see table above)
5. Deploy — Vercel auto-deploys on every `git push`
6. After first deploy, visit `/admin/seed-demo` to seed demo data

---

## Security

- Passwords hashed with **Werkzeug PBKDF2**
- All mutating forms protected with **Flask-WTF CSRF tokens**
- **SQLAlchemy ORM** — no raw SQL interpolation
- Admin routes protected by `@admin_required` decorator
- Booking QR, receipt, and detail access is owner-or-admin only
- SMTP credentials loaded from environment variables only
- `SECRET_KEY` and `DATABASE_URL` never committed to git

---

## Testing

```powershell
python -m pytest -q
```

Current test suite covers:
- User registration and login
- Authenticated booking creation
- Database persistence
- Slot reservation state changes
- Admin pricing page access

---

## Payment Policy Design

SmartPark uses a **parking-session fee only** model:

- Users **never pay a website subscription**
- Admin sets fee rates via **Payment Policies** (amount + duration)
- Admin can enable **free parking** globally with one toggle
- Policy has `effective_from` / `effective_to` dates — admin controls when it activates
- At checkout, fee = 0 if free-parking is ON, else calculated from slot price + duration

```
Admin sets policy: ₹30/hr · active for 6 months from 1 Jan
         ↓
User parks → session tracked
         ↓
Admin checks out → fee auto-calculated → Payment record created
         ↓
User receives notification + can download PDF receipt
```

---

## Roadmap

- [x] Authentication (register, login, password reset)
- [x] Vehicle management
- [x] Parking area and slot CRUD
- [x] Bulk slot creation
- [x] Reservation with fee estimation
- [x] Secure QR pass generation
- [x] Admin check-in / check-out
- [x] Payment recording and ledger
- [x] PDF receipts
- [x] In-app notifications
- [x] Dark / light mode
- [x] PWA (installable)
- [x] PostgreSQL + Vercel deployment
- [ ] Payment gateway integration (Razorpay / Stripe)
- [ ] Real-time slot updates (WebSocket)
- [ ] Advanced analytics dashboard
- [ ] Profile photo upload
- [ ] Multi-language support

---

## Academic Context

SmartPark is developed as an **MCA Minor Project** and demonstrates:

| Concept | Implementation |
|---------|---------------|
| MVC Architecture | Flask blueprints, Jinja2 templates, SQLAlchemy models |
| ORM & Relationships | User → Vehicle → Booking → Payment chain |
| Authentication | Werkzeug hashing, Flask-Login sessions |
| Authorization | Role-based `@admin_required`, owner checks |
| CSRF Protection | Flask-WTF on all POST forms |
| File Generation | QR images (qrcode + Pillow), PDFs (ReportLab) |
| Email Service | Flask-Mail with SMTP, graceful fallback |
| Frontend Design | CSS variables, Bootstrap 5, responsive + dark mode |
| PWA | Service worker, manifest, install prompt |
| Deployment | Vercel serverless + Neon PostgreSQL |
| Testing | Pytest regression suite |

---

<div align="center">

Built with ❤️ for MCA Minor Project · 2026

[🌐 Live Demo](https://smart-parking-three-henna.vercel.app) · [📁 GitHub](https://github.com/RajenderMohanVerma/SmartParking)

</div>
