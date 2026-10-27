from sqlalchemy import create_engine,MetaData,Table,Column,Integer,String, ForeignKey,Join,text,func
from sqlalchemy.orm import Session

engine = create_engine("postgresql+psycopg://saksham@localhost:5432/fastapi_db",echo=True)

# #engine to create / connection between the databse and python file
# #echo just tells what happens after every command 

# conn = engine.connect()

# conn.execute(text("CREATE TABLE python_table (name VARCHAR(50),age INT,gender VARCHAR(20))"))

# conn.commit()

# session = Session(engine)

# session.execute(text("INSERT INTO python_table(name,age,gender) VALUES('saksham',18,'M')"))

# session.commit()
# rows = session.execute(text("SELECT * FROM python_table")).all()
# print(rows)

# all this was by using raw sql commands and everything if u we wann ause sqlalchemy we use metadata and ORMS

meta = MetaData()
conn = engine.connect()

people = Table(
    "people",
    meta,
    Column('id',Integer,primary_key=True),
    Column('name',String,nullable=False),
    Column('age',Integer)
)
things = Table(
    "things",
    meta,
    Column('t_id',Integer,primary_key=True),
    Column('object',String,nullable=False),
    Column('owner',Integer,ForeignKey('people.id'))
)

# CREATE TABLE people (
#         id SERIAL NOT NULL, 
#         name VARCHAR NOT NULL, 
#         age INTEGER, 
#         PRIMARY KEY (id)
# )
#code create by the meta data
# insert = people.insert().values(id = 2,name = "vedanshi",age = 19)
# # insert_cmmd = insert(people).values() .... another way of inserting
# conn.execute(insert)
# conn.commit()

# select = people.select().where(...)
# result = conn.execute(select)
# conn.commit()

# for r in result:
#     print(r)

# update = people.update().where(people.c.name == "saksham").values(name = "saxam",age = 18)
# result = conn.execute(update)
# conn.commit()

# select = people.select()
# result = conn.execute(select)
# conn.commit()

# for r in result:
#     print(r)

# delete = people.delete()
# result = conn.execute(delete)
# conn.commit()

# result = conn.execute(people.select())
# conn.commit()

# for r in result:
#     print(r)

meta.create_all(engine) #use to create all  

insert_1 = people.insert().values([

    {'id' : 1, "name" : "Saksham", "age" : 18},
    {'id' : 2, "name" : "Vedanshi", "age" : 19},
    {'id' : 3, "name" : "Rishit", "age" : 19},
    {'id' : 4, "name" : "Saumya", "age" : 18}

])

insert_2 = things.insert().values([

    {"t_id" : 5, "object" : "laptop","owner" : 1},
    {"t_id" : 9, "object" : "mouse","owner" : 2},
    {"t_id" : 8, "object" : "apple","owner" : 3},
    {"t_id" : 6, "object" : "books","owner" : 4}

])

# conn.execute(insert_1)
# conn.execute(insert_2)
# conn.commit()

# #we can perform joins on tables
# # Person ID 5 has no items in 'things'
# conn.execute(text("INSERT INTO people VALUES (8, 'Rahul', 22)"))
# # 'car' has owner ID 99 (which doesn't exist in 'people')
# conn.execute(text("INSERT INTO things VALUES (10, 'car')"))
# conn.commit()

# join = things.join(people,people.c.id == things.c.owner, full=True) #isouter = True means outer join and False means inner join

# select = people.select().with_only_columns(people.c.id,people.c.name,things.c.object,things.c.owner).select_from(join)
# result = conn.execute(select)
# conn.commit()

# print("\n--- JOIN RESULT ---")
# for row in result:
#     print(row)



#full outer join (full = True) means it will return all the rows from both tables and if there is no match it will return null values
#inner join normal then add nothing
#if left join then add isouter = True and 
#if right join then add isouter = True and change the order of tables in join


#GROUP AND AGGEGATE FUNCTIONS

# Total sum of all ages (without grouping)
group = people.select().with_only_columns(people.c.age,func.sum(people.c.age)).group_by(people.c.age).having(func.sum(people.c.age) > 36)
result1 = conn.execute(group)
conn.commit()

print("\n--- TOTAL SUM OF GROUP AGES ---")
print(result1.all())

total_sum = people.select().with_only_columns(func.sum(people.c.age))
result2 = conn.execute(total_sum)
conn.commit()

print("\n--- TOTAL SUM OF AGES ---")
print(result2.all())