from sqlalchemy import create_engine, Column, Integer, String , Float, ForeignKey, func
from sqlalchemy.orm import sessionmaker,declarative_base, relationship
import pandas as pd

engine = create_engine("postgresql+psycopg://saksham@localhost:5432/fastapi_db",echo=True)

Session = sessionmaker(bind=engine)
 # session = Session(engine) is also correct but this is the recommended way to create a session

session = Session() # this is used to create a session which is used to interact with the database. It is used to add, update, delete and query the data in the database.

#why is ORM used?
#ORM is used to map the database tables to python classes and objects. 
# It allows us to interact with the database using python objects instead of writing raw SQL queries. 
# It provides a higher level of abstraction and makes it easier to work with the database. 
# It also helps in maintaining the code and makes it more readable. 
# It also provides features like lazy loading, caching, and relationship management.

# meta = MetaData() # this is used to create a metadata object which is used to store the information about the database tables and their columns. It is used to create the tables in the database.

Base = declarative_base() # this is used to create a Base class which is used to create the tables in the database. It is used to create the tables in the database.

#in ORMs we depict tables through classes and columns through attributes of the class.

class Student(Base):
    __tablename__ = "students" 
    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False) 
    gender = Column(String,nullable=False)
    gpa = Column(Float, nullable=False) 

    subjects = relationship("Subject", back_populates="students",cascade="all, delete-orphan")


class Subject(Base):
    __tablename__ = "subjects" 
    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String, nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)

    students = relationship("Student", back_populates="subjects")


Base.metadata.create_all(engine)

# new_person = Student(name="Shourya", age=18, gpa=8.7)
# session.add(new_person)
# session.flush()
#this is used to flush the changes to the database without committing them. It is used to get the id of the newly added person.
#but even if u commit the changes to the database, the id of the newly added person will be available in the new_person object. So, flush is not necessary here. why not necesary? because the id of the newly added person will be available in the new_person object even if we commit the changes to the database. So, flush is not necessary here. where it is necessary? flush is necessary when we want to get the id of the newly added person before committing the changes to the database. For example, if we want to add a subject for the newly added person, we need to get the id of the newly added person before committing the changes to the database. So, flush is necessary here.

# new_subject = Subject(name="Chemistry",student_id=new_person.id)
# session.add(new_subject)
# session.commit()

# print(new_person.subjects[0].name)
# print(new_subject.students.name)

result = session.query(Student.id,Student.name,Student.age).all()
#seession.query() is used to print rows in tuples


#select becomes query
#where become filter

# result_D = session.query(Student).filter(Student.age <= 18).delete()
# session.commit() 
# result = session.query(Student).filter(Student.age <= 18).all()

# for rows in result:
#     print(rows.name)

# result_U = session.query(Student).filter(Student.age <= 18).update({'name' : 'new_thing'})

# result = session.query(Student.name,Subject.name).join(Subject).all()


result_group_by = session.query(Student.age,func.avg(Student.gpa)).group_by(Student.age).all()
session.commit()
session.close()

df = pd.read_sql("SELECT * FROM students", con = engine)
print(df)



