from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def receipt_pdf(booking):
    output = BytesIO()
    document = canvas.Canvas(output, pagesize=A4)
    document.setTitle(f"SmartPark receipt {booking.booking_id}")
    document.setFont("Helvetica-Bold", 22)
    document.drawString(60, 780, "SmartPark")
    document.setFont("Helvetica", 11)
    document.drawString(60, 755, "Digital parking receipt")
    details = [("Receipt / booking", booking.booking_id), ("Customer", booking.user.full_name), ("Vehicle", booking.vehicle.vehicle_number), ("Parking area", booking.area.name), ("Slot", booking.slot.slot_number), ("Entry", str(booking.actual_entry_time or booking.entry_time)), ("Exit", str(booking.actual_exit_time or "-")), ("Amount", f"INR {booking.final_fee or booking.estimated_fee:.2f}"), ("Status", booking.status)]
    y = 700
    for label, value in details:
        document.setFont("Helvetica-Bold", 10)
        document.drawString(70, y, label)
        document.setFont("Helvetica", 10)
        document.drawString(220, y, value)
        y -= 28
    document.setFont("Helvetica-Oblique", 9)
    document.drawString(60, 80, "Thank you for choosing SmartPark.")
    document.save()
    output.seek(0)
    return output
