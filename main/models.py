from django.db import models

# user login 

class User(models.Model):
    user_Id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password_hash = models.TextField()
    role = models.TextField(default="user")

    class Meta:
        db_table = "User"



# staff profile data

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    
    class Meta:
        db_table = "Staff"


class Team(models.Model):
    team_id = models.AutoField(primary_key=True)

    team_name = models.CharField(max_length=100)
    date_created = models.DateField()
    team_mission = models.TextField(blank=True, null=True)
    team_description = models.TextField(blank=True, null=True)

    team_status = models.CharField(max_length=30)

    department = models.ForeignKey(
        "Department",
        on_delete=models.CASCADE, db_column="department_id"
    )

    class Meta:
        db_table = "Team"

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100)
    department_head = models.CharField(max_length=100)
    department_description = models.TextField(null=True, blank=True)  

    class Meta:
        db_table = "Department"
        
class Message(models.Model):
    # Uses their custom User model instead of Django's built-in one
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        db_column='sender_id'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages',
        db_column='receiver_id'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = "Message"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.sender.email} → {self.receiver.email}: {self.content[:40]}"
