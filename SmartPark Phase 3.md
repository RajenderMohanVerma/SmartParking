# SMARTPARK – PHASE 3
# SQLITE DATABASE + SQLALCHEMY + FINAL INTEGRATION

You are continuing the EXACT SAME project:

**SmartPark – Smart Parking Management System**

Phase 1:
Complete Frontend

Phase 2:
Flask Backend

Now implement:

Phase 3:
**SQLite Database + SQLAlchemy + Complete Final Integration**

DO NOT create a new project.

DO NOT delete the existing frontend.

DO NOT rebuild the application.

Connect the existing Flask backend to SQLite.

---

# 1. DATABASE TECHNOLOGY

Use:

- SQLite
- SQLAlchemy
- Flask-SQLAlchemy

Database:

instance/smartpark.db

Use ORM models.

Do not write unnecessary raw SQL.

---

# 2. DATABASE MODELS

Create proper models for:

### User

Fields:

- id
- full_name
- username
- email
- phone
- password_hash
- role
- profile_photo
- address
- is_active
- email_verified
- created_at
- updated_at

---

### Vehicle

Fields:

- id
- user_id
- vehicle_number
- vehicle_type
- brand
- model
- color
- fuel_type
- notes
- is_default
- created_at

Relationship:

User → Vehicles

---

### ParkingArea

Fields:

- id
- name
- location
- description
- floors
- operating_hours
- status
- created_at
- updated_at

---

### ParkingSlot

Fields:

- id
- area_id
- slot_number
- floor
- slot_type
- vehicle_type
- price
- status
- location_info
- created_at
- updated_at

Relationship:

ParkingArea → ParkingSlots

---

### Booking

Fields:

- id
- booking_id
- user_id
- vehicle_id
- parking_area_id
- parking_slot_id
- booking_date
- entry_time
- expected_exit_time
- actual_entry_time
- actual_exit_time
- estimated_fee
- final_fee
- status
- qr_token
- created_at
- updated_at

---

### Payment

Fields:

- id
- transaction_id
- booking_id
- amount
- payment_method
- status
- paid_at
- created_at

---

### Pricing

Fields:

- id
- name
- vehicle_type
- slot_type
- hourly_price
- additional_hour_price
- daily_price
- grace_period_minutes
- is_active
- created_at
- updated_at

---

### Notification

Fields:

- id
- user_id
- title
- message
- type
- is_read
- created_at

---

### PasswordResetToken

Fields:

- id
- user_id
- token
- expires_at
- used
- created_at

---

### SystemSetting

Create settings for:

- Parking name
- Contact email
- Contact phone
- Operating hours
- Booking expiry
- Grace period
- Notification settings

---

# 3. DATABASE RELATIONSHIPS

Implement proper relationships:

User
→ Vehicles

User
→ Bookings

User
→ Notifications

ParkingArea
→ ParkingSlots

Booking
→ User

Booking
→ Vehicle

Booking
→ ParkingArea

Booking
→ ParkingSlot

Booking
→ Payment

Use foreign keys.

Use cascade behavior carefully.

---

# 4. CONSTRAINTS

Implement database constraints for:

- Unique email
- Unique username
- Unique vehicle number where appropriate
- Unique slot number within parking area
- Unique booking ID
- Unique transaction ID
- Unique QR token

---

# 5. INDEXES

Add indexes where useful:

- User email
- Username
- Booking ID
- Vehicle number
- Booking status
- Slot status
- Booking date
- Transaction ID

---

# 6. DATABASE INITIALIZATION

Create a clean database initialization system.

Support:

- Create tables
- Database initialization
- Database reset for development
- Seed demo data

Do not destroy existing data automatically.

---

# 7. SEED DATA

Create realistic demo data.

Example:

Admin:
admin@smartpark.com

User:
user@smartpark.com

Add sample:

- Users
- Vehicles
- Parking areas
- Parking slots
- Pricing
- Notifications
- Example bookings

Passwords must be securely hashed.

---

# 8. REAL SLOT AVAILABILITY

Replace all frontend demo slot data with real SQLite data.

When slot is:

AVAILABLE

