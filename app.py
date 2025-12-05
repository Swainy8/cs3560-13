from fastapi import FastAPI

app = FastAPI(title="Event Attendance Manager")

events = {}
attendees = {}

@app.get("/{event_id}/list")
def get_attendance_list(event_id: int):
    return attendees.get(event_id, [])

@app.get("/{event_id}/attendee/{id}")
def get_attendee(event_id: int, id: int):
    event_attendees = attendees.get(event_id, [])
    for a in event_attendees:
        if a["id"] == id:
            return a
    return {}

@app.post("/{event_id}/register")
def post_register(event_id: int, name: str, guests: int):
    if event_id not in attendees:
        attendees[event_id] = []
    new_id = len(attendees[event_id]) + 1
    attendee = {"id": new_id, "name": name, "guests": guests, "cancelled": False}
    attendees[event_id].append(attendee)
    return attendee

@app.post("/create")
def create_event(name: str, date: int):
    event_id = len(events) + 1
    events[event_id] = {"id": event_id, "name": name, "date": date, "goh": None, "latest": None}
    attendees[event_id] = []
    return events[event_id]

@app.put("/{event_id}/latest")
def put_latest(event_id: int, id: int):
    if event_id in events:
        events[event_id]["latest"] = id
    return events.get(event_id, {})

@app.put("/{event_id}/goh")
def put_guest_of_honor(event_id: int, id: int):
    if event_id in events:
        events[event_id]["goh"] = id
    return events.get(event_id, {})

@app.patch("/{event_id}/{id}/updateGuests/{guests}")
def update_guests(event_id: int, id: int, guests: int):
    if event_id in attendees:
        for a in attendees[event_id]:
            if a["id"] == id:
                a["guests"] = guests
                return a
    return {}

@app.patch("/{event_id}/{id}/cancel")
def cancel_attendance(event_id: int, id: int):
    if event_id in attendees:
        for a in attendees[event_id]:
            if a["id"] == id:
                a["cancelled"] = True
                return a
    return {}

@app.delete("/{event_id}/cancel")
def cancel_event(event_id: int):
    if event_id in events:
        del events[event_id]
        del attendees[event_id]
        return {"status": "deleted"}
    return {"status": "not found"}

@app.delete("/{event_id}/clearAttendance")
def clear_attendance(event_id: int):
    if event_id in attendees:
        attendees[event_id] = []
    return {"status": "cleared"}
