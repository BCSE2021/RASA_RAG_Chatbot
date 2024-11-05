# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
import re
import requests
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.ext.declarative import declarative_base
#from db import connection
from .models import Users, Course, Class, Registration
import datetime
import os
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
class ActionCheckDBConnection(Action):
    def name(self):
        return "action_check_db_connection"

    def run(self, dispatcher, tracker, domain):
        try:
            connection = engine.connect()
            dispatcher.utter_message("Kết nối thành công!")
            connection.close()
        except Exception as e:
            dispatcher.utter_message(f"Kết nối thất bại: {e}")

        return []
    
class GetInfo(Action):
    def name(self) -> str:
        return "action_provide_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        student = session.query(Users).filter_by(student_id=21110087).first()

        if student:
            message = f"Sinh viên {student.student_id} được đăng ký vào lúc {student.created_at}."
        else:
            message = f"Không tìm thấy sinh viên với mã số."
        dispatcher.utter_message(text=message)
        return []

class ValidateStudentID(Action):
    def name(self) -> str:
        return "action_validate_student_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        student_id = next(tracker.get_latest_entity_values("student_id"), None)

        student_id_validate = session.query(Users).filter_by(student_id = student_id)

        if student_id_validate and re.fullmatch(r"\d{8}", student_id):

            dispatcher.utter_message(text=f"Mã sinh viên bạn đang sử dụng để đăng ký là {student_id}.\n Hãy nhập mã môn học bạn đang muốn đăng ký")
            
            return [SlotSet("id_student", student_id)]
        else:
            dispatcher.utter_message(text="Mã sinh viên không hợp lệ hoặc không có . Vui lòng nhập lại mã sinh viên của bạn gồm 8 chữ số.")
            return [SlotSet("id_student", None)]
        

class ValidateSubjectID(Action):
    def name(self) -> str:
        return "action_validate_subject_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        subject_id = next(tracker.get_latest_entity_values("subject_id"), None)
        course_id_validate = session.query(Course).filter_by(id = subject_id)

        if course_id_validate and re.fullmatch(r"[a-zA-Z]{3}\d{4}", subject_id):
            dispatcher.utter_message(text=f"Mã môn học bạn đang đăng ký là {subject_id}.")
            return [SlotSet("subject_id", subject_id)]
        else:
            dispatcher.utter_message(text="Mã môn học không hợp lệ hoặc hiện chưa mở. Mời nhập mã môn học khác.")
            return [SlotSet("subject_id", None)]


class ValidateClassID(Action):
    def name(self) -> str:
        return "action_validate_subject_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        subject_id = next(tracker.get_latest_entity_values("subject_id"), None)
        class_id = next(tracker.get_latest_entity_values("class_id"), None)

        class_id_validate = session.query(Class).filter_by(id=class_id, subject_id=subject_id)

        if class_id_validate and re.fullmatch(r"[a-zA-Z]{2}\d{2}", class_id):
            dispatcher.utter_message(text=f"Mã môn học bạn đang đăng ký là {class_id}.")

            return [SlotSet("class_id", class_id)]
        else:
            dispatcher.utter_message(text="Mã môn học không hợp lệ hoặc hiện chưa mở. Mời nhập mã môn học khác.")
            return [SlotSet("class_id", None)]

class RegistrationCourse(Action):
    def name(self) -> str:
        return "registration_course"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        class_ = session.query(Class).filter_by()


