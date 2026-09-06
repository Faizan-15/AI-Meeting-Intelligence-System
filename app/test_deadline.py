from datetime import date

from services.deadline_service import normalize_deadline


meeting_date = date(2026, 9, 3)


print("\nDEADLINE TESTS:\n")

print("Friday:", normalize_deadline("Friday", meeting_date))
print("Tomorrow:", normalize_deadline("Tomorrow", meeting_date))
print("Monday:", normalize_deadline("Monday", meeting_date))
print("Next Monday:", normalize_deadline("Next Monday", meeting_date))
print("September 10:", normalize_deadline("September 10", meeting_date))
print("End of month:", normalize_deadline("end of month", meeting_date))
print("Missing:", normalize_deadline("", meeting_date))