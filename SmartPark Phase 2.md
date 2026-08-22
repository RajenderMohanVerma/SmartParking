# SMARTPARK – PHASE 2
# FLASK BACKEND & APPLICATION LOGIC

You are continuing the EXACT SAME project created in Phase 1:

**SmartPark – Smart Parking Management System**

DO NOT create a new project.

DO NOT rebuild the frontend from scratch.

DO NOT remove the existing frontend.

The Phase 1 frontend already exists.

Your job is to add a professional Flask backend and connect the existing frontend to it.

---

# 1. CORE RULE

Preserve the existing:

- HTML
- CSS
- JavaScript
- Bootstrap
- Components
- Page structure
- UI design
- Dark/light mode
- Responsive design

Connect them to Flask.

Do not unnecessarily redesign working frontend pages.

---

# 2. BACKEND STACK

Use:

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-Mail
- Flask-WTF
- Werkzeug
- Jinja2
- python-dotenv

Additional packages:

- qrcode
- Pillow
- ReportLab
- email-validator

Use Flask Blueprints.

---

# 3. BACKEND ARCHITECTURE

Create:

app/
    __init__.py
    models.py

    routes/
        auth.py
        user.py
        parking.py
        booking.py
        payment.py
        notification.py
        admin.py

    services/
        booking_service.py
        fee_service.py
        qr_service.py
        pdf_service.py
        email_service.py
        notification_service.py

    utils/
        validators.py
        decorators.py

    templates/
    static/

config.py
run.py
requirements.txt
.env.example

Keep business logic separate from routes wherever practical.

---

# 4. FLASK APPLICATION

Create Flask application factory.

Configure:

- Secret key
- Session
- SQLAlchemy
- Login manager
- Mail
- CSRF
- Upload folders
- Generated file folders

Use environment variables.

---

# 5. AUTHENTICATION

Implement real authentication.

Features:

- Register
- Login
- Logout
- Password hashing
- Remember me
- Forgot password
- Password reset
- Email verification
- Session management
- Role-based access

Use Flask-Login.

Use secure password hashing.

---

# 6. USER ROUTES

Connect frontend pages to backend.

Implement routes for:

- Dashboard
- Profile
- Vehicles
- Bookings
- Parking search
- Notifications
- Active parking
- Receipts

---

# 7. PARKING SYSTEM

Implement:

- Parking area management
- Slot management
- Slot status
- Availability
- Search
- Filters

Create API endpoints for dynamic availability.

Use fetch/AJAX from the Phase 1 frontend.

---

# 8. BOOKING ENGINE

Implement actual booking logic.

Flow:

Select parking
→ Select slot
→ Select vehicle
→ Select time
→ Validate availability
→ Calculate estimated fee
→ Create booking
→ Generate booking ID
→ Confirm booking

Prevent double booking.

Validate everything server-side.

---

# 9. BOOKING EXPIRY

Implement automatic expiry logic.

If booking is not checked in within configured time:

Booking = EXPIRED

Slot = AVAILABLE

Ensure expired bookings do not block slots.

---

# 10. QR SYSTEM

Implement actual QR generation.

Generate secure QR token.

QR should reference booking securely.

Do not expose sensitive personal information.

Implement:

- QR generation
- QR download
- QR verification
- Manual booking ID verification

---

# 11. CHECK-IN

Implement:

- QR verification
- Booking verification
- Expiry validation
- Status validation
- Check-in timestamp
- Booking = ACTIVE
- Slot = OCCUPIED

Return appropriate success/error responses to frontend.

---

# 12. CHECK-OUT

Implement:

- Exit timestamp
- Parking duration
- Fee calculation
- Payment record
- Booking completion
- Slot release
- Receipt generation
- Notification
- Email

All operations must remain consistent.

---

# 13. FEE CALCULATION

Create a reusable fee calculation service.

Support:

- Hourly price
- Additional hourly price
- Daily pricing
- VIP pricing
- EV pricing
- Vehicle-specific pricing
- Grace period

Pricing should come from configuration/database later.

