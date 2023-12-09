#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import datetime
from models import db, Doctor, Patient, Appointment

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.get("/")
def index():
    return "doctor/patient"

@app.get('/appointments')
def get_appointments():
    apps = Appointment.query.all()
    data = [app.to_dict() for app in apps]
    return make_response(jsonify(data), 200)


@app.get("/doctors")
def get_doctors():
    doctors = Doctor.query.all()
    data = [doctor.to_dict(rules=("-appointment_list",)) for doctor in doctors]
    return make_response(jsonify(data), 200)


@app.get("/doctors/<int:id>")
def get_doctor_by_id(id):
    doctor = Doctor.query.filter(Doctor.id == id).first()
    if not doctor:
        make_response(jsonify({"error": "that is a quack"}), 404)
    doctor_dict = doctor.to_dict()
    return make_response(jsonify(doctor_dict), 200)

@app.get('/patients')
def get_patients():
    patients = Patient.query.all()
    data = [p.to_dict(rules=('-appointment_list',)) for p in patients]
    return make_response(jsonify(data, 200))


@app.get("/patients/<int:id>")
def get_patient_by_id(id):
    patient = db.session.get(Patient, id)
    doctors = [d.to_dict(rules=("-appointment_list",)) for d in patient.doctors]
    patient_dict = patient.to_dict(rules=("-appointment_list",))
    patient_dict["doctors"] = doctors
    return make_response(jsonify(patient_dict), 200)


@app.post("/doctors")
def post_doctor():
    data = request.get_json()

    try:
        doc = Doctor(name=data["name"], specialty=data["specialty"])
        db.session.add(doc)
        db.session.commit()
        return make_response(jsonify(doc.to_dict()), 201)
    except ValueError:
        return make_response(jsonify({"error": "that's a quack!"}), 405)
    
@app.post('/patients')
def post_patient():
    data = request.json
    
    try:
        patient = Patient(name=data['name'])
        db.session.add(patient)
        db.session.commit()
        return make_response(jsonify(patient.to_dict()), 201)
    except ValueError:
        return make_response(jsonify({'error': 'Yoo aa Wong!'}))


@app.patch("/patients/<int:id>")
def patch_patients(id):
    data = request.get_json()
    patient = Patient.query.filter(Patient.id == id).first()
    if not patient:
        return make_response(jsonify({"error": "no such patient"}), 404)
    try:
        for key in data:
            setattr(patient, key, data[key])
        db.session.add(patient)
        db.session.commit()
        return make_response(jsonify(patient.to_dict()), 201)
    except:
        return make_response(jsonify({"error": "could not update patient"}), 405)
    
@app.patch('/doctors/<int:id>')
def patch_doctors(id):
    data = request.json
    doctor = db.session.get(Doctor, id)
    
    if not doctor:
        return make_response(jsonify({"error": "no doctor"}), 404)
    
    try:
        for key in data:
            setattr(doctor, key, data[key])
        db.session.add(doctor)
        db.session.commit()
        return make_response(jsonify(doctor.to_dict()), 201)
    except:
        return make_response(jsonify({"error": "Shumting wong, could not update"}), 405)
    
@app.patch('/appointments/<int:id>')
def patch_appointment(id):
    data = request.json
    appointment = db.session.get(Appointment, id)
    
    if not appointment:
        return make_response(jsonify({"error": "no appointment"}), 404)
    try:
        for key in data:
            setattr(appointment, key, data[key])
        db.session.add(appointment)
        db.session.commit()
        return make_response(jsonify(appointment.to_dict()), 201)
    except:
        return make_response(jsonify({"error": "Shumting wong, could not update"}), 405)

@app.post("/appointments")
def post_appointment():
    data = request.json
    try:
        appointment = Appointment(
            patient_id=data.get("patient_id"),
            doctor_id=data.get("doctor_id"),
            day=data.get("day"),
        )
        db.session.add(appointment)
        db.session.commit()
        return make_response(
            jsonify(appointment.to_dict(rules=("-patient_id", "-doctor_id"))), 201
        )
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 405)
    
@app.delete('/appointments')
def delete_appointment(id:int):
    appointment = db.session.get(Appointment, id)
    if not appointment:
        return make_response(jsonify({"error": 'Shumting Wong - no appointment'}), 404)
    db.session.delete(appointment)
    db.session.commit()
    return make_response(jsonify({}), 204)

@app.delete('/doctors')
def delete_doctor(id:int):
    doctor = Doctor.query.filter(Doctor.id == id).first()
    
    if not doctor:
        return make_response(jsonify({"error": 'Shumting Wong - no appointment'}), 404)
    
    db.session.delete(doctor)
    db.session.commit()
    return make_response(jsonify({}), 204)

@app.delete('/patients')
def delete_patient(id:int):
    patient = db.session.get(Patient, id)
    
    if not patient:
        return make_response(jsonify({"error": 'Shumting wong, no patient'}), 404)
    
    db.session.delete(patient)
    db.session.commit()
    return make_response(jsonify({}), 204)

if __name__ == "__main__":
    app.run(port=5555, debug=True)