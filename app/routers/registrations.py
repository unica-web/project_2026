from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.data.db import SessionDep
from app.models.event import Event
from app.models.registration import Registration
from app.models.user import User


router = APIRouter(tags=["registrations"])

# GET /registrations
@router.get("/registrations")
def get_registrations(session: SessionDep):
	"""
	Restituisce la lista di tutte le registrazioni esistenti.
	"""
	registrations = session.exec(select(Registration)).all()
	return registrations


# DELETE /registrations?username=...&event_id=...
@router.delete("/registrations")
def delete_registration(username: str, event_id: int, session: SessionDep):
	"""
	Elimina una singola registrazione, identificata tramite query parameter.
	"""
	event = session.get(Event, event_id)
	if event is None:
		raise HTTPException(status_code=404, detail="Event not found")

	user = session.get(User, username)
	if user is None:
		raise HTTPException(status_code=404, detail="User not found")

	registration = session.get(Registration, (username, event_id))
	if registration is None:
		raise HTTPException(status_code=404, detail="Registration not found")

	session.delete(registration)
	session.commit()
	return {"detail": "Registration deleted"}