Do not hard-code pricing inside multiple routes.

---

# 14. PAYMENT

Implement payment record management.

For this academic project:

Use simulated payment processing.

Do NOT pretend it is real banking/payment processing.

Create:

- Transaction ID
- Booking ID
- Amount
- Method
- Status
- Timestamp

---

# 15. QR TICKET

Generate digital parking ticket data.

Connect the Phase 1 ticket page.

Provide:

- Booking information
- QR code
- Parking information
- Vehicle
- Entry/exit
- Estimated fee

---

# 16. PDF RECEIPT

Implement ReportLab PDF generation.

Connect Phase 1:

**Download PDF Receipt**

button.

Generate professional receipt.

---

# 17. EMAIL

Implement Flask-Mail.

Support:

- Registration
- Verification
- Booking confirmation
- Cancellation
- Expiry
- Check-in
- Check-out
- Payment
- Password reset

Use .env credentials.

If SMTP is unavailable:

Do not crash the application.

Log a safe development message instead.

---

# 18. NOTIFICATIONS

Implement backend notification creation.

Create notifications when:

- Booking created
- Booking confirmed
- Booking cancelled
- Booking expired
- Check-in
- Check-out
- Payment completed

Connect notification UI from Phase 1.

---

# 19. ADMIN BACKEND

Implement admin routes.

Admin can:

- Manage users
- Manage parking areas
- Manage slots
- Manage pricing
- Manage bookings
- Manage payments
- Manage reports
- Manage analytics
- Manage notifications
- Manage settings

Protect all admin routes.

---

# 20. DASHBOARD APIs

Create endpoints for:

- Total users
- Total slots
- Available slots
- Occupied slots
- Reserved slots
- Active bookings
- Today's bookings
- Today's revenue
- Monthly revenue
- Occupancy
- Analytics

Connect these to Phase 1 Chart.js dashboards.

---

# 21. SEARCH/FILTER APIs

Implement backend search/filtering for:

Users
Bookings
Parking
Slots
Payments

Support pagination.

Do not load unnecessary large datasets.

---

# 22. VALIDATION

Implement server-side validation for every form.

Never trust frontend data.

Validate:

- Email
- Password
- Phone
- Vehicle number
- Dates
- Times
- Slot
- Booking
- Payment
- File uploads

---

# 23. SECURITY

Implement:

- CSRF
- Password hashing
- Authentication
- Authorization
- SQL injection prevention
- Secure sessions
- Input validation
- Secure file uploads
- Environment variables
- Safe error handling

---

# 24. ERROR HANDLING

Implement:

400
401
403
404
500

Return either proper HTML error pages or JSON errors for API requests.

Do not expose stack traces to users.

---

# 25. CONNECT FRONTEND

Now connect every Phase 1 page to Flask.

Replace demo data with backend data.

Connect:

- Login
- Registration
- Dashboard
- Parking
- Slots
- Booking
- QR
- Check-in
- Check-out
- Payment
- Receipts
- Vehicles
- Notifications
- Admin
- Reports
- Analytics

Do not create duplicate pages.

---

# 26. FINAL BACKEND TEST

Test the complete flow:

Register
→ Login
→ Add Vehicle
→ Find Parking
→ Select Slot
→ Book
→ QR
→ Check-in
→ Active Parking
→ Check-out
→ Fee
→ Payment
→ Receipt
→ Notification

Also test:

- Cancellation
- Expiry
- Double booking
- Unauthorized access
- Admin access

Fix all errors.

DO NOT start Phase 3 until the backend is properly integrated with the existing frontend.

---

# 27. PROJECT CONTINUITY

This remains the SAME SmartPark project.

Phase 1 frontend must remain intact.

Phase 2 adds Flask backend.

Phase 3 will add/connect SQLite database.

Do not create a second project.

Do not replace working UI unnecessarily.

At the end of Phase 2, the application should have:

Frontend + Flask backend + temporary/in-memory/mock persistence where necessary.

Prepare all models and database interfaces so Phase 3 can connect SQLite cleanly.

Wait for Phase 3.