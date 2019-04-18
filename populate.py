import os
os.environ['DJANGO_SETTINGS_MODULE']='vKarma.settings'
import django
django.setup()
from classroom.models import *
from faker import Faker
import random
from passlib.hash import pbkdf2_sha256, django_pbkdf2_sha256
from passlib.utils import to_bytes, to_native_str
import base64
import datetime

 # PASSWORD is kvrox113
# PASSWORD = 'password'
# ROUND = 120000
# SALT = to_bytes('google')
# hash0 = pbkdf2_sha256.using(salt=SALT,rounds=ROUND).hash(PASSWORD)
# print(hash0) 
hash0 = 'pbkdf2_sha256$120000$fOLZy0sSU8XG$JwG4JaSXADYIxTj65bjkFwSup0hnet5FGjqxShuhVKA='
# $pbkdf2-sha256$20000$Z29vZ2xl$PtFLyZHJJucUa2KBg1iJeVJsivis8JimRhFifRRKlFc

fake = Faker('it_IT')


print('creating even amount of users to be distributed over 2 schools ...')
def create_data(n_admins=2,n_students=20,n_teachers=4,n_parents=20):
	n = n_admins + n_students + n_teachers + n_parents
	firstNames = [fake.first_name() for _ in range(n)]
	lastNames = [fake.last_name() for _ in range(n)]
	Subjects = ['Mathematics','Physics','Computer Science','Biology','Chemistry','English']
	Colors = ['#00c2ff','#ff99ff','#f2300d','#7dff7d','#b2668c','#ff0066']
	batches = ['Alpha','Beta','Gamma','Delta',
				'Epsilon','Zeta','Eta','Theta']
	schools= ['Bhartiya Vidyapeeth School','Cambridge School Indirapuram']
	school = [''.join([ i[0] for i in school.split(' ')]) for school in schools ]
	Batches = [Batch.objects.create(name=batch,school=school[0]) for batch in batches[:4]] + [Batch.objects.create(name=batch,school=school[1]) for batch in batches[4:]]
	child = []
	email = [ fake.email() for _ in range(n) ]
	phone_number = [fake.phone_number() for _ in range(n)]
	dob = [fake.simple_profile(sex=None)['birthdate'] for _ in range(n)]
	address = [fake.simple_profile(sex=None)['address'] for _ in range(n)]
	age = [random.randint(6,18) for _ in range(n_students)]
	usernames = []


	for i in range(1,n_students+1):
		roll_no = '0'*(4 - len(str(i))) + str(i)
		if(i < n_students/2 + 1):
			usernames.append('VK'+ school[0] + 'S' + roll_no)
		else:
			usernames.append('VK'+ school[1] + 'S' + roll_no)

	for i in range(n_students+1,n_students + n_teachers +1):
		roll_no = '0'*(4 - len(str(i))) + str(i)
		if(i < (n_teachers)/2 + 1 + n_students):
			usernames.append('VK'+ school[0] + 'T' + roll_no)
		else:
			usernames.append('VK'+ school[1] + 'T' + roll_no)

	for i in range(n_students + n_teachers +1,n_students + n_teachers +1 + n_parents):
		roll_no = '0'*(4 - len(str(i))) + str(i)
		if(i < (n_parents)/2 + 1 + n_students + n_teachers):
			usernames.append('VK'+ school[0] + 'P' + roll_no)
		else:
			usernames.append('VK'+ school[1] + 'P' + roll_no)  
		

