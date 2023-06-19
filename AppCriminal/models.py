from django.db import models


class Admin_Details(models.Model):
    Username = models.CharField(default=None,max_length=100)
    Password = models.CharField(default=None,max_length=100)
    
    class Meta:
        db_table = 'Admin_Details'  



class Officer_details(models.Model):
    FirstName = models.CharField(default=None,max_length=100)
    LastName = models.CharField(default=None,max_length=100)
    Username = models.CharField(default=None,max_length=100)
    Email = models.CharField(default=None,max_length=100)
    Password = models.CharField(default=None,max_length=100)
    mobile = models.CharField(default=None,max_length=100)
    Address = models.CharField(default=None,max_length=100)
    City = models.CharField(default=None,max_length=100)
    State = models.CharField(default=None,max_length=100)
    Image = models.ImageField(upload_to='img/images')
    
    class Meta:
        db_table = 'Officer_details' 



class Suspects_details(models.Model):
    CaseID = models.CharField(default=None,max_length=100)
    Name = models.CharField(default=None,max_length=100)
    Email = models.CharField(default=None,max_length=100)
    mobile = models.CharField(default=None,max_length=100)
    Address = models.CharField(default=None,max_length=100)
    Relation = models.CharField(default=None,max_length=100)
    Date = models.DateField()
    Rank = models.CharField(default=None,max_length=100)
    Image = models.ImageField(upload_to='img/images')
    Note = models.CharField(default=None,max_length=100)
    OfficerID = models.CharField(default=None,max_length=100)
    
    class Meta:
        db_table = 'Suspects_details' 


class Case_details(models.Model):
    CaseID = models.CharField(default=None,max_length=100)
    OfficerID = models.CharField(default=None,max_length=100)
    CaseType = models.CharField(default=None,max_length=100)
    Name = models.CharField(default=None,max_length=100)
    Note = models.CharField(default=None,max_length=100)
    Status = models.CharField(default=None,max_length=100)
    GuiltyID = models.CharField(default=None,max_length=100)
    GuiltyRelation = models.CharField(default=None,max_length=100)
    
    class Meta:
        db_table = 'Case_details' 


class Evidence_Details(models.Model):
    CaseID = models.CharField(default=None,max_length=100)
    Evidence = models.CharField(default=None,max_length=100)
    Type = models.CharField(default=None,max_length=100)
    Suspects = models.CharField(default=None,max_length=100)
    Image = models.ImageField(upload_to='img/images')
    Note = models.CharField(default=None,max_length=100)
    Rank = models.CharField(default=None,max_length=100)
    Date = models.DateField()
    OfficerID = models.CharField(default=None,max_length=100)
    
    class Meta:
        db_table = 'Evidence_Details' 


class CaseHistory(models.Model):
    CaseID = models.CharField(default=None,max_length=100)
    History = models.CharField(default=None,max_length=300)
    Date = models.DateField()
    OfficerID = models.CharField(default=None,max_length=100)
    
    
    class Meta:
        db_table = 'CaseHistory' 