class Validate(FormValidationAction):
    def name(self) -> str:
        return "validate_registration_form"

    def validate_id_student(self,slot_value: Any, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if len(slot_value) == 8:
            dispatcher.utter_message(text=f"Mã sinh viên bạn đang sử dụng để đăng ký là {slot_value}.")
            student_id_validate = session.query(Users).filter_by(student_id=slot_value).first()
            if student_id_validate:
                dispatcher.utter_message(text=" Hãy nhập mã học phần mà bạn muốn đăng ký.")
                return {"id_student": slot_value}
            else: 
                dispatcher.utter_message(text="Mã sinh viên của bạn không tồn tại. Vui lòng nhập lại mã sinh viên")
                return {"id_student", None}
        else:
            dispatcher.utter_message(text="Mã sinh viên không hợp lệ . Vui lòng nhập lại mã sinh viên gồm 8 chữ số.")
            return {"id_student", None}
        

    # def validate_id_subject(self, slot_value: Any, dispatcher: CollectingDispatcher,
    #         tracker: Tracker,
    #         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    #     #if not student_id_validate or not re.fullmatch(r"\d{8}", student_id):
    #     if slot_value and re.fullmatch(r"[a-zA-Z]{3}\d{3}", slot_value):
    #         dispatcher.utter_message(text=f"Mã môn học bạn đang đăng ký là {slot_value}.")
    #         course_id_validate = session.query(Course).filter_by(id=slot_value).first()
    #         if course_id_validate:
    #             dispatcher.utter_message(text=" Hãy nhập mã lớp của học phần mà bạn muốn đăng ký.")
    #             return {"id_subject": slot_value}
    #         else: 
    #             dispatcher.utter_message(text="Mã học phần của bạn không tồn tại. Vui lòng nhập lại mã học phần")
    #             return {"id_subject", None}
    #     else:
    #         dispatcher.utter_message(text="Mã môn học không hợp lệ. Vui lòng nhập mã môn học khác.")
    #         return {"id_subject", None}
    
    # testing
    def validate_id_subject(self, slot_value: Any, dispatcher: CollectingDispatcher,
                        tracker: Tracker,
                        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        student_id = tracker.get_slot('id_student') 

        if slot_value and re.fullmatch(r"[a-zA-Z]{3}\d{3}", slot_value):
            dispatcher.utter_message(text=f"Mã môn học bạn đang đăng ký là {slot_value}.")

            query = f"""SELECT r.student_id, c.subject_id, co.id FROM registrations r JOIN classes c ON r.class_id = c.id JOIN courses co ON c.subject_id = co.id WHERE r.student_id = :student_id AND co.id = :course_id"""
            result = session.execute(query, {'student_id': student_id, 'course_id': slot_value}).fetchone()
            print(result)
            if result:
                dispatcher.utter_message(text="Bạn đã đăng ký môn học này.")
                return {"id_subject": None}
        
            else:
                dispatcher.utter_message(text="Hãy nhập mã lớp của học phần mà bạn muốn đăng ký.")
                return {"id_subject": slot_value}
        else:
            dispatcher.utter_message(text="Mã môn học không hợp lệ. Vui lòng nhập mã môn học khác.")
            return {"id_subject": None}
    
    def validate_id_class(self, slot_value: Any, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        subject_id = tracker.get_slot("id_subject")
        if slot_value and re.fullmatch(r"[a-zA-Z]{2}\d{2}", slot_value):
            dispatcher.utter_message(text=f"Lớp học bạn đang đăng ký là {slot_value}.")
            class_id_validate = session.query(Class).filter_by(id=slot_value, subject_id=subject_id).first()
            if class_id_validate: 
                return {"id_class": slot_value}
            else: 
                dispatcher.utter_message(text="Mã lớp của bạn không tồn tại. Vui lòng nhập lại mã lớp")
                return {"id_class", None}
        else:
            dispatcher.utter_message(text="Mã lớp học không hợp lệ. Vui lòng nhập mã lớp học khác.")
            return {"id_class", None}
    # def validate_confirmations(self, slot_value: Any, dispatcher: CollectingDispatcher,
    #         tracker: Tracker,
    #         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
    #     confirmation = tracker.latest_message['intent'].get('name')
    #     dispatcher.utter_message(text="Hãy xác nhận lại thông tin của bạn.")
    #     if confirmation == "affirm":
    #         dispatcher.utter_message(text="Thông tin đã được xác nhận.")
    #         return {"confirmatios": confirmation}
    #     elif confirmation == "deny":
    #         dispatcher.utter_message(text="Vui lòng nhập lại thông tin.")
    #         return {"confirmatios": None}


class Registration(Action):
    def name(self) -> str:
        return "action_registration_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        student_id = tracker.get_slot("id_student")
        class_id = tracker.get_slot("id_class")
        class_data = session.query(Class.current_slots, Class.max_slots).filter_by(id=class_id).first()
        class_id_validate = session.query(Class).filter_by(id=class_id).first()
        print(f"class_id_validate: {class_id_validate}")
        if class_data:
            current_slots, max_slots = class_data
            if current_slots < max_slots:
                insert_query = """ INSERT INTO registrations (student_id, class_id, registered_at) VALUES (:student_id, :class_id, :registered_at) """
                update_query = """ UPDATE classes SET current_slots = current_slots + 1 WHERE id = :class_id """

                session.execute(insert_query, {
                    'student_id': student_id,
                    'class_id': class_id,
                    'registered_at': datetime.datetime.utcnow()
                })

                session.execute(update_query, {
                    'class_id': class_id
                })

                session.commit()
                dispatcher.utter_message(text="Bạn đã đăng ký thành công lớp học.")
            else:
                dispatcher.utter_message(text="Lớp học này đã đầy. Vui lòng chọn lớp khác.")
        else: dispatcher.utter_message(text="Không có giá trị")


class ActionDefaultFallback(Action):
    def name(self) -> str:
        return "action_query_rag"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_message = tracker.latest_message.get('text')
        try:
            response = requests.post(
                "http://127.0.0.1:8000/generative_ai", 
                json={"question": user_message}
            )
            
            if response.status_code == 200:
                rag_answer = response.json().get("answer", "Sorry, I couldn't find an answer.")
                dispatcher.utter_message(text=rag_answer)
            else:
                dispatcher.utter_message(text="Sorry, I couldn't reach the answer service.")
        except Exception as e:
            dispatcher.utter_message(text=f"An error occurred: {e}")
        
        return []