show green.

When:

RESERVED

show yellow.

When:

OCCUPIED

show red.

When:

MAINTENANCE

show appropriate state.

Frontend must retrieve actual backend/database state.

---

# 9. REAL BOOKING SYSTEM

Booking must now be database-backed.

When user books:

1. Validate user
2. Validate vehicle
3. Validate parking area
4. Validate slot
5. Check slot availability
6. Check overlapping booking
7. Calculate estimated fee
8. Create booking
9. Generate booking ID
10. Generate QR token
11. Save booking
12. Update slot status
13. Create notification
14. Send email if configured

All operations must be handled safely.

---

# 10. DOUBLE BOOKING PREVENTION

This is critical.

Prevent two users from booking the same slot for overlapping times.

Perform server-side checks.

Do not rely only on frontend availability.

If two users attempt to book simultaneously:

Only one should successfully reserve the slot.

Return a proper error for the other user.

---

# 11. BOOKING EXPIRY

Use database timestamps.

Find expired bookings.

Update:

Booking:
EXPIRED

Slot:
AVAILABLE

Create notification.

Send email if configured.

Do not allow expired booking check-in.

---

# 12. CHECK-IN DATABASE FLOW

When QR is verified:

Validate:

- QR token
- Booking
- User
- Booking status
- Expiry
- Slot

Then:

Booking:
ACTIVE

Slot:
OCCUPIED

Save:

actual_entry_time

Create notification.

---

# 13. CHECK-OUT DATABASE FLOW

At checkout:

Save:

actual_exit_time

Calculate:

parking duration

Calculate:

final fee

Create payment record.

Update:

Booking = COMPLETED

Slot = AVAILABLE

Generate receipt.

Create notification.

Send email.

---

# 14. FEE CALCULATION FROM DATABASE

Pricing must come from Pricing table.

Do not hard-code prices.

Support:

- Hourly
- Additional hourly
- Daily
- VIP
- EV
- Vehicle-specific
- Grace period

Calculate accurately based on actual timestamps.

---

# 15. PAYMENT DATABASE

Every payment must be stored.

Fields:

- Transaction ID
- Booking
- Amount
- Method
- Status
- Date

Payment history must be visible to user and admin.

---

# 16. QR DATABASE INTEGRATION

QR must be connected to real booking records.

QR token:

- Unique
- Secure
- Non-sensitive

Verification must retrieve booking from database.

---

# 17. PDF RECEIPTS

Generate PDF from actual database information.

Do not use hard-coded receipt values.

Receipt must contain actual:

- User
- Vehicle
- Booking
- Slot
- Entry
- Exit
- Duration
- Amount
- Payment
- Transaction ID

---

# 18. EMAIL DATABASE EVENTS

Trigger emails based on actual database events:

- Registration
- Verification
- Booking
- Cancellation
- Expiry
- Check-in
- Check-out
- Payment
- Password reset

---

# 19. NOTIFICATIONS

Save all notifications in SQLite.

Connect Phase 1 notification UI to database.

Support:

- Read
- Unread
- Mark all read
- Delete

---

# 20. ADMIN DATABASE OPERATIONS

Admin dashboard must use real database data.

Statistics must be calculated from SQLite.

Examples:

Total users:
COUNT(users)

Available slots:
COUNT(slots WHERE status='available')

Revenue:
SUM(payments.amount)

Bookings:
COUNT(bookings)

Do not use fake dashboard numbers.

---

# 21. REPORTS

Generate reports from real database records.

Reports:

- Daily
- Weekly
- Monthly
- Revenue
- Occupancy
- Booking
- User activity

Filters must query SQLite.

---

# 22. ANALYTICS

Calculate actual:

- Peak parking hours
- Most used area
- Most used slot type
- Average parking duration
- Average revenue
- Cancellation rate
- Occupancy percentage

Feed real values to Chart.js.

---

# 23. SEARCH AND FILTERS

Connect all Phase 1 filters to database queries.

Users:
- Name
- Email
- Phone

Bookings:
- Booking ID
- Vehicle number
- Status
- Date
- Area

Parking:
- Area
- Slot
- Status
- Type