# CREATION OF STUDENTS


	users = [User.objects.create(firstName=firstNames[i],
							lastName=lastNames[i],
							is_student=True,
							school=school[0],
							username=usernames[i],
							password=hash0) for i in range(n_students//2)] + [User.objects.create(firstName=firstNames[i],
							lastName=lastNames[i],
							is_student=True,
							school=school[1],
							username=usernames[i],
							password=hash0) for i in range(n_students//2,n_students)]
	print("The following users have been created")
	for user in users:
		print("UserType : Student | Username : {} | password : kvrox113".format(user.username))
	for i in range(n_students):
		if(i < n_students):
			child.append(Student.objects.create(user=users[i],
				batch=random.sample(Batches[:4],1)[0],
				email=email[i],
				phone_number=phone_number[i],
				dob=dob[i],
				address=address[i],
				age=age[i]))
		if(i >= n_students):
			child.append(Student.objects.create(user=users[i],
				batch=random.sample(Batches[4:],1)[0],
				email=email[i],
				phone_number=phone_number[i],
				dob=dob[i],
				address=address[i],
				age=age[i]))

# CREATION OF TEACHERS
	users = [User.objects.create(firstName=firstNames[i],
							lastName=lastNames[i],
							is_teacher=True,
							school=school[0],
							username=usernames[i],
							password=hash0) for i in range(n_students,n_teachers//2 + n_students)] + [User.objects.create(firstName=firstNames[i],
							lastName=lastNames[i],
							is_teacher=True,
							school=school[1],
							username=usernames[i],
							password=hash0) for i in range(n_teachers//2 + n_students,n_teachers + n_students)]
	for user in users:
		print("UserType : Teacher | Username : {} | password : kvrox113".format(user.username))
	for i in range(n_students,n_students+n_teachers):
		teacher = Teacher.objects.create(
			user=users[i - n_students],
			email=email[i],
			phone_number=phone_number[i]
			)
		if(teacher.user.school == school[0]):
			teacher.batch.set(random.sample(Batches[:4],3))
		elif(teacher.user.school == school[1]):
			teacher.batch.set(random.sample(Batches[4:],3))

# CREATION OF PARENTS
	

	users = [User.objects.create(firstName=firstNames[i],
							lastName=lastNames[i],
							is_parent=True,
							school=school[0],
							username=usernames[i],
							password=hash0) for i in range(n_teachers + n_students,n_teachers + n_students + n_parents//2)] + [User.objects.create(firstName=firstNames[i],
							lastName=lastNames[i],
							is_parent=True,
							school=school[1],
							username=usernames[i],
							password=hash0) for i in range(n_teachers + n_students + n_parents//2,n_teachers + n_students + n_parents)]

	for user in users:
		print("UserType : Parent | Username : {} | password : kvrox113".format(user.username))
	for i in range(n_students+n_teachers,n_students+n_teachers + n_parents):
		Parent.objects.create(
			user=users[i - n_students-n_teachers],
			child=child[i-n_students-n_teachers],
			email=email[i],
			phone_number=phone_number[i],
			address=address[i]
			)
	admins = []
	admins.append(User.objects.create(firstName=fake.first_name(),
							lastName=fake.last_name(),
							is_admin=True,
							school=school[0],
							password=hash0,
							username="keshav_admin1"))
	Admin.objects.create(user=admins[0])

	admins.append(User.objects.create(firstName=fake.first_name(),
							lastName=fake.last_name(),
							is_admin=True,
							school=school[1],
							password=hash0,
							username="keshav_admin2"))
	Admin.objects.create(user=admins[1])
	for admin in admins:
		print('Admins created : username : {} | password : kvrox113 | school : {}'.format(admin.username,admin.school))
	
	for _ in range(5):
		Notification.objects.create(school=school[0],
									issue_date=datetime.datetime.now().strftime("%Y-%m-%d"),
									owner = admins[0],
									name = fake.street_name(),
									description = fake.text())

	for _ in range(5):
		Notification.objects.create(school=school[1],
									issue_date=datetime.datetime.now().strftime("%Y-%m-%d"),
									owner = admins[1],
									name = fake.street_name(),
									description = fake.text())

	print("Notifications created ! 5 for each school")
	for name,color in zip(Subjects,Colors):
		Subject.objects.create(name=name,color=color,school=school[0])
	for name,color in zip(Subjects,Colors):
		Subject.objects.create(name=name,color=color,school=school[1])
	print("Subjects created, same for each schools : {}".format(','.join(Subjects)))
create_data()