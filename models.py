from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
import string, datetime
from datetime import datetime
import re


metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)
db = SQLAlchemy(metadata=metadata)


class Patient(db.Model, SerializerMixin):
    __tablename__ = "patient_table"

    serialize_rules = ('-appointment_list.patient',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    appointments_list = db.relationship('Appointment', back_populates='patient')

class Appointment(db.Model, SerializerMixin):
    __tablename__ = "appointment_table"

    serailize_rules = ('-patient.appointment_list', '-doctor.appointment_list')

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String, nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor_table.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient_table.id'), nullable=False)

    patient = db.relationship('Patient', back_populates='appointment_list')
    doctor = db.relationship('Doctor', back_populates='appointment_list')

    @validates('day')
    def validate_day(self, key: str, value: str):
        day_open = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        if value not in day_open:
            raise ValueError('Shumting Wong')
        return value



class Doctor(db.Model, SerializerMixin):
    __tablename__ = "doctor_table"

    serialize_rules = ('-appointment_list.doctor',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    speciality = db.Column(db.String, nullable=False)

    appointments_list = db.relationship('Appointment', back_populates='doctor')

    @validates('name')
    def validate_name(self, key: str, value: str):
        if value.startswith('Dr.'):
            
            length = value[3:]

            if len(length) >=1:
                return value

        raise ValueError('Shumting Wong')
        
