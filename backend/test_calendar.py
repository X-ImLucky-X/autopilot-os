from datetime import datetime, timedelta

from tools.calendar_tool import create_calendar_event


start = datetime.now() + timedelta(hours=1)

end = start + timedelta(hours=3)


link = create_calendar_event(
    "happy b day",
    start,
    end
)

print("Event Created:")
print(link)