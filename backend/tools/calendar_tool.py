from googleapiclient.discovery import build

from tools.gmail_tool import gmail_authenticate


def create_calendar_event(
    title,
    start_time,
    end_time
):

    creds = gmail_authenticate()

    service = build(
        "calendar",
        "v3",
        credentials=creds
    )

    event = {

        "summary": title,

        "start": {

            "dateTime": start_time.isoformat(),

            "timeZone": "UTC",
        },

        "end": {

            "dateTime": end_time.isoformat(),

            "timeZone": "UTC",
        },
    }

    created_event = service.events().insert(

        calendarId="primary",

        body=event

    ).execute()

    print("Event Created:")
    print(created_event.get("htmlLink"))

    return created_event.get("htmlLink")