Payments:
- Transaction ID
- Method
- Status
- Date

Implement pagination.

---

# 24. DATABASE ERROR HANDLING

Handle:

- IntegrityError
- Invalid foreign keys
- Missing records
- Duplicate records
- Transaction failures
- Database connection issues

Never expose raw SQL/database errors to users.

---

# 25. MIGRATION SUPPORT

If Flask-Migrate is being used, configure migrations properly.

The database schema should be maintainable.

Do not manually recreate the database every time the application starts.

---

# 26. COMPLETE END-TO-END TEST

Now test the ENTIRE APPLICATION.

## USER FLOW

Register
→ Verify email
→ Login
→ Dashboard
→ Add vehicle
→ Find parking
→ Search/filter
→ Select slot
→ Book
→ Booking confirmation
→ QR generated
→ Ticket
→ Check-in
→ Active parking
→ Check-out
→ Fee calculation
→ Payment
→ Receipt
→ PDF
→ Notification
→ Booking history

---

# 27. ADMIN FLOW

Login
→ Dashboard
→ Users
→ Parking Areas
→ Slots
→ Pricing
→ Bookings
→ Payments
→ Reports
→ Analytics
→ Notifications
→ Settings

All information must come from SQLite.

---

# 28. SECURITY AUDIT

Check:

- Password hashing
- CSRF
- Authorization
- Authentication
- SQL injection protection
- Session security
- File upload security
- Environment variables
- Secret keys
- Error handling

---

# 29. UI AUDIT

Do not damage Phase 1 UI.

Verify:

- Light mode
- Dark mode
- Mobile
- Tablet
- Desktop
- Forms
- Tables
- Modals
- Toasts
- Loading states
- Error states
- Empty states
- Charts

---

# 30. FUNCTIONAL AUDIT

Check EVERY:

- Button
- Link
- Form
- API
- Route
- Database operation
- CRUD operation
- Search
- Filter
- Pagination
- QR
- PDF
- Email
- Notification

No dummy functionality should remain.

---

# 31. REMOVE MOCK DATA

After SQLite integration:

REMOVE unnecessary frontend mock/demo data.

All production application information must come from:

Flask → SQLAlchemy → SQLite

Use demo data only through the database seed system.

---

# 32. FINAL PROJECT STRUCTURE

Maintain one clean project:

smartpark/

app/
    __init__.py
    models.py

    routes/
    services/
    utils/

    templates/
    static/

instance/
    smartpark.db

tests/

config.py
run.py
requirements.txt
.env.example
README.md
.gitignore

---

# 33. FINAL REQUIREMENT

The final result must be ONE fully integrated application:

HTML
↓
CSS
↓
JavaScript
↓
Bootstrap
↓
Flask
↓
SQLAlchemy
↓
SQLite

Every major feature must work through this architecture.

---

# 34. FINAL QUALITY STANDARD

The final SmartPark project must be:

- Fully functional
- Professional
- Responsive
- Secure
- Database-driven
- API-connected
- Modern UI
- Dark/Light mode
- QR enabled
- PDF enabled
- Email enabled
- Notification enabled
- Searchable
- Filterable
- Report-enabled
- Analytics-enabled
- Admin controlled
- Easy enough for an MCA student to understand

It must be suitable for:

**MCA 1st Semester Minor Project**

and should be easy to explain during:

- Project demonstration
- Viva
- Faculty evaluation

---

# 35. FINAL COMMAND

DO NOT just tell me what is wrong.

Inspect the complete existing project.

Run it.

Test it.

Find errors.

Fix errors.

Check frontend.

Check Flask routes.

Check database.

Check APIs.

Check JavaScript.

Check forms.

Check authentication.

Check authorization.

Check booking logic.

Check QR.

Check PDF.

Check email.

Check notifications.

Check admin.

Check responsive design.

Check dark mode.

Fix everything required.

Do not leave known errors unresolved.

Do not create a new project.

Do not break existing working functionality.

The final output must be the completed **SmartPark – Smart Parking Management System** with Phase 1 + Phase 2 + Phase 3 fully integrated into ONE project.