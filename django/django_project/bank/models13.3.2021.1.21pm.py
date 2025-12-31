from __future__ import unicode_literals
from django import forms
from django.db import models

import datetime
from django.forms import TextInput, Textarea
from django.utils import timezone
from .forms import FaqForm
from datetime import datetime as dt




# Create your models here.

class current_affairs_slide(models.Model):

    upper_heading = models.CharField(max_length=50)
    yellow_heading = models.CharField(max_length=50)
    key_1= models.CharField(max_length=50)
    key_2 = models.CharField(max_length=50)
    key_3 = models.CharField(max_length=50)
    key_4 = models.CharField(max_length=50,null=True,blank=True)
    day = models.DateField(default=datetime.date.today)
    
    creation_time= models.TimeField(blank=True, null=True)

    
   
    
    ca_image = models.FileField(upload_to='current_affairs/%Y/%m/%d')
    def __str__(self):
        return self.day.strftime('%d/%m/%Y') + '     '+ self.upper_heading




class current_affairs(models.Model):
    s= (
    ("2018", "2018"),   
    ("2019", "2019"),
    ("2020", "2020"),
    )
    year_now = models.CharField(max_length=10,
                          choices=s,
                          default="2050",blank=True,null=True,db_index=True)
    month_ch= (
    ("January", "January"),   
    ("February", "February"),
    ("March", "March"),
    ("April", "April"),
    ("May", "May"),
    ("June", "June"),
    ("July", "July"),
    ("August", "August"),   
    ("September", "September"),
    ("October", "October"),
    ("November", "November"),
    ("December", "December"),
    
    )
    month = models.CharField(max_length=15,
                  choices=month_ch,
                  default="December",blank=True,null=True,db_index=True)
    day = models.DateField(default=datetime.date.today,db_index=True)
    creation_time= models.TimeField(blank=True, null=True)
    upper_heading = models.CharField(max_length=250)
    yellow_heading = models.CharField(max_length=250)
    key_1= models.CharField(max_length=200)
    key_2 = models.CharField(max_length=200)
    key_3 = models.CharField(max_length=200)
    key_4 = models.CharField(max_length=200,null=True,blank=True)
    
    paragraph=models.TextField(default='',blank=True,null=True)
    all_key_points=models.TextField(default='',blank=True,null=True)
    link=models.TextField(default='',blank=True,null=True)
    url=models.TextField(default='',blank=True,null=True)
    Science_Techonlogy = models.BooleanField(default=False,db_index=True)
    
    National = models.BooleanField(default=False,db_index=True)
    
    State=models.BooleanField(default=False,db_index=True)
    
    International =models.BooleanField(default=False,db_index=True)
    
    Business_Economy_Banking  =models.BooleanField(default=False,db_index=True)
    
    Environment =models.BooleanField(default=False,db_index=True)
    
    Defence =models.BooleanField(default=False,db_index=True)
    
    Persons_in_News =models.BooleanField(default=False,db_index=True)
    
    Awards_Honours =models.BooleanField(default=False,db_index=True)
    
    Sports =models.BooleanField(default=False,db_index=True)
    
    Art_Culture =models.BooleanField(default=False,db_index=True)
    
    Government_Schemes =models.BooleanField(default=False)
    rank =models.BooleanField(default=False)
    obituary =models.BooleanField(default=False)
    appointment  =models.BooleanField(default=False)
    static_gk =models.BooleanField(default=False)
    ca_img = models.FileField(upload_to='ca/%Y/%m/%d')
    new_id=models.CharField(max_length=300,default='',blank=True,null=True,db_index=True)
    

    class Meta:
        ordering = ["-day"]

        
   
    
    
    def __str__(self):
        return self.day.strftime('%d/%m/%Y') + '     '+ self.upper_heading

    def save(self):
        self.new_id= self.upper_heading +'===' +self.day.strftime('%d-%m-%Y')
        super(current_affairs, self).save()




      

class total(models.Model):
    
    total_current_affairs = models.IntegerField (db_index=True,default=3)
    total_current_affairs_page = models.IntegerField (db_index=True,default=3)
    
    Science_Techonlogy=models.IntegerField (db_index=True,default=0)
    
    National = models.IntegerField (db_index=True,default=0)
    
    State=models.IntegerField (db_index=True,default=0)
    
    International =models.IntegerField (db_index=True,default=0)
    
    Business_Economy_Banking  =models.IntegerField (db_index=True,default=0)
    
    Environment =models.IntegerField (db_index=True,default=0)
    
    Defence =models.IntegerField (db_index=True,default=0)
    
    Persons_in_News =models.IntegerField (db_index=True,default=0)
    
    Awards_Honours =models.IntegerField (db_index=True,default=0)
    
    Sports =models.IntegerField (db_index=True,default=0)
    
    Art_Culture =models.IntegerField (db_index=True,default=0)
    
    Government_Schemes =models.IntegerField (db_index=True,default=0)
    rank =models.IntegerField (db_index=True,default=0)
    obituary =models.IntegerField (db_index=True,default=0)
    appointment  =models.IntegerField (db_index=True,default=0)
    static_gk =models.IntegerField (db_index=True,default=0)

    
   
    
    


    def save(self):
        totall=current_affairs.objects.count()
        self.total_current_affairs= totall
        self.total_current_affairs_page=int(totall+300)/3

        total_st=current_affairs.objects.filter(Science_Techonlogy=True).count()
        total_n=current_affairs.objects.filter(National=True).count()
        total_State=current_affairs.objects.filter(State=True).count()
        total_International=current_affairs.objects.filter(International=True).count()
        total_Business_Economy_Banking=current_affairs.objects.filter(Business_Economy_Banking=True).count()
        total_Environment=current_affairs.objects.filter(Environment=True).count()
        total_Defence=current_affairs.objects.filter(Defence=True).count()
        total_Persons_in_News=current_affairs.objects.filter(Persons_in_News=True).count()
        total_Awards_Honours=current_affairs.objects.filter(Awards_Honours=True).count()
        total_Sports=current_affairs.objects.filter(Sports=True).count()
        total_Art_Culture=current_affairs.objects.filter(Art_Culture=True).count()
        total_Government_Schemes=current_affairs.objects.filter(Government_Schemes=True).count()
        total_rank=current_affairs.objects.filter(rank=True).count()
        total_appointment=current_affairs.objects.filter(appointment=True).count()
        total_obituary=current_affairs.objects.filter(obituary=True).count()
        total_static_gk=current_affairs.objects.filter(static_gk=True).count()
        if total_st !=0:
            
            if(int(total_st)%3==0):
                total_page_Science_Techonlogy=(int(total_st)/3)
            else:
                total_page_Science_Techonlogy=(int(total_st)/3)+1

            self.Science_Techonlogy= total_page_Science_Techonlogy        

                


        if total_n !=0:
            
            if(int(total_n)%3==0):
                total_page_National=(int(total_n)/3)
            else:
                total_page_National=(int(total_n)/3)+1
            self.National= total_page_National       

        if total_State !=0:
            
            if(int(total_State)%3==0):
                total_page_State=(int(total_State)/3)

            else:
                total_page_State=(int(total_State)/3)+1
            self.State= total_page_State     

        if total_International !=0:
            
            if(int(total_International)%3==0):
                total_page_International=(int(total_International)/3)
            else:
                total_page_International=(int(total_International)/3)+1
            self.International= total_page_International     

        if total_Business_Economy_Banking !=0:
            
            if(int(total_Business_Economy_Banking)%3==0):
                total_page_Business_Economy_Banking=(int(total_Business_Economy_Banking)/3)

            else:
                total_page_Business_Economy_Banking=(int(total_Business_Economy_Banking)/3)+1

            self.Business_Economy_Banking= total_page_Business_Economy_Banking    

        if total_Environment !=0:
            
            if(int(total_Environment)%3==0):
                total_page_Environment=(int(total_Environment)/3)
            else:
                total_page_Environment=(int(total_Environment)/3)+1
            self.Environment= total_page_Environment     

        if total_Defence !=0:
            
            if(int(total_Defence)%3==0):
                total_page_Defence=(int(total_Defence)/3)
            else:
                total_page_Defence=(int(total_Defence)/3)+1

            self.Defence= total_page_Defence     

        if total_Persons_in_News !=0:
            
            if(int(total_Persons_in_News)%3==0):
                total_page_Persons_in_News=(int(total_Persons_in_News)/3)
            else:
                total_page_Persons_in_News=(int(total_Persons_in_News)/3)+1

            self.Persons_in_News= total_page_Persons_in_News     

        if total_Awards_Honours !=0:
            
            if(int(total_Awards_Honours)%3==0):
                total_page_Awards_Honours=(int(total_Awards_Honours)/3)
            else:
                total_page_Awards_Honours=(int(total_Awards_Honours)/3)+1
            self.Awards_Honours= total_page_Awards_Honours    

        if total_Sports !=0:
            
            if(int(total_Sports)%3==0):
                total_page_Sports=(int(total_Sports)/3)
            else:
                total_page_Sports=(int(total_Sports)/3)+1

            self.Sports= total_page_Sports    

        if total_Art_Culture !=0:
            
            if(int(total_Art_Culture)%3==0):
                total_page_Art_Culture=(int(total_Art_Culture)/3)
            else:
                total_page_Art_Culture=(int(total_Art_Culture)/3)+1

            self.Art_Culture= total_page_Art_Culture     

        if total_Government_Schemes !=0:
            
            if(int(total_Government_Schemes)%3==0):
                total_page_Government_Schemes=(int(total_Government_Schemes)/3)
            else:
                total_page_Government_Schemes=(int(total_Government_Schemes)/3)+1
            self.Government_Schemes= total_page_Government_Schemes
        if total_rank !=0:
            
            if(int(total_rank)%3==0):
                total_page_rank=(int(total_rank)/3)
            else:
                total_page_rank=(int(total_rank)/3)+1
            self.rank= total_page_rank

        if total_obituary !=0:
            
            if(int(total_obituary)%3==0):
                total_page_obituary=(int(total_obituary)/3)
            else:
                total_page_obituary=(int(total_obituary)/3)+1
            self.obituary= total_page_obituary

        
        if total_appointment !=0:
            
            if(int(total_appointment)%3==0):
                total_page_appointment=(int(total_appointment)/3)
            else:
                total_page_appointment=(int(total_appointment)/3)+1
            self.appointment= total_page_appointment

        if total_static_gk !=0:
            
            if(int(total_static_gk)%3==0):
                total_page_static_gk=(int(total_static_gk)/3)
            else:
                total_page_static_gk=(int(total_static_gk)/3)+1
            self.static_gk= total_page_static_gk

            
        super(total, self).save()



class the_hindu_word_Header1(models.Model):
    
   
    Heading_for_list1=models.TextField() 
    day = models.DateField(default=datetime.date.today,db_index=True)
    creation_time= models.TimeField(blank=True, null=True)
    link = models.CharField(max_length=450,blank=True,null=True)
    new_id=models.CharField(max_length=300,default='',blank=True,null=True,db_index=True)
    class Meta:
        ordering = ["-day"]

    def __str__(self):
        return self.day.strftime('%d/%m/%Y')+ self.Heading_for_list1[:100]

    def save(self):
        self.new_id= 'the_hindu_header1' +self.day.strftime('%d-%m-%Y')
        super(the_hindu_word_Header1, self).save()


    







class the_hindu_word_Header2(models.Model):
    
   
    Heading_for_list2=models.TextField() 
    day = models.DateField(default=datetime.date.today,db_index=True)
    creation_time= models.TimeField(blank=True, null=True)
    link = models.CharField(max_length=450,blank=True,null=True)
    new_id=models.CharField(max_length=300,default='',blank=True,null=True,db_index=True)
    class Meta:
        ordering = ["-day"]

    def __str__(self):
        return self.day.strftime('%d/%m/%Y')+self.Heading_for_list2[:30]

    def save(self):
        self.new_id= 'the_hindu_header2' +self.day.strftime('%d-%m-%Y')
        super(the_hindu_word_Header2, self).save()       
        
        
class the_hindu_word_list1(models.Model):
    
    word = models.CharField(max_length=150,db_index=True)
    meaning = models.CharField(max_length=650,blank=True,null=True)
    example = models.CharField(max_length=650,blank=True,null=True)
    synonym= models.CharField(max_length=600,blank=True,null=True)
    
 
    day = models.DateField(default=datetime.date.today,db_index=True)
    
    new_id=models.CharField(max_length=300,default='',blank=True,null=True,db_index=True)
    
    creation_time= models.TimeField(blank=True, null=True)

    
    word_img = models.FileField(upload_to='word/%Y/%m/%d',blank=True,null=True)
    class Meta:
        ordering = ["-day"]



    def __str__(self):
        return self.day.strftime('%d/%m/%Y') + '...'+ self.word

    def save(self):
        self.new_id= self.word +self.day.strftime('%d-%m-%Y')
        super(the_hindu_word_list1, self).save()    



class the_hindu_word_list2(models.Model):
    
    word = models.CharField(max_length=150,db_index=True)
    meaning = models.CharField(max_length=650,blank=True,null=True)
    example = models.CharField(max_length=650,blank=True,null=True)
    synonym= models.CharField(max_length=600,blank=True,null=True)
 
    day = models.DateField(default=datetime.date.today,db_index=True)
    
    new_id=models.CharField(max_length=300,default='',blank=True,null=True,db_index=True)
    
    creation_time= models.TimeField(blank=True, null=True)

    
    word_img = models.FileField(upload_to='word/%Y/%m/%d',blank=True,null=True)
    class Meta:
        ordering = ["-day"]
        

    

    
   
    
    
    def __str__(self):
        return self.day.strftime('%d/%m/%Y') + '...'+ self.word

    def save(self):
        self.new_id= self.word+self.day.strftime('%d-%m-%Y') 
        super(the_hindu_word_list2, self).save()



class the_economy_word_Header1(models.Model):
    
   
    Heading_for_list1=models.TextField() 
    day = models.DateField(default=datetime.date.today,db_index=True)
    creation_time= models.TimeField(blank=True, null=True)
    
    new_id=models.CharField(max_length=300,default='',blank=True,null=True,db_index=True)
    link = models.CharField(max_length=450,blank=True,null=True)
    class Meta:
        ordering = ["-day"]

    def __str__(self):
        return self.day.strftime('%d/%m/%Y')+self.Heading_for_list1[:30]

    def save(self):
        self.new_id= 'the_economy_header1' +self.day.strftime('%d-%m-%Y')
        super(the_economy_word_Header1, self).save()


    







class the_economy_word_Header2(models.Model):
    
   
    Heading_for_list2=models.TextField() 
    day = models.DateField(default=datetime.date.today,db_index=True)
    creation_time= models.TimeField(blank=True, null=True)
    link = models.CharField(max_length=450,blank=True,null=True)
    new_id=models.CharField(max_length=300,default='',blank=True,null=True,db_index=True)
    class Meta:
        ordering = ["-day"]

    def __str__(self):
        return self.day.strftime('%d/%m/%Y')

    def save(self):
        self.new_id= 'the_economy_header2' +self.day.strftime('%d-%m-%Y')
        super(the_economy_word_Header2, self).save()       
               


    
class the_economy_word_list1(models.Model):
    
    word = models.CharField(max_length=150,db_index=True)
    meaning = models.CharField(max_length=650,blank=True,null=True)
    example = models.CharField(max_length=650,blank=True,null=True)
    synonym= models.CharField(max_length=600,blank=True,null=True)
     
    day = models.DateField(default=datetime.date.today,db_index=True)
    
    new_id=models.CharField(max_length=300,default='',blank=True,null=True,db_index=True)
    
    creation_time= models.TimeField(blank=True, null=True)

    
    word_img = models.FileField(upload_to='word/%Y/%m/%d',blank=True,null=True)
    class Meta:
        ordering = ["-day"]

    def __str__(self):
        return self.day.strftime('%d/%m/%Y') + '...'+ self.word

    def save(self):
        self.new_id= self.word+self.day.strftime('%d-%m-%Y') 
        super(the_economy_word_list1, self).save()
    





class the_economy_word_list2(models.Model):
    
    word = models.CharField(max_length=150,db_index=True)
    meaning = models.CharField(max_length=650,blank=True,null=True)
    example = models.CharField(max_length=650,blank=True,null=True)
    synonym= models.CharField(max_length=600,blank=True,null=True)
 
    day = models.DateField(default=datetime.date.today,db_index=True)
    
    new_id=models.CharField(max_length=300,default='',blank=True,null=True,db_index=True)
    
    creation_time= models.TimeField(blank=True, null=True)

    
    word_img = models.FileField(upload_to='word/%Y/%m/%d',blank=True,null=True)
    class Meta:
        ordering = ["-day"]


    def __str__(self):
        return self.day.strftime('%d/%m/%Y') + '...'+ self.word

    def save(self):
        self.new_id= self.word+self.day.strftime('%d-%m-%Y')
        super(the_economy_word_list2, self).save()


class home(models.Model):
    
   
    
 
    word1_day = models.DateField(blank=True,null=True,db_index=True)
    word2_day = models.DateField(blank=True,null=True,db_index=True)
    word_e1_day = models.DateField(blank=True,null=True,db_index=True)
    word_e2_day = models.DateField(blank=True,null=True,db_index=True)
    
    day = models.DateField(default=datetime.date.today,db_index=True)
   
    
    creation_time= models.TimeField(blank=True, null=True)

    
    img = models.FileField(upload_to='home/%Y/%m/%d',blank=True,null=True)
    class Meta:
        ordering = ["-day"]


    def __str__(self):
        return self.day.strftime('%d/%m/%Y') + '...'+ str(self.creation_time)

    def save(self):
        
        super(home, self).save()





class total_english(models.Model):
    
    total_the_hindu_word_list1 = models.IntegerField (db_index=True,default=0)
    total_the_hindu_word_list2 = models.IntegerField (db_index=True,default=0)
    total_the_hindu_header1 = models.IntegerField (db_index=True,default=0)
    total_the_hindu_header2 = models.IntegerField (db_index=True,default=0)
    total_the_economy_word_list1 = models.IntegerField (db_index=True,default=0)
    total_the_economy_word_list2 = models.IntegerField (db_index=True,default=0)
    total_the_economy_header1 = models.IntegerField (db_index=True,default=0)
    total_the_economy_header2 = models.IntegerField (db_index=True,default=0)
    total_page = models.IntegerField (db_index=True,default=0)
    no_of_hindu_today = models.IntegerField (db_index=True,default=0)
    no_of_economy_today = models.IntegerField (db_index=True,default=0)
    
    test=models.CharField(max_length=500,default='',blank=True,null=True)


    
    

    def save(self):
        totall=the_hindu_word_list1.objects.all().distinct('day').count()
        self.total_page= totall
        date_object_from_hindu_one = the_hindu_word_list1.objects.values('day').order_by('-day')[:1]
        date_from_hindu_one=(date_object_from_hindu_one[0]['day'])
        date_object_from_hindu_two=the_hindu_word_list2.objects.values('day').order_by('-day')[:1]
        date_from_hindu_two=(date_object_from_hindu_two[0]['day'])
        
        
        date_object_from_economy_one = the_economy_word_list1.objects.values('day').order_by('-day')[:1]
        if(date_object_from_economy_one.count()>0):
            date_from_economy_one=(date_object_from_economy_one[0]['day'])
        
        date_object_from_economy_two = the_economy_word_list2.objects.values('day').order_by('-day')[:1]
        if(date_object_from_economy_two.count()>0):
            
            date_from_economy_two=(date_object_from_economy_two[0]['day'])
        
        if(date_from_hindu_one==date_from_hindu_two):
            self.no_of_hindu_today= 2

        else:
            self.no_of_hindu_today= 1

            
        if(date_object_from_economy_two.count()>0):
            if(the_economy_word_list1==the_economy_word_list2):
                self.no_of_economy_today= 2

            else:
                self.no_of_economy_today= 1
                

        else:
            self.no_of_economy_today= 1

        self.total_the_hindu_word_list1=the_hindu_word_list1.objects.count()
        self.total_the_hindu_word_list2=the_hindu_word_list2.objects.count()
        self.total_the_hindu_header1=the_hindu_word_Header1.objects.count()
        self.total_the_hindu_header2=the_hindu_word_Header2.objects.count()
        self.total_the_economy_word_list1=the_economy_word_list1.objects.count()
        self.total_the_economy_word_list2=the_economy_word_list2.objects.count()
        self.total_the_hindu_header1=the_economy_word_Header1.objects.count()
        self.total_the_hindu_header2=the_economy_word_Header2.objects.count()
        self.test=  date_object_from_economy_two

    
        def __str__(self):
            return self.day.strftime('%d/%m/%Y')               


            
        super(total_english, self).save()
        

class math(models.Model):
    question_no = models.IntegerField (default=1,blank=True, null=True)
    question = models.TextField()
    question_image = models.FileField(upload_to='math/math/%Y/%m/%d/question',blank=True,null=True)
    one = models.FileField(upload_to='math/math/%Y/%m/%d/question',blank=True,null=True)
    two = models.FileField(upload_to='math/math/%Y/%m/%d/question',blank=True,null=True)
    three = models.FileField(upload_to='math/math/%Y/%m/%d/question',blank=True,null=True)
    four = models.FileField(upload_to='math/math/%Y/%m/%d/question',blank=True,null=True)
    five = models.FileField(upload_to='math/math/%Y/%m/%d/question',blank=True,null=True)
    day = models.DateField(default=datetime.date.today,db_index=True)
    creation_time= models.TimeField(blank=True, null=True,db_index=True)


    a=models.CharField(max_length=300,default='',blank=True,null=True)
    a_img = models.FileField(upload_to='math/math/%Y/%m/%d/question',blank=True,null=True)
    
    b=models.CharField(max_length=300,default='',blank=True,null=True)
    b_img = models.FileField(upload_to='math/math/%Y/%m/%d/question',blank=True,null=True)

    c=models.CharField(max_length=300,default='',blank=True,null=True)
    c_img = models.FileField(upload_to='math/math/%Y/%m/%d/question',blank=True,null=True)

    d=models.CharField(max_length=300,default='',blank=True,null=True)
    d_img = models.FileField(upload_to='math/math/%Y/%m/%d/question',blank=True,null=True)

    e=models.CharField(max_length=300,default='',blank=True,null=True)
    e_img = models.FileField(upload_to='math/math/%Y/%m/%d/question',blank=True,null=True)
    solution = models.TextField()
    solution_image = models.FileField(upload_to='word/%Y/%m/%d',blank=True,null=True)
    solution_one = models.FileField(upload_to='math/math/%Y/%m/%d/solution',blank=True,null=True)
    solution_two = models.FileField(upload_to='math/math/%Y/%m/%d/solution',blank=True,null=True)
    solution_three = models.FileField(upload_to='math/math/%Y/%m/%d/solution',blank=True,null=True)
    solution_four = models.FileField(upload_to='math/math/%Y/%m/%d/solution',blank=True,null=True)
    solution_five = models.FileField(upload_to='math/math/%Y/%m/%d/solution',blank=True,null=True)

    level=models.CharField(max_length=100,default='',blank=True,null=True,db_index=True)
    ans = models.IntegerField (default=1)
    new_id=models.CharField(max_length=100,default='',blank=True,null=True,db_index=True)

    shortcut = models.TextField(blank=True,null=True)
    shortcut_image = models.FileField(upload_to='math/math/%Y/%m/%d/short',blank=True,null=True)
    

    use_image = models.IntegerField (default=0)
    time = models.IntegerField (blank=True,null=True)
    s= (
    ("profit_n_loss", "profit_n_loss"),   
    ("squre_n_cube", "squre_n_cube"),
    ("simplification", "simplification"),
    ("average", "average"),
    ("percentage", "percentage"),
    ("problem_on_age", "problem_on_age"),
    ("ratio_n_proportion", "ratio_n_proportion"),
    ("partnership", "partnership"),
    ("time_n_work", "time_n_work"),
    ("pipe_cistern", "pipe_cistern"),
    ("time_n_distance", "time_n_distance"),
    ("problem_on_age", "problem_on_age"),
    ("boats_n_stream", "boats_n_stream"),
    ("alligation_n_mixture", "alligation_n_mixture"),
    ("simple_interest", "simple_interest"),
    ("compound_interest", "compound_interest"),
    
    ("volume_n_surface_area", "volume_n_surface_area"),
    ("probability", "probability"),
    ("permutation_combination", "permutation_combination"),
    ("bar_graph", "bar_graph"),
    ("pie_charts", "pie_charts"),
    ("line_graph", "line_graph"),
   
    

    )
    chapter = models.CharField(max_length=50,
                  choices=s,
                  default="any",blank=True,null=True,db_index=True)
    home = models.BooleanField(default=False,db_index=True)

    s= (
    ("easy", "easy"),   
    ("medium", "medium"),
    ("hard", "hard"),
    )
    difficult_level = models.CharField(max_length=10,
                          choices=s,
                          default="easy",blank=True,null=True,db_index=True)
    extra = models.TextField(blank=True,null=True,default='')

    class Meta:
        ordering = ["-day",'creation_time']

    def __str__(self):
            return self.day.strftime('%d/%m/%Y')+'========  ' +self.question[:30]+' ========    ' +str(self.chapter)+'========='+str(self.question_no)         
    




   

       


class total_math(models.Model):
    
    total_profit_n_loss = models.IntegerField (db_index=True,default=5)
    total_profit_n_loss_page = models.IntegerField (db_index=True,default=5)

    total_squre_n_cube = models.IntegerField (db_index=True,default=5)
    total_squre_n_cube_page = models.IntegerField (db_index=True,default=5)

    total_simplification = models.IntegerField (db_index=True,default=5)
    total_simplification_page = models.IntegerField (db_index=True,default=5)

    total_average = models.IntegerField (db_index=True,default=5)
    total_average_page = models.IntegerField (db_index=True,default=5)

    total_percentage = models.IntegerField (db_index=True,default=5)
    total_percentage_page = models.IntegerField (db_index=True,default=5)

    total_problem_on_age = models.IntegerField (db_index=True,default=5)
    total_problem_on_age_page = models.IntegerField (db_index=True,default=5)

    total_ratio_n_proportion = models.IntegerField (db_index=True,default=5)
    total_ratio_n_proportion_page = models.IntegerField (db_index=True,default=5)

    total_partnership = models.IntegerField (db_index=True,default=5)
    total_partnership_page = models.IntegerField (db_index=True,default=5)

    total_time_n_work = models.IntegerField (db_index=True,default=5)
    total_time_n_work_page = models.IntegerField (db_index=True,default=5)

    total_pipe_cistern = models.IntegerField (db_index=True,default=5)
    total_pipe_cistern_page = models.IntegerField (db_index=True,default=5)

    total_time_n_distance = models.IntegerField (db_index=True,default=5)
    total_time_n_distance_page = models.IntegerField (db_index=True,default=5)

    total_problem_on_age = models.IntegerField (db_index=True,default=5)
    total_problem_on_age_page = models.IntegerField (db_index=True,default=5)

    total_boats_n_stream = models.IntegerField (db_index=True,default=5)
    total_boats_n_stream_page = models.IntegerField (db_index=True,default=5)

    total_alligation_n_mixture = models.IntegerField (db_index=True,default=5)
    total_alligation_n_mixture_page = models.IntegerField (db_index=True,default=5)

    total_simple_interest = models.IntegerField (db_index=True,default=5)
    total_simple_interest_page = models.IntegerField (db_index=True,default=5)

    total_compound_interest = models.IntegerField (db_index=True,default=5)
    total_compound_interest_page = models.IntegerField (db_index=True,default=5)

    total_volume_n_surface_area = models.IntegerField (db_index=True,default=5)
    total_volume_n_surface_area_page = models.IntegerField (db_index=True,default=5)

    total_probability = models.IntegerField (db_index=True,default=5)
    total_probability_page = models.IntegerField (db_index=True,default=5)

    total_permutation_combination = models.IntegerField (db_index=True,default=5)
    total_permutation_combination_page = models.IntegerField (db_index=True,default=5)

    total_bar_graph = models.IntegerField (db_index=True,default=5)
    total_bar_graph_page = models.IntegerField (db_index=True,default=5)

    total_pie_charts = models.IntegerField (db_index=True,default=5)
    total_pie_charts_page = models.IntegerField (db_index=True,default=5)

    total_line_graph = models.IntegerField (db_index=True,default=5)
    total_line_graph_page = models.IntegerField (db_index=True,default=5)
    

    
   
    
    


    def save(self):
        totall_profit_n_loss=math.objects.filter(chapter='profit_n_loss').count()
        totall_squre_n_cube=math.objects.filter(chapter='squre_n_cube').count()
        totall_simplification=math.objects.filter(chapter='simplification').count()
        totall_average=math.objects.filter(chapter='average').count()
        totall_percentage=math.objects.filter(chapter='percentage').count()
        totall_problem_on_age=math.objects.filter(chapter='problem_on_age').count()
        totall_ratio_n_proportion=math.objects.filter(chapter='ratio_n_proportion').count()
        totall_partnership=math.objects.filter(chapter='partnership').count()
        totall_time_n_work=math.objects.filter(chapter='time_n_work').count()
        totall_pipe_cistern=math.objects.filter(chapter='pipe_cistern').count()
        totall_time_n_distance=math.objects.filter(chapter='time_n_distance').count()
        totall_problem_on_age=math.objects.filter(chapter='problem_on_age').count()
        totall_boats_n_stream=math.objects.filter(chapter='boats_n_stream').count()
        totall_simple_interest=math.objects.filter(chapter='simple_interest').count()
        totall_alligation_n_mixture=math.objects.filter(chapter='alligation_n_mixture').count()
        totall_compound_interest=math.objects.filter(chapter='compound_interest').count()
        totall_volume_n_surface_area=math.objects.filter(chapter='volume_n_surface_area').count()
        totall_probability=math.objects.filter(chapter='probability').count()
        totall_permutation_combination=math.objects.filter(chapter='permutation_combination').count()
        totall_bar_graph=math.objects.filter(chapter='bar_graph').count()
        totall_pie_charts=math.objects.filter(chapter='pie_charts').count()
        totall_line_graph=math.objects.filter(chapter='line_graph').count()
       
        

     
        if totall_profit_n_loss !=0:
            
            if(int(totall_profit_n_loss)%5==0):
                total_profit_n_loss_page=(int(totall_profit_n_loss)/5)
            else:
                total_profit_n_loss_page=(int(totall_profit_n_loss)/5)+1

            self.total_profit_n_loss_page= total_profit_n_loss_page

        if totall_squre_n_cube !=0:
            
            if(int(totall_squre_n_cube)%5==0):
                total_squre_n_cube_page=(int(totall_squre_n_cube)/5)
            else:
                total_squre_n_cube_page=(int(totall_squre_n_cube)/5)+1

            self.total_squre_n_cube_page= total_squre_n_cube_page        


        if totall_simplification !=0:
            
            if(int(totall_simplification)%5==0):
                total_simplification_page=(int(totall_simplification)/5)
            else:
                total_simplification_page=(int(totall_simplification)/5)+1

            self.total_simplification_page= total_simplification_page        

        if totall_average !=0:
            
            if(int(totall_average)%5==0):
                total_average_page=(int(totall_average)/5)
            else:
                total_average_page=(int(totall_average)/5)+1

            self.total_average_page= total_average_page        

        if totall_percentage !=0:
            
            if(int(totall_profit_n_loss)%5==0):
                total_percentage_page=(int(totall_profit_n_loss)/5)
            else:
                total_percentage_page=(int(totall_profit_n_loss)/5)+1

            self.total_percentage_page= total_percentage_page        

        if totall_problem_on_age !=0:
            
            if(int(totall_problem_on_age)%5==0):
                total_problem_on_age_page=(int(totall_problem_on_age)/5)
            else:
                total_problem_on_age_page=(int(totall_problem_on_age)/5)+1

            self.total_problem_on_age_page= total_problem_on_age_page        

        if totall_ratio_n_proportion !=0:
            
            if(int(totall_ratio_n_proportion)%5==0):
                total_ratio_n_proportion_page=(int(totall_ratio_n_proportion)/5)
            else:
                total_ratio_n_proportion_page=(int(totall_ratio_n_proportion)/5)+1

            self.total_ratio_n_proportion_page= total_ratio_n_proportion_page        

        if totall_partnership !=0:
            
            if(int(totall_partnership)%5==0):
                total_partnership_page=(int(totall_partnership)/5)
            else:
                total_partnership_page=(int(totall_partnership)/5)+1

            self.total_partnership_page= total_partnership_page        

        if totall_time_n_work !=0:
            
            if(int(totall_time_n_work)%5==0):
                total_time_n_work_page=(int(totall_time_n_work)/5)
            else:
                total_time_n_work_page=(int(totall_time_n_work)/5)+1

            self.total_time_n_work_page= total_time_n_work_page        

        if totall_pipe_cistern !=0:
            
            if(int(totall_pipe_cistern)%5==0):
                total_time_n_distance_page=(int(totall_pipe_cistern)/5)
            else:
                total_pipe_cistern_page=(int(totall_pipe_cistern)/5)+1

            self.total_pipe_cistern_page= total_pipe_cistern_page        

        if totall_time_n_distance !=0:
            
            if(int(totall_time_n_distance)%5==0):
                total_time_n_distance_page=(int(totall_time_n_distance)/5)
            else:
                total_time_n_distance_page=(int(totall_time_n_distance)/5)+1

            self.total_time_n_distance_page= total_time_n_distance_page        

        if totall_problem_on_age !=0:
            
            if(int(totall_problem_on_age)%5==0):
                total_problem_on_age_page=(int(totall_problem_on_age)/5)
            else:
                total_problem_on_age_page=(int(totall_problem_on_age)/5)+1

            self.total_problem_on_age_page= total_problem_on_age_page        

        if totall_boats_n_stream !=0:
            
            if(int(totall_boats_n_stream)%5==0):
                total_boats_n_stream_page=(int(totall_boats_n_stream)/5)
            else:
                total_boats_n_stream_page=(int(totall_boats_n_stream)/5)+1

            self.total_boats_n_stream_page= total_boats_n_stream_page        

        if totall_alligation_n_mixture !=0:
            
            if(int(totall_alligation_n_mixture)%5==0):
                total_alligation_n_mixture_page=(int(totall_alligation_n_mixture)/5)
            else:
                total_alligation_n_mixture_page=(int(totall_alligation_n_mixture)/5)+1

            self.total_alligation_n_mixture_page= total_alligation_n_mixture_page        

        if totall_simple_interest !=0:
            
            if(int(totall_simple_interest)%5==0):
                total_simple_interest_page=(int(totall_simple_interest)/5)
            else:
                total_simple_interest_page=(int(totall_simple_interest)/5)+1

            self.total_simple_interest_page= total_simple_interest_page        

        if totall_compound_interest !=0:
            
            if(int(totall_compound_interest)%5==0):
                total_compound_interest_page=(int(totall_compound_interest)/5)
            else:
                total_compound_interest_page=(int(totall_compound_interest)/5)+1

            self.total_compound_interest_page= total_compound_interest_page        

        if totall_volume_n_surface_area !=0:
            
            if(int(totall_volume_n_surface_area)%5==0):
                total_volume_n_surface_area_page=(int(totall_volume_n_surface_area)/5)
            else:
                total_volume_n_surface_area_page=(int(totall_volume_n_surface_area)/5)+1

            self.total_volume_n_surface_area_page= total_volume_n_surface_area_page        

        if totall_probability !=0:
            
            if(int(totall_probability)%5==0):
                total_probability_page=(int(totall_probability)/5)
            else:
                total_probability_page=(int(totall_probability)/5)+1

            self.total_probability_page= total_probability_page        

        if totall_permutation_combination !=0:
            
            if(int(totall_permutation_combination)%5==0):
                total_permutation_combination_page=(int(totall_permutation_combination)/5)
            else:
                total_permutation_combination_page=(int(totall_permutation_combination)/5)+1

            self.total_permutation_combination_page= total_permutation_combination_page        

        if totall_bar_graph !=0:
            
            if(int(totall_bar_graph)%5==0):
                total_bar_graph_page=(int(totall_bar_graph)/5)
            else:
                total_bar_graph_page=(int(totall_bar_graph)/5)+1

            self.total_bar_graph_page= total_bar_graph_page        

        if totall_pie_charts !=0:
            
            if(int(totall_pie_charts)%5==0):
                total_pie_charts_page=(int(totall_pie_charts)/5)
            else:
                total_pie_charts_page=(int(totall_pie_charts)/5)+1

            self.total_pie_charts_page= total_pie_charts_page        

        if totall_line_graph !=0:
            
            if(int(totall_line_graph)%5==0):
                total_line_graph_page=(int(totall_line_graph)/5)
            else:
                total_line_graph_page=(int(totall_line_graph)/5)+1

            self.total_line_graph_page= total_line_graph_page        

    

                


            
        super(total_math, self).save()

class job(models.Model):
    top =models.BooleanField(default=False,db_index=True)

    heading = models.CharField(max_length=250)
    ca_img = models.FileField(upload_to='job/%Y/%m/%d',blank=True,null=True)
   
    
    day = models.DateField(default=datetime.date.today,db_index=True)
    creation_time= models.TimeField(blank=True, null=True)
    first_day = models.DateField(default=datetime.date.today,db_index=True)
    last_day = models.DateField(default=datetime.date.today,db_index=True)
    extra_day = models.TextField(default='Admit Download: /// preliminary Exam: ///Main Exam: ///Result of Preliminary Exam: ///Result of Main Exam:',blank=True,null=True)
    
    home =models.BooleanField(default=False,db_index=True)
   
    
    

    eligibility=models.TextField(default='Graduate',blank=True,null=True)
    age=models.TextField(default='Gen: ///OBC: ///Sc: ///ST: ///PH:',blank=True,null=True)
    amount=models.CharField(max_length=300,default='Gen: ///OBC: ///Sc: ///ST: ///PH:',blank=True,null=True)
    graduate_only =models.BooleanField(default=False,db_index=True)
    tenth =models.BooleanField(default=False,db_index=True)
    
    twelth =models.BooleanField(default=False,db_index=True)
    eighth =models.BooleanField(default=False,db_index=True)
    
    
    iti =models.BooleanField(default=False,db_index=True)
    deploma =models.BooleanField(default=False,db_index=True)
    b_com =models.BooleanField(default=False,db_index=True)
    b_ed =models.BooleanField(default=False,db_index=True)
    b_pharm =models.BooleanField(default=False,db_index=True)
    b_sc =models.BooleanField(default=False,db_index=True)
    bba =models.BooleanField(default=False,db_index=True)
    bca =models.BooleanField(default=False,db_index=True)
    bds =models.BooleanField(default=False,db_index=True)
    b_tech =models.BooleanField(default=False,db_index=True)
    
    
   
    
    ca =models.BooleanField(default=False,db_index=True)
    cs =models.BooleanField(default=False,db_index=True)
    

    
    llb =models.BooleanField(default=False,db_index=True)
    llm =models.BooleanField(default=False,db_index=True)

    
    m_com =models.BooleanField(default=False,db_index=True)
    m_ed =models.BooleanField(default=False,db_index=True)
    m_pharm =models.BooleanField(default=False,db_index=True)
    m_sc =models.BooleanField(default=False,db_index=True)
    mba =models.BooleanField(default=False,db_index=True)
    mca =models.BooleanField(default=False,db_index=True)
    m_phil =models.BooleanField(default=False,db_index=True)
    m_tech =models.BooleanField(default=False,db_index=True)
    mbbs =models.BooleanField(default=False,db_index=True)
    medical  =models.BooleanField(default=False,db_index=True)
    
    agriculture =models.BooleanField(default=False,db_index=True)
    
    phd =models.BooleanField(default=False,db_index=True)
    m_phil =models.BooleanField(default=False,db_index=True)
    post_g =models.BooleanField(default=False,db_index=True)
    
    
   
    
    
    s= (
    ("all_india", "ALL INDIA"),   
    ("andaman_nicobar", "Andaman & Nicobar"),
    ("andhra_pradesh", "Andhra Pradesh"),
    ("arunachal_pradesh", "Arunachal Pradesh"),
    ("assam", "Assam"),
    ("bihar", "Bihar"),
    ("chandigarh", "Chandigarh"),
    ("chattisgarh", "Chhattisgarh"),
    ("dadra_nagar_haveli", "Dadra &Nagar Haveli"),
    ("daman_diu", "Daman & Diu"),
    ("delhi", "Delhi"),
    ("goa", "Goa"),
    ("gujarat", "Gujarat"),
    ("haryana", "Haryana"),
    ("himachal_pradesh", "Himachal Pradesh"),
    ("jammu_kashmir", "Jammu & Kashmir"),
    ("jharkhand", "Jharkhand"),
    ("karnataka", "Karnataka"),
    ("kerala", "Kerala"),
    ("madhya_pradesh", "Madhya Pradesh"),
    ("maharashtra", "Maharashtra"),
    ("manipur", "Manipur"),
    ("meghalaya", "Meghalaya"),
    ("mizoram", "Mizoram"),
    ("nagaland", "Nagaland"),
    ("orissa", "Orissa"),
    ("puducherry", "Puducherry"),
    ("punjab", "Punjab"),
    ("rajasthan", "Rajasthan"),
    ("sikkim", "Sikkim"),
    ("tamil_nadu", "Tamil Nadu"),
    ("telangana", "Telangana"),
    ("tripura", "Tripura"),
    ("uttar_pradesh", "Uttar Pradesh"),
    ("uttarakhand", "Uttarakhand"),
    ("west_bengal", "West Bengal"),
    

    )
    state = models.CharField(max_length=50,
                  choices=s,
                  default="any",blank=True,null=True,db_index=True)
    cat= (
    ("any", "ANY"),   
    ("bank", "BANK"),
    ("ssc", "SSC"),
    ("upsc", "UPSC"),
    ("rail", "RAIL"),
    ("defence", "DEFENCE"),
    ("other", "OTHER"),
   
    

    )
    category = models.CharField(max_length=50,
                  choices=cat,
                  default="other",blank=True,null=True,db_index=True)    
    
    apply_link=models.CharField(max_length=300,default='#',blank=True,null=True)
    detail_link=models.CharField(max_length=300,default='#',blank=True,null=True)
    
    
    des = models.FileField(upload_to='job/%Y/%m/%d',blank=True,null=True)
    new_id=models.CharField(max_length=300,default='',blank=True,null=True,db_index=True)

    class Meta:
        ordering = ['-day','-creation_time']

        
   
    
    
    def __str__(self):
        return self.day.strftime('%d/%m/%Y') + '     '+ self.heading

    def save(self):
        self.new_id= self.heading +'===' +self.day.strftime('%d-%m-%Y')
        super(job, self).save()
        


class total_job(models.Model):
    
    total_job = models.IntegerField (default=3)
    total_job_page = models.IntegerField (default=3)
    total_bank = models.IntegerField (default=3)
    total_bank_page = models.IntegerField (default=3)
    
    total_ssc=models.IntegerField (default=0)
    total_ssc_page=models.IntegerField (default=0)
    
    total_upsc = models.IntegerField (default=0)
    total_upsc_page = models.IntegerField (default=0)
    
    total_rail=models.IntegerField (default=0)
    total_rail_page=models.IntegerField (default=0)
    
    total_ssc =models.IntegerField (default=0)
    total_ssc_page =models.IntegerField (default=0)
    
    total_defence  =models.IntegerField (default=0)
    total_defence_page  =models.IntegerField (default=0)
    
    total_other =models.IntegerField (default=0)
    total_other_page =models.IntegerField (default=0)
    
    def __str__(self):
        return ' %s' % (self.total_job)
    class Admin:
        list_display = ('total_job', 'total_bank', 'total_ssc')

    

    
    
    

    
   
    
    


    def save(self):
        totall=job.objects.count()
        self.total_job= totall
        self.total_job_page=int(totall+300)/10

        total_bank=job.objects.filter(category='bank').count()
        total_ssc=job.objects.filter(category='ssc').count()
        total_upsc=job.objects.filter(category='upsc').count()
        total_rail=job.objects.filter(category='rail').count()
        total_defence=job.objects.filter(category='defence').count()
        total_other=job.objects.filter(category='other').count()
        total_other=int(total_other)+300
        

       
        
        if total_bank !=0:
            
            if(int(total_bank)%10==0):
                total_total_bank=(int(total_bank)/10)
            else:
                total_total_bank=(int(total_bank)/10)+1

            self.total_bank_page= total_total_bank
            self.total_bank= total_bank

                


        if total_ssc !=0:
            
            if(int(total_ssc)%10==0):
                total_total_ssc=(int(total_ssc)/10)
            else:
                total_total_ssc=(int(total_ssc)/10)+1

            self.total_ssc_page= total_total_ssc
            self.total_ssc= total_ssc 

        if total_upsc !=0:
            
            if(int(total_upsc)%10==0):
                total_total_upsc=(int(total_upsc)/10)
            else:
                total_total_upsc=(int(total_upsc)/10)+1

            self.total_upsc_page= total_total_upsc
        if total_rail !=0:
            
            if(int(total_rail)%10==0):
                total_total_rail=(int(total_rail)/10)
            else:
                total_total_railway=(int(total_rail)/10)+1

            self.total_rail_page= total_total_railway
        if total_defence !=0:
            
            if(int(total_defence)%10==0):
                total_total_defence=(int(total_defence)/10)
            else:
                total_total_defence=(int(total_defence)/10)+1

            self.total_defence_page= total_total_defence
        if total_other !=0:
            
            if(int(total_other)%10==0):
                total_total_other=(int(total_other)/10)
            else:
                total_total_other=(int(total_other)/10)+1

            self.total_other_page= total_total_other
            
     

            
        super(total_job, self).save()




class total_job_category(models.Model):
    
  

    total_graduate_only =models.IntegerField (default=0)
    total_graduate_only_page =models.IntegerField (default=0)

    total_tenth =models.IntegerField (default=0)
    total_tenth_page =models.IntegerField (default=0)
    
    total_twelth =models.IntegerField (default=0)
    total_twelth_page =models.IntegerField (default=0)
    
    total_iti =models.IntegerField (default=0)
    total_iti_page =models.IntegerField (default=0)
    
    total_b_com =models.IntegerField (default=0)
    total_b_com_page =models.IntegerField (default=0)
    
    total_b_ed =models.IntegerField (default=0)
    total_b_ed_page =models.IntegerField (default=0)
    
    total_b_pharm =models.IntegerField (default=0)
    total_b_pharm_page =models.IntegerField (default=0)
    
    total_b_sc =models.IntegerField (default=0)
    total_b_sc_page =models.IntegerField (default=0)
    
    total_bba =models.IntegerField (default=0)
    total_bba_page =models.IntegerField (default=0)
    
    total_bca =models.IntegerField (default=0)
    total_bca_page =models.IntegerField (default=0)
    
    total_bds =models.IntegerField (default=0)
    total_bds_page =models.IntegerField (default=0)
    
    total_b_tech =models.IntegerField (default=0)
    total_b_tech_page =models.IntegerField (default=0)
    
    total_ca =models.IntegerField (default=0)
    total_ca_page =models.IntegerField (default=0)
    
    total_cs =models.IntegerField (default=0)
    total_cs_page =models.IntegerField (default=0)
    
    total_llb =models.IntegerField (default=0)
    total_llb_page =models.IntegerField (default=0)

    total_llm =models.IntegerField (default=0)
    total_llm_page =models.IntegerField (default=0)
    
    total_m_com =models.IntegerField (default=0)
    total_m_com_page =models.IntegerField (default=0)
    
    total_m_ed =models.IntegerField (default=0)
    total_m_ed_page =models.IntegerField (default=0)
    
    total_m_pharm =models.IntegerField (default=0)
    total_m_pharm_page =models.IntegerField (default=0)
    
    total_m_sc =models.IntegerField (default=0)
    total_m_sc_page =models.IntegerField (default=0)
    
    total_mba =models.IntegerField (default=0)
    total_mba_page =models.IntegerField (default=0)
    
    total_mca =models.IntegerField (default=0)
    total_mca_page =models.IntegerField (default=0)
    
    total_m_phil =models.IntegerField (default=0)
    total_m_phil_page =models.IntegerField (default=0)
    
    total_m_tech =models.IntegerField (default=0)
    total_m_tech_page =models.IntegerField (default=0)
    
    total_mbbs =models.IntegerField (default=0)
    total_mbbs_page =models.IntegerField (default=0)
    
    total_medical =models.IntegerField (default=0)
    total_medical_page =models.IntegerField (default=0)
    
    total_agriculture =models.IntegerField (default=0)
    total_agriculture_page =models.IntegerField (default=0)
    
    total_phd =models.IntegerField (default=0)
    total_phd_page =models.IntegerField (default=0)
    
    total_m_phil =models.IntegerField (default=0)
    total_m_phil_page =models.IntegerField (default=0)
    
    total_post_g =models.IntegerField (default=0)
    total_post_g_page =models.IntegerField (default=0)

    total_eighth =models.IntegerField (default=0)
    total_eighth_page =models.IntegerField (default=0)

    total_deploma =models.IntegerField (default=0)
    total_deploma_page =models.IntegerField (default=0)
    

    
    
    

    
   
    
    


    def save(self):
        

        total_graduate_only=job.objects.filter(graduate_only=True).count()
        total_tenth=job.objects.filter(tenth=True).count()
        total_twelth=job.objects.filter(twelth=True).count()
        total_iti=job.objects.filter(iti=True).count()
        total_b_com=job.objects.filter(b_com=True).count()
        total_b_ed=job.objects.filter(b_ed=True).count()
        total_b_pharm=job.objects.filter(b_pharm=True).count()
        total_b_sc=job.objects.filter(b_sc=True).count()
        total_bba=job.objects.filter(bba=True).count()
        total_bca=job.objects.filter(bca=True).count()
        total_bds=job.objects.filter(bds=True).count()
        total_b_tech=job.objects.filter(b_tech=True).count()
        total_ca=job.objects.filter(ca=True).count()
        total_cs=job.objects.filter(cs=True).count()
        total_llb=job.objects.filter(llb=True).count()
        total_m_com=job.objects.filter(m_com=True).count()
        total_m_ed=job.objects.filter(m_ed=True).count()
        total_m_pharm=job.objects.filter(m_pharm=True).count()
        total_m_sc=job.objects.filter(m_sc=True).count()
        total_mba=job.objects.filter(mba=True).count()
        total_mca=job.objects.filter(mca=True).count()
        total_m_phil=job.objects.filter(m_phil=True).count()
        total_m_tech=job.objects.filter(m_tech=True).count()
        total_mbbs=job.objects.filter(mbbs=True).count()
        total_medical=job.objects.filter(medical=True).count()
        total_agriculture=job.objects.filter(agriculture=True).count()
        total_phd=job.objects.filter(phd=True).count()
        total_m_phil=job.objects.filter(m_phil=True).count()
        total_post_g=job.objects.filter(post_g=True).count()
        total_deploma=job.objects.filter(post_g=True).count()
      
        

       
        
        if total_graduate_only !=0:
            
            if(int(total_graduate_only)%10==0):
                total_total_graduate_only=(int(total_graduate_only)/10)
            else:
                total_total_graduate_only=(int(total_graduate_only)/10)+1

            self.total_graduate_only_page= total_total_graduate_only       

        if total_eighth !=0:
            
            if(int(total_eighth)%10==0):
                total_total_tenth=(int(total_eighth)/10)
            else:
                total_total_tenth=(int(total_eighth)/10)+1

            self.total_total_eighth= total_total_tenth        


        if total_tenth !=0:
            
            if(int(total_tenth)%10==0):
                total_total_tenth=(int(total_tenth)/10)
            else:
                total_total_tenth=(int(total_tenth)/10)+1

            self.total_tenth_page= total_total_tenth

        if total_twelth !=0:
            
            if(int(total_tenth)%10==0):
                total_total_twelth=(int(total_twelth)/10)
            else:
                total_total_twelth=(int(total_twelth)/10)+1

            self.total_twelth_page= total_total_twelth



        if total_iti !=0:
            
            if(int(total_iti)%10==0):
                total_total_tenth=(int(total_iti)/10)
            else:
                total_total_iti=(int(total_iti)/10)+1

            self.total_iti_page= total_total_iti


        if total_b_com !=0:
            
            if(int(total_tenth)%10==0):
                total_total_b_com=(int(total_b_com)/10)
            else:
                total_total_b_com=(int(total_b_com)/10)+1

            self.total_b_com_page= total_total_b_com


        if total_b_ed !=0:
            
            if(int(total_b_ed)%10==0):
                total_total_b_ed=(int(total_b_ed)/10)
            else:
                total_total_b_ed=(int(total_b_ed)/10)+1

            self.total_b_ed_page= total_total_b_ed


        if total_b_pharm !=0:
            
            if(int(total_b_pharm)%10==0):
                total_total_b_pharm=(int(total_b_pharm)/10)
            else:
                total_total_b_pharm=(int(total_b_pharm)/10)+1

            self.total_b_pharm_page= total_total_b_pharm


        if total_b_sc !=0:
            
            if(int(total_b_sc)%10==0):
                total_total_b_sc=(int(total_b_sc)/10)
            else:
                total_total_b_sc=(int(total_b_sc)/10)+1

            self.total_b_sc_page= total_total_b_sc


        if total_bba !=0:
            
            if(int(total_bba)%10==0):
                total_total_bba=(int(total_bba)/10)
            else:
                total_total_bba=(int(total_bba)/10)+1

            self.total_bba_page= total_total_bba


        if total_bca !=0:
            
            if(int(total_bca)%10==0):
                total_total_bca=(int(total_bca)/10)
            else:
                total_total_bca=(int(total_bca)/10)+1

            self.total_bca_page= total_total_bca


        if total_bds !=0:
            
            if(int(total_bds)%10==0):
                total_total_bds=(int(total_bds)/10)
            else:
                total_total_bds=(int(total_bds)/10)+1

            self.total_bds_page= total_total_bds


        if total_b_tech !=0:
            
            if(int(total_b_tech)%10==0):
                total_total_b_tech=(int(total_b_tech)/10)
            else:
                total_total_b_tech=(int(total_b_tech)/10)+1

            self.total_b_tech_page= total_total_b_tech


        if total_ca !=0:
            
            if(int(total_ca)%10==0):
                total_total_ca=(int(total_ca)/10)
            else:
                total_total_ca=(int(total_ca)/10)+1

            self.total_ca_page= total_total_ca

        if total_cs !=0:
            
            if(int(total_cs)%10==0):
                total_total_cs=(int(total_cs)/10)
            else:
                total_total_cs=(int(total_cs)/10)+1

            self.total_cs_page= total_total_cs


        if total_llb !=0:
            
            if(int(total_llb)%10==0):
                total_total_llb=(int(total_llb)/10)
            else:
                total_total_llb=(int(total_llb)/10)+1

            self.total_llb_page= total_total_llb

        if total_llm !=0:
            
            if(int(total_llm)%10==0):
                total_total_llm=(int(total_llm)/10)
            else:
                total_total_llm=(int(total_llm)/10)+1

            self.total_llm_page= total_total_llm    


        if total_m_com !=0:
            
            if(int(total_m_com)%10==0):
                total_total_m_com=(int(total_m_com)/10)
            else:
                total_total_m_com=(int(total_m_com)/10)+1

            self.total_m_com_page= total_total_m_com


        if total_m_ed !=0:
            
            if(int(total_m_ed)%10==0):
                total_total_m_ed=(int(total_m_ed)/10)
            else:
                total_total_m_ed=(int(total_m_ed)/10)+1

            self.total_m_ed_page= total_total_m_ed


        if total_m_pharm !=0:
            
            if(int(total_m_pharm)%10==0):
                total_total_m_pharm=(int(total_m_pharm)/10)
            else:
                total_total_m_pharm=(int(total_m_pharm)/10)+1

            self.total_m_pharm_page= total_total_m_pharm


        if total_m_sc !=0:
            
            if(int(total_m_sc)%10==0):
                total_total_m_sc=(int(total_m_sc)/10)
            else:
                total_total_m_sc=(int(total_m_sc)/10)+1

            self.total_m_sc_page= total_total_m_sc


        if total_mba !=0:
            
            if(int(total_mba)%10==0):
                total_total_mba=(int(total_mba)/10)
            else:
                total_total_mba=(int(total_mba)/10)+1

            self.total_mba_page= total_total_mba


        if total_mca !=0:
            
            if(int(total_mca)%10==0):
                total_total_mca=(int(total_mca)/10)
            else:
                total_total_mca=(int(total_mca)/10)+1

            self.total_mca_page= total_total_mca

        if total_m_phil !=0:
            
            if(int(total_m_phil)%10==0):
                total_total_m_phil=(int(total_m_phil)/10)
            else:
                total_total_m_phil=(int(total_m_phil)/10)+1

            self.total_m_phil_page= total_total_m_phil


        if total_m_tech !=0:
            
            if(int(total_m_tech)%10==0):
                total_total_m_tech=(int(total_m_tech)/10)
            else:
                total_total_m_tech=(int(total_m_tech)/10)+1

            self.total_m_tech_page= total_total_m_tech


        if total_mbbs !=0:
            
            if(int(total_mbbs)%10==0):
                total_total_mbbs=(int(total_mbbs)/10)
            else:
                total_total_mbbs=(int(total_mbbs)/10)+1

            self.total_mbbs_page= total_total_mbbs


        if total_medical !=0:
            
            if(int(total_medical)%10==0):
                total_total_medical=(int(total_medical)/10)
            else:
                total_total_medical=(int(total_medical)/10)+1

            self.total_medical_page= total_total_medical


        if total_agriculture !=0:
            
            if(int(total_agriculture)%10==0):
                total_total_agriculture=(int(total_agriculture)/10)
            else:
                total_total_agriculture=(int(total_agriculture)/10)+1

            self.total_agriculture_page= total_total_agriculture


        if total_phd !=0:
            
            if(int(total_phd)%10==0):
                total_total_phd=(int(total_phd)/10)
            else:
                total_total_phd=(int(total_phd)/10)+1

            self.total_phd_page= total_total_phd


        if total_m_phil !=0:
            
            if(int(total_m_phil)%10==0):
                total_total_m_phil=(int(total_m_phil)/10)
            else:
                total_total_m_phil=(int(total_m_phil)/10)+1

            self.total_m_phil_page=total_total_m_phil

        if total_post_g !=0:
            
            if(int(total_post_g)%10==0):
                total_total_post_g=(int(total_post_g)/10)
            else:
                total_total_post_g=(int(total_post_g)/10)+1

            self.total_post_g_page=total_total_post_g

        if total_deploma !=0:
            
            if(int(total_deploma)%10==0):
                total_total_deploma=(int(total_deploma)/10)
            else:
                total_total_deploma=(int(total_deploma)/10)+1

            self.total_deploma_page=total_total_deploma    

            
            

            


        super(total_job_category, self).save()




class total_job_state(models.Model):
    
  

    total_andaman_nicobar =models.IntegerField (default=0)
    total_andaman_nicobar_page =models.IntegerField (default=0)

    total_andhra_pradesh =models.IntegerField (default=0)
    total_andhra_pradesh_page =models.IntegerField (default=0)
    
    total_arunachal_pradesh =models.IntegerField (default=0)
    total_arunachal_pradesh_page =models.IntegerField (default=0)
    
    total_assam =models.IntegerField (default=0)
    total_assam_page =models.IntegerField (default=0)
    
    total_bihar =models.IntegerField (default=0)
    total_bihar_page =models.IntegerField (default=0)
    
    total_chandigarh =models.IntegerField (default=0)
    total_chandigarh_page =models.IntegerField (default=0)
    
    total_chattisgarh =models.IntegerField (default=0)
    total_chattisgarh_page =models.IntegerField (default=0)
    
    total_dadra_nagar_haveli =models.IntegerField (default=0)
    total_dadra_nagar_haveli_page =models.IntegerField (default=0)
    
    total_daman_diu =models.IntegerField (default=0)
    total_daman_diu_page =models.IntegerField (default=0)
    
    total_delhi =models.IntegerField (default=0)
    total_delhi_page =models.IntegerField (default=0)
    
    total_goa =models.IntegerField (default=0)
    total_goa_page =models.IntegerField (default=0)
    
    total_gujarat =models.IntegerField (default=0)
    total_gujarat_page =models.IntegerField (default=0)
    
    total_haryana =models.IntegerField (default=0)
    total_haryana_page =models.IntegerField (default=0)
    
    total_himachal_pradesh =models.IntegerField (default=0)
    total_himachal_pradesh_page =models.IntegerField (default=0)
    
    total_jammu_kashmir =models.IntegerField (default=0)
    total_jammu_kashmir_page =models.IntegerField (default=0)
    
    total_jharkhand =models.IntegerField (default=0)
    total_jharkhand_page =models.IntegerField (default=0)
    
    total_karnataka =models.IntegerField (default=0)
    total_karnataka_page =models.IntegerField (default=0)
    
    total_kerala =models.IntegerField (default=0)
    total_kerala_page =models.IntegerField (default=0)

    total_lakshadweep =models.IntegerField (default=0)
    total_lakshadweep =models.IntegerField (default=0)
    
    
    total_madhya_pradesh =models.IntegerField (default=0)
    total_madhya_pradesh_page =models.IntegerField (default=0)
    
    total_maharashtra =models.IntegerField (default=0)
    total_maharashtra_page =models.IntegerField (default=0)
    
    total_manipur =models.IntegerField (default=0)
    total_manipur_page =models.IntegerField (default=0)
    
    total_meghalaya =models.IntegerField (default=0)
    total_meghalaya_page =models.IntegerField (default=0)
    
    total_mizoram =models.IntegerField (default=0)
    total_mizoram_page =models.IntegerField (default=0)
    
    total_nagaland =models.IntegerField (default=0)
    total_nagaland_page =models.IntegerField (default=0)
    
    total_orissa =models.IntegerField (default=0)
    total_orissa_page =models.IntegerField (default=0)
    
    total_puducherry =models.IntegerField (default=0)
    total_puducherry_page =models.IntegerField (default=0)
    
    total_punjab =models.IntegerField (default=0)
    total_punjab_page =models.IntegerField (default=0)
    
    total_rajasthan =models.IntegerField (default=0)
    total_rajasthan_page =models.IntegerField (default=0)
    
    total_sikkim =models.IntegerField (default=0)
    total_sikkim_page =models.IntegerField (default=0)

    total_tamil_nadu =models.IntegerField (default=0)
    total_tamil_nadu_page =models.IntegerField (default=0)
    
    total_telangana =models.IntegerField (default=0)
    total_telangana_page =models.IntegerField (default=0)
    
    total_tripura =models.IntegerField (default=0)
    total_tripura_page =models.IntegerField (default=0)
    
    total_uttar_pradesh =models.IntegerField (default=0)
    total_uttar_pradesh_page =models.IntegerField (default=0)
    
    total_uttarakhand =models.IntegerField (default=0)
    total_uttarakhand_page =models.IntegerField (default=0)
    
    total_west_bengal =models.IntegerField (default=0)
    total_west_bengal_page =models.IntegerField (default=0)
    
   
    

    
    
    

    
   
    
    


    def save(self):
        

        total_andaman_nicobar=job.objects.filter(state='andaman_nicobar').count()
        total_andhra_pradesh=job.objects.filter(state='andhra_pradesh').count()
        total_arunachal_pradesh=job.objects.filter(state='arunachal_pradesh').count()
        total_assam=job.objects.filter(state='assam').count()
        total_bihar=job.objects.filter(state='bihar').count()
        total_chandigarh=job.objects.filter(state='chandigarh').count()
        total_chattisgarh=job.objects.filter(state='chattisgarh').count()
        total_dadra_nagar_haveli=job.objects.filter(state='dadra_nagar_haveli').count()
        total_daman_diu=job.objects.filter(state='daman_diu').count()
        total_delhi=job.objects.filter(state='delhi').count()
        total_goa=job.objects.filter(state='goa').count()
        total_gujarat=job.objects.filter(state='gujarat').count()
        total_haryana=job.objects.filter(state='haryana').count()
        total_himachal_pradesh=job.objects.filter(state='himachal_pradesh').count()
        total_jammu_kashmir=job.objects.filter(state='jammu_kashmir').count()
        total_jharkhand=job.objects.filter(state='jharkhand').count()
        total_karnataka=job.objects.filter(state='karnataka').count()
        total_kerala=job.objects.filter(state='kerala').count()
        total_madhya_pradesh=job.objects.filter(state='madhya_pradesh').count()
        
        total_lakshadweep=job.objects.filter(state='lakshadweep').count()
        
        total_maharashtra=job.objects.filter(state='maharashtra').count()
        total_manipur=job.objects.filter(state='manipur').count()
        total_meghalaya=job.objects.filter(state='meghalaya').count()
        total_mizoram=job.objects.filter(state='mizoram').count()
        total_nagaland=job.objects.filter(state='nagaland').count()
        total_orissa=job.objects.filter(state='orissa').count()
        total_puducherry=job.objects.filter(state='puducherry').count()
        total_punjab=job.objects.filter(state='punjab').count()
        total_rajasthan=job.objects.filter(state='rajasthan').count()
        total_sikkim=job.objects.filter(state='sikkim').count()
        total_tamil_nadu=job.objects.filter(state='tamil_nadu').count()
        total_telangana=job.objects.filter(state='telangana').count()
        total_tripura=job.objects.filter(state='tripura').count()
        total_uttar_pradesh=job.objects.filter(state='uttar_pradesh').count()
        total_uttarakhand=job.objects.filter(state='uttarakhand').count()
        total_west_bengal=job.objects.filter(state='west_bengal').count()
      
      
        

       
        
        if total_andaman_nicobar !=0:
            
            if(int(total_andaman_nicobar)%10==0):
                total_total_andaman_nicobar=(int(total_andaman_nicobar)/10)
            else:
                total_total_andaman_nicobar=(int(total_andaman_nicobar)/10)+1

            self.total_andaman_nicobar_page= total_total_andaman_nicobar       

                


        if total_andhra_pradesh !=0:
            
            if(int(total_andhra_pradesh)%10==0):
                total_total_andhra_pradesh=(int(total_andhra_pradesh)/10)
            else:
                total_total_andhra_pradesh=(int(total_andhra_pradesh)/10)+1

            self.total_total_andhra_pradesh= total_total_andhra_pradesh

        if total_arunachal_pradesh !=0:
            
            if(int(total_arunachal_pradesh)%10==0):
                total_total_arunachal_pradesh=(int(total_arunachal_pradesh)/10)
            else:
                total_total_arunachal_pradesh=(int(total_arunachal_pradesh)/10)+1

            self.total_arunachal_pradesh_page= total_total_arunachal_pradesh



        if total_assam !=0:
            
            if(int(total_assam)%10==0):
                total_total_assam=(int(total_assam)/10)
            else:
                total_total_assam=(int(total_assam)/10)+1

            self.total_assam_page= total_total_assam


        if total_bihar !=0:
            
            if(int(total_bihar)%10==0):
                total_total_bihar=(int(total_bihar)/10)
            else:
                total_total_bihar=(int(total_bihar)/10)+1

            self.total_bihar_page= total_total_bihar


        if total_chandigarh !=0:
            
            if(int(total_chandigarh)%10==0):
                total_total_chandigarh=(int(total_chandigarh)/10)
            else:
                total_total_chandigarh=(int(total_chandigarh)/10)+1

            self.total_chandigarh_page= total_total_chandigarh


        if total_chattisgarh !=0:
            
            if(int(total_chattisgarh)%10==0):
                total_total_chattisgarh=(int(total_chattisgarh)/10)
            else:
                total_total_chattisgarh=(int(total_chattisgarh)/10)+1

            self.total_chattisgarh_page= total_total_chattisgarh


        if total_dadra_nagar_haveli !=0:
            
            if(int(total_dadra_nagar_haveli)%10==0):
                total_total_dadra_nagar_haveli=(int(total_dadra_nagar_haveli)/10)
            else:
                total_total_dadra_nagar_haveli=(int(total_dadra_nagar_haveli)/10)+1

            self.total_dadra_nagar_haveli_page= total_total_dadra_nagar_haveli


        if total_daman_diu !=0:
            
            if(int(total_daman_diu)%10==0):
                total_total_daman_diu=(int(total_daman_diu)/10)
            else:
                total_total_daman_diu=(int(total_daman_diu)/10)+1

            self.total_daman_diu_page= total_total_daman_diu


        if total_delhi !=0:
            
            if(int(total_delhi)%10==0):
                total_total_delhi=(int(total_delhi)/10)
            else:
                total_total_delhi=(int(total_delhi)/10)+1

            self.total_delhi_page= total_total_delhi


        if total_goa !=0:
            
            if(int(total_goa)%10==0):
                total_total_goa=(int(total_goa)/10)
            else:
                total_total_goa=(int(total_goa)/10)+1

            self.total_goa_page= total_total_goa


        if total_gujarat !=0:
            
            if(int(total_gujarat)%10==0):
                total_total_gujarat=(int(total_gujarat)/10)
            else:
                total_total_gujarat=(int(total_gujarat)/10)+1

            self.total_gujarat_page= total_total_gujarat


        if total_haryana !=0:
            
            if(int(total_haryana)%10==0):
                total_total_haryana=(int(total_haryana)/10)
            else:
                total_total_haryana=(int(total_haryana)/10)+1

            self.total_haryana_page= total_total_haryana

        if total_himachal_pradesh !=0:
            
            if(int(total_himachal_pradesh)%10==0):
                total_total_himachal_pradesh=(int(total_himachal_pradesh)/10)
            else:
                total_total_himachal_pradesh=(int(total_himachal_pradesh)/10)+1

            self.total_himachal_pradesh_page= total_total_himachal_pradesh


        if total_jammu_kashmir !=0:
            
            if(int(total_jammu_kashmir)%10==0):
                total_total_jammu_kashmir=(int(total_jammu_kashmir)/10)
            else:
                total_total_jammu_kashmir=(int(total_jammu_kashmir)/10)+1

            self.total_jammu_kashmir_page= total_total_jammu_kashmir


        if total_jharkhand !=0:
            
            if(int(total_jharkhand)%10==0):
                total_total_jharkhand=(int(total_jharkhand)/10)
            else:
                total_total_jharkhand=(int(total_jharkhand)/10)+1

            self.total_jharkhand_page= total_total_jharkhand


        if total_karnataka !=0:
            
            if(int(total_karnataka)%10==0):
                total_total_karnataka=(int(total_karnataka)/10)
            else:
                total_total_karnataka=(int(total_karnataka)/10)+1

            self.total_karnataka_page= total_total_karnataka


        if total_kerala !=0:
            
            if(int(total_kerala)%10==0):
                total_total_kerala=(int(total_kerala)/10)
            else:
                total_total_kerala=(int(total_kerala)/10)+1

            self.total_kerala_page= total_total_kerala

        if total_lakshadweep !=0:
            
            if(int(total_lakshadweep)%10==0):
                total_total_lakshadweep=(int(total_lakshadweep)/10)
            else:
                total_total_lakshadweep=(int(total_lakshadweep)/10)+1

            self.total_lakshadweep_page= total_total_lakshadweep    


        if total_madhya_pradesh !=0:
            
            if(int(total_madhya_pradesh)%10==0):
                total_total_madhya_pradesh=(int(total_madhya_pradesh)/10)
            else:
                total_total_madhya_pradesh=(int(total_madhya_pradesh)/10)+1

            self.total_madhya_pradesh_page= total_total_madhya_pradesh


        if total_maharashtra !=0:
            
            if(int(total_maharashtra)%10==0):
                total_total_maharashtra=(int(total_maharashtra)/10)
            else:
                total_total_maharashtra=(int(total_maharashtra)/10)+1

            self.total_maharashtra_page= total_total_maharashtra


        if total_manipur !=0:
            
            if(int(total_manipur)%10==0):
                total_total_manipur=(int(total_manipur)/10)
            else:
                total_total_manipur=(int(total_manipur)/10)+1

            self.total_manipur_page= total_total_manipur

        if total_meghalaya !=0:
            
            if(int(total_meghalaya)%10==0):
                total_total_meghalaya=(int(total_meghalaya)/10)
            else:
                total_total_meghalaya=(int(total_meghalaya)/10)+1

            self.total_meghalaya_page= total_total_meghalaya


        if total_mizoram !=0:
            
            if(int(total_mizoram)%10==0):
                total_total_mizoram=(int(total_mizoram)/10)
            else:
                total_total_mizoram=(int(total_mizoram)/10)+1

            self.total_mizoram_page= total_total_mizoram


        if total_nagaland !=0:
            
            if(int(total_nagaland)%10==0):
                total_total_nagaland=(int(total_nagaland)/10)
            else:
                total_total_nagaland=(int(total_nagaland)/10)+1

            self.total_nagaland_page= total_total_nagaland


        if total_orissa !=0:
            
            if(int(total_orissa)%10==0):
                total_total_orissa=(int(total_orissa)/10)
            else:
                total_total_orissa=(int(total_medical)/10)+1

            self.total_orissa_page= total_total_orissa


        if total_puducherry !=0:
            
            if(int(total_puducherry)%10==0):
                total_total_puducherry=(int(total_puducherry)/10)
            else:
                total_total_puducherry=(int(total_puducherry)/10)+1

            self.total_puducherry_page= total_total_puducherry


        if total_punjab !=0:
            
            if(int(total_punjab)%10==0):
                total_total_punjab=(int(total_punjab)/10)
            else:
                total_total_punjab=(int(total_punjab)/10)+1

            self.total_punjab_page= total_total_punjab


        if total_rajasthan !=0:
            
            if(int(total_rajasthan)%10==0):
                total_total_rajasthan=(int(total_rajasthan)/10)
            else:
                total_total_rajasthan=(int(total_rajasthan)/10)+1

            self.total_rajasthan_page=total_total_rajasthan

        if total_sikkim !=0:
            
            if(int(total_sikkim)%10==0):
                total_total_sikkim=(int(total_sikkim)/10)
            else:
                total_total_sikkim=(int(total_sikkim)/10)+1

            self.total_sikkim_page=total_total_sikkim


        if total_tamil_nadu !=0:
            
            if(int(total_tamil_nadu)%10==0):
                total_total_tamil_nadu=(int(total_tamil_nadu)/10)
            else:
                total_total_tamil_nadu=(int(total_tamil_nadu)/10)+1

            self.total_tamil_nadu_page=total_total_tamil_nadu

        if total_telangana !=0:
            
            if(int(total_telangana)%10==0):
                total_total_telangana=(int(total_telangana)/10)
            else:
                total_total_telangana=(int(total_telangana)/10)+1

            self.total_telangana_page=total_total_telangana

        if total_tripura !=0:
            
            if(int(total_tripura)%10==0):
                total_total_tripura=(int(total_tripura)/10)
            else:
                total_total_tripura=(int(total_tripura)/10)+1

            self.total_tripura_page=total_total_tripura

        if total_uttar_pradesh !=0:
            
            if(int(total_uttar_pradesh)%10==0):
                total_total_uttar_pradesh=(int(total_uttar_pradesh)/10)
            else:
                total_total_uttar_pradesh=(int(total_uttar_pradesh)/10)+1

            self.total_uttar_pradesh_page=total_total_uttar_pradesh

        if total_uttarakhand !=0:
            
            if(int(total_uttarakhand)%10==0):
                total_total_uttarakhand=(int(total_uttarakhand)/10)
            else:
                total_total_uttarakhand=(int(total_uttarakhand)/10)+1

            self.total_uttarakhand_page=total_total_uttarakhand

    
        if total_west_bengal !=0:
            
            if(int(total_west_bengal)%10==0):
                total_total_west_bengal=(int(total_west_bengal)/10)
            else:
                total_total_west_bengal=(int(total_west_bengal)/10)+1

            self.total_west_bengal_page=total_total_west_bengal

    

            
            

            super(total_job_state, self).save()
        
        



class topic(models.Model):
    
    headline = models.CharField(max_length=150,db_index=True)
    
 
    day = models.DateField(default=datetime.date.today,db_index=True)
    
    new_id=models.CharField(max_length=300,default='',blank=True,null=True,db_index=True)
    
    creation_time= models.TimeField(blank=True, null=True)

    
    file = models.FileField(upload_to='topic/%Y/%m/%d',blank=True,null=True)
    class Meta:
        ordering = ["-day"]



    def __str__(self):
        return self.day.strftime('%d/%m/%Y') + '...'+ self.headline

    def save(self):
        self.new_id= self.headline +self.day.strftime('%d-%m-%Y')
        super(topic, self).save()




        


        
class user_save(models.Model):
    
    user_id = models.CharField(max_length=150,db_index=True)
    section = models.CharField(max_length=650,blank=True,null=True)
    headline = models.CharField(max_length=650,blank=True,null=True)
    date_added = models.DateField(default=datetime.date.today,db_index=True)

     
    day = models.DateField(default=datetime.date.today,db_index=True)
    
    img_link=models.CharField(max_length=300,default='',blank=True,null=True)
    
    creation_time= models.TimeField(blank=True, null=True)
    link_id=models.CharField(max_length=650,blank=True,null=True)

    
    

    def __str__(self):
        return self.day.strftime('%d/%m/%Y') + '...'+ self.user_id+ '...'+self.headline

    def save(self):
        super(user_save, self).save()




class reasoning(models.Model):
    
    question = models.TextField()
    question_part = models.TextField(default='',blank=True,null=True)
    question_image = models.FileField(upload_to='reasoning/reasoning/%Y/%m/%d/question',blank=True,null=True)
    one = models.FileField(upload_to='reasoning/reasoning/%Y/%m/%d/question',blank=True,null=True)
    two = models.FileField(upload_to='reasoning/reasoning/%Y/%m/%d/question',blank=True,null=True)
    three = models.FileField(upload_to='reasoning/reasoning/%Y/%m/%d/question',blank=True,null=True)
    four = models.FileField(upload_to='reasoning/reasoning/%Y/%m/%d/question',blank=True,null=True)
    five = models.FileField(upload_to='reasoning/reasoning/%Y/%m/%d/question',blank=True,null=True)
    day = models.DateField(default=datetime.date.today,db_index=True)
    creation_time= models.TimeField(blank=True, null=True,db_index=True)


    a=models.CharField(max_length=300,default='',blank=True,null=True)
    a_img = models.FileField(upload_to='reasoning/reasoning/%Y/%m/%d/question',blank=True,null=True)
    
    b=models.CharField(max_length=300,default='',blank=True,null=True)
    b_img = models.FileField(upload_to='reasoning/reasoning/%Y/%m/%d/question',blank=True,null=True)

    c=models.CharField(max_length=300,default='',blank=True,null=True)
    c_img = models.FileField(upload_to='reasoning/reasoning/%Y/%m/%d/question',blank=True,null=True)

    d=models.CharField(max_length=300,default='',blank=True,null=True)
    d_img = models.FileField(upload_to='reasoning/reasoning/%Y/%m/%d/question',blank=True,null=True)

    e=models.CharField(max_length=300,default='',blank=True,null=True)
    e_img = models.FileField(upload_to='reasoning/reasoning/%Y/%m/%d/question',blank=True,null=True)
    solution = models.TextField()
    solution_image = models.FileField(upload_to='word/%Y/%m/%d',blank=True,null=True)
    solution_one = models.FileField(upload_to='reasoning/reasoning/%Y/%m/%d/solution',blank=True,null=True)
    solution_two = models.FileField(upload_to='reasoning/reasoning/%Y/%m/%d/solution',blank=True,null=True)
    solution_three = models.FileField(upload_to='reasoning/reasoning/%Y/%m/%d/solution',blank=True,null=True)
    solution_four = models.FileField(upload_to='reasoning/reasoning/%Y/%m/%d/solution',blank=True,null=True)
    solution_five = models.FileField(upload_to='reasoning/reasoning/%Y/%m/%d/solution',blank=True,null=True)

    level=models.CharField(max_length=100,default='',blank=True,null=True,db_index=True)
    ans = models.CharField(max_length=100,default='',blank=True,null=True)
    new_id=models.CharField(max_length=100,default='',blank=True,null=True,db_index=True)

    shortcut = models.TextField(blank=True,null=True)
    shortcut_image = models.FileField(upload_to='reasoning/reasoning/%Y/%m/%d/short',blank=True,null=True)
    

    use_image = models.IntegerField (default=0)
    time = models.IntegerField (blank=True,null=True)
    s= (
    ("analogy", "analogy"),   
    ("classification", "classification"),
    ("alpha_numaric_symbol", "alpha_numaric_symbol"),
    ("coding_decoding", "coding_decoding"),
    ("fictious_symbol", "fictious_symbol"),
    ("seating_arrangment", "seating_arrangment"),
    ("Ranking_test", "Ranking_test"),
    ("inequality_and_coded_inequality", "inequality_and_coded_inequality"),
    ("input_output", "input_output"),
    ("circle_puzzle", "circle_puzzle"),
    ("squere_puzzle", "squere_puzzle"),
    ("flore_puzzle", "flore_puzzle"),
    ("blood_relation", "blood_relation"),
    ("coded_relationship", "coded_relationship"),
    ("decision_making", "decision_making"),
    ("syllogism", "syllogism"),
    ("clock", "clock"),
    ("calender", "calender"),
    
    ("arguments", "arguments"),
    ("cause_n_effect", "cause_n_effect"),
    ("direction_test", "direction_test"),
   
   
    

    )
    chapter = models.CharField(max_length=50,
                  choices=s,
                  default="any",blank=True,null=True,db_index=True)
    home = models.BooleanField(default=False,db_index=True)

    class Meta:
        ordering = ["-day",'creation_time']
    def __str__(self):
            
            return self.day.strftime('%d/%m/%Y')+'========  ' +self.question[:30]+' ========    ' +str(self.chapter)


    
    

    def save(self):
        
        self.new_id= str(self.day)+str(self.creation_time)+self.question[:30]
       

    
        super(reasoning, self).save()
        
    

class total_reasoning(models.Model):
    
    total_analogy = models.IntegerField (db_index=True,default=5)
    total_analogy_page = models.IntegerField (db_index=True,default=5)

    total_classification = models.IntegerField (db_index=True,default=5)
    total_classification_page = models.IntegerField (db_index=True,default=5)

    total_alpha_numaric_symbol = models.IntegerField (db_index=True,default=5)
    total_alpha_numaric_symbol_page = models.IntegerField (db_index=True,default=5)

    total_coding_decoding = models.IntegerField (db_index=True,default=5)
    total_coding_decoding_page = models.IntegerField (db_index=True,default=5)

    total_fictious_symbol = models.IntegerField (db_index=True,default=5)
    total_fictious_symbol_page = models.IntegerField (db_index=True,default=5)

    total_flore_puzzle = models.IntegerField (db_index=True,default=5)
    total_flore_puzzle_page = models.IntegerField (db_index=True,default=5)

    total_Ranking_test = models.IntegerField (db_index=True,default=5)
    total_Ranking_test_page = models.IntegerField (db_index=True,default=5)

    total_inequality_and_coded_inequality = models.IntegerField (db_index=True,default=5)
    total_inequality_and_coded_inequality_page = models.IntegerField (db_index=True,default=5)

    total_input_output = models.IntegerField (db_index=True,default=5)
    total_input_output_page = models.IntegerField (db_index=True,default=5)

    total_circle_puzzle = models.IntegerField (db_index=True,default=5)
    total_circle_puzzle_page = models.IntegerField (db_index=True,default=5)

    total_squere_puzzle = models.IntegerField (db_index=True,default=5)
    total_squere_puzzle_page = models.IntegerField (db_index=True,default=5)

    total_flore_puzzle = models.IntegerField (db_index=True,default=5)
    total_flore_puzzle_page = models.IntegerField (db_index=True,default=5)

    total_blood_relation = models.IntegerField (db_index=True,default=5)
    total_blood_relation_page = models.IntegerField (db_index=True,default=5)

    total_decision_making = models.IntegerField (db_index=True,default=5)
    total_decision_making_page = models.IntegerField (db_index=True,default=5)

    total_syllogism = models.IntegerField (db_index=True,default=5)
    total_syllogism_page = models.IntegerField (db_index=True,default=5)

    total_clock = models.IntegerField (db_index=True,default=5)
    total_clock_page = models.IntegerField (db_index=True,default=5)

    total_calender = models.IntegerField (db_index=True,default=5)
    total_calender_page = models.IntegerField (db_index=True,default=5)

    total_arguments = models.IntegerField (db_index=True,default=5)
    total_arguments_page = models.IntegerField (db_index=True,default=5)

    total_cause_n_effect = models.IntegerField (db_index=True,default=5)
    total_cause_n_effect_page = models.IntegerField (db_index=True,default=5)
	
    total_direction_test = models.IntegerField (db_index=True,default=5)
    total_direction_test_page = models.IntegerField (db_index=True,default=5)

    total_seating_arrangment= models.IntegerField (db_index=True,default=5)
    total_seating_arrangment_page = models.IntegerField (db_index=True,default=5)

    total_coded_relationship= models.IntegerField (db_index=True,default=5)
    total_coded_relationship_page = models.IntegerField (db_index=True,default=5)
    


    
   
    
    


    def save(self):
        totall_analogy=reasoning.objects.filter(chapter='analogy').count()
        totall_classification=reasoning.objects.filter(chapter='classification').count()
        totall_alpha_numaric_symbol=reasoning.objects.filter(chapter='alpha_numaric_symbol').count()
        totall_coding_decoding=reasoning.objects.filter(chapter='coding_decoding').count()
        totall_fictious_symbol=reasoning.objects.filter(chapter='fictious_symbol').count()
        totall_Ranking_test=reasoning.objects.filter(chapter='Ranking_test').count()
        totall_inequality_and_coded_inequality=reasoning.objects.filter(chapter='inequality_and_coded_inequality').count()
        totall_input_output=reasoning.objects.filter(chapter='input_output').count()
        totall_squere_puzzle=reasoning.objects.filter(chapter='squere_puzzle').count()
        totall_problem_on_age=reasoning.objects.filter(chapter='problem_on_age').count()
        totall_blood_relation=reasoning.objects.filter(chapter='blood_relation').count()
        totall_syllogism=reasoning.objects.filter(chapter='syllogism').count()
        totall_decision_making=reasoning.objects.filter(chapter='decision_making').count()
        totall_clock=reasoning.objects.filter(chapter='clock').count()
        totall_calender=reasoning.objects.filter(chapter='calender').count()
        totall_arrangment=reasoning.objects.filter(chapter='arrangment').count()
        totall_cause_n_effect=reasoning.objects.filter(chapter='cause_n_effect').count()
        totall_direction_test=reasoning.objects.filter(chapter='direction_test').count()

        totall_seating_arrangment=reasoning.objects.filter(chapter='seating_arrangment').count()
       
        totall_coded_relationship=reasoning.objects.filter(chapter='coded_relationship').count()

        totall_flore_puzzle=reasoning.objects.filter(chapter='flore_puzzle').count()
        totall_circle_puzzle=reasoning.objects.filter(chapter='circle_puzzle').count()
        totall_arguments=reasoning.objects.filter(chapter='arguments').count()

     
        if totall_analogy !=0:
            
            if(int(totall_analogy)%5==0):
                total_analogy_page=(int(totall_analogy)/5)
            else:
                total_analogy_page=(int(totall_analogy)/5)+1

            self.total_analogy_page= total_analogy_page

        if totall_classification !=0:
            
            if(int(totall_classification)%5==0):
                total_classification_page=(int(totall_classification)/5)
            else:
                total_classification_page=(int(totall_classification)/5)+1

            self.total_classification_page= total_classification_page        


        if totall_alpha_numaric_symbol !=0:
            
            if(int(totall_alpha_numaric_symbol)%5==0):
                total_alpha_numaric_symbol_page=(int(totall_alpha_numaric_symbol)/5)
            else:
                total_alpha_numaric_symbol_page=(int(totall_alpha_numaric_symbol)/5)+1

            self.total_alpha_numaric_symbol_page= total_alpha_numaric_symbol_page        

        if totall_coding_decoding !=0:
            
            if(int(totall_coding_decoding)%5==0):
                total_coding_decoding_page=(int(totall_coding_decoding)/5)
            else:
                total_coding_decoding_page=(int(totall_coding_decoding)/5)+1

            self.total_coding_decoding_page= total_coding_decoding_page        

        if totall_fictious_symbol !=0:
            
            if(int(totall_fictious_symbol)%5==0):
                total_fictious_symbol_page=(int(totall_fictious_symbol)/5)
            else:
                total_fictious_symbol_page=(int(totall_fictious_symbol)/5)+1

            self.total_fictious_symbol_page= total_fictious_symbol_page        

     
        if totall_flore_puzzle !=0:
            
            if(int(totall_flore_puzzle)%5==0):
               total_flore_puzzle_page=(int(totall_flore_puzzle)/5)
            else:
               total_flore_puzzle_page=(int(totall_flore_puzzle)/5)+1

            self.total_flore_puzzle_page=total_flore_puzzle_page    

        if totall_Ranking_test !=0:
            
            if(int(totall_Ranking_test)%5==0):
                total_Ranking_test_page=(int(totall_Ranking_test)/5)
            else:
                total_Ranking_test_page=(int(totall_Ranking_test)/5)+1

            self.total_Ranking_test_page= total_Ranking_test_page        

        if totall_inequality_and_coded_inequality !=0:
            
            if(int(totall_inequality_and_coded_inequality)%5==0):
                total_inequality_and_coded_inequality_page=(int(totall_inequality_and_coded_inequality)/5)
            else:
                total_inequality_and_coded_inequality_page=(int(totall_inequality_and_coded_inequality)/5)+1

            self.total_inequality_and_coded_inequality_page= total_inequality_and_coded_inequality_page        

        if totall_input_output !=0:
            
            if(int(totall_input_output)%5==0):
                total_input_output_page=(int(totall_input_output)/5)
            else:
                total_input_output_page=(int(totall_input_output)/5)+1

            self.total_input_output_page= total_input_output_page        

        if totall_circle_puzzle !=0:
            
            if(int(totall_circle_puzzle)%5==0):
                total_squere_puzzle_page=(int(totall_circle_puzzle)/5)
            else:
                total_circle_puzzle_page=(int(totall_circle_puzzle)/5)+1

            self.total_circle_puzzle_page= total_circle_puzzle_page        

        if totall_squere_puzzle !=0:
            
            if(int(totall_squere_puzzle)%5==0):
                total_squere_puzzle_page=(int(totall_squere_puzzle)/5)
            else:
                total_squere_puzzle_page=(int(totall_squere_puzzle)/5)+1

            self.total_squere_puzzle_page= total_squere_puzzle_page        

               

        if totall_blood_relation !=0:
            
            if(int(totall_blood_relation)%5==0):
                total_blood_relation_page=(int(totall_blood_relation)/5)
            else:
                total_blood_relation_page=(int(totall_blood_relation)/5)+1

            self.total_blood_relation_page= total_blood_relation_page        

        if totall_decision_making !=0:
            
            if(int(totall_decision_making)%5==0):
                total_decision_making_page=(int(totall_decision_making)/5)
            else:
                total_decision_making_page=(int(totall_decision_making)/5)+1

            self.total_decision_making_page= total_decision_making_page        

        if totall_syllogism !=0:
            
            if(int(totall_syllogism)%5==0):
                total_syllogism_page=(int(totall_syllogism)/5)
            else:
                total_syllogism_page=(int(totall_syllogism)/5)+1

            self.total_syllogism_page= total_syllogism_page        

        if totall_clock !=0:
            
            if(int(totall_clock)%5==0):
                total_clock_page=(int(totall_clock)/5)
            else:
                total_clock_page=(int(totall_clock)/5)+1

            self.total_clock_page= total_clock_page        

        if totall_calender !=0:
            
            if(int(totall_calender)%5==0):
                total_calender_page=(int(totall_calender)/5)
            else:
                total_calender_page=(int(totall_calender)/5)+1

            self.total_calender_page= total_calender_page        

        if totall_arguments !=0:
            
            if(int(totall_arguments)%5==0):
                total_arguments_page=(int(totall_arguments)/5)
            else:
                total_arguments_page=(int(totall_arguments)/5)+1

            self.total_arguments_page= total_arguments_page        

        if totall_cause_n_effect !=0:
            
            if(int(totall_cause_n_effect)%5==0):
                total_cause_n_effect_page=(int(totall_cause_n_effect)/5)
            else:
                total_cause_n_effect_page=(int(totall_cause_n_effect)/5)+1

            self.total_cause_n_effect_page= total_cause_n_effect_page        

	
  
        if totall_seating_arrangment !=0:
            
            if(int(totall_seating_arrangment)%5==0):
                total_seating_arrangment_page=(int(totall_seating_arrangment)/5)
            else:
                total_seating_arrangment_page=(int(totall_seating_arrangment)/5)+1

            self.total_seating_arrangment_page= total_seating_arrangment_page
  
        if totall_coded_relationship !=0:
            
            if(int(totall_coded_relationship)%5==0):
                total_coded_relationship_page=(int(totall_coded_relationship)/5)
            else:
                total_coded_relationship_page=(int(totall_coded_relationship)/5)+1

            self.total_coded_relationship_page= total_coded_relationship_page

        if totall_direction_test !=0:
            
            if(int(totall_direction_test)%5==0):
                total_direction_test_page=(int(totall_direction_test)/5)
            else:
                total_direction_test_page=(int(totall_direction_test)/5)+1

            self.total_direction_test_page= total_direction_test_page    
                


            
        super(total_reasoning, self).save()


class close(models.Model):
    
    question = models.TextField()
    question_part = models.TextField(default='',blank=True,null=True)

    day = models.DateField(default=datetime.date.today,db_index=True)
    creation_time= models.TimeField(blank=True, null=True,db_index=True)


    a=models.CharField(max_length=100,default='',blank=True,null=True)
 
    
    b=models.CharField(max_length=100,default='',blank=True,null=True)
 

    c=models.CharField(max_length=100,default='',blank=True,null=True)


    d=models.CharField(max_length=100,default='',blank=True,null=True)


    e=models.CharField(max_length=100,default='',blank=True,null=True)

    f=models.CharField(max_length=100,default='',blank=True,null=True)

    g=models.CharField(max_length=100,default='',blank=True,null=True)
    h=models.CharField(max_length=100,default='',blank=True,null=True)
    i=models.CharField(max_length=100,default='',blank=True,null=True)
    j=models.CharField(max_length=100,default='',blank=True,null=True)
    

    solution = models.TextField()


    level=models.CharField(max_length=100,default='',blank=True,null=True,db_index=True)
    ans = models.CharField(max_length=100,default='',blank=True,null=True)
    loop=models.CharField(max_length=100,default='',blank=True,null=True)
    new_id=models.CharField(max_length=100,default='',blank=True,null=True,db_index=True)

 
    


    time = models.IntegerField (blank=True,null=True)

    home = models.BooleanField(default=False,db_index=True)
    page = models.IntegerField (blank=True,null=True)

    class Meta:
        ordering = ["-day",'creation_time']
    def __str__(self):
            return self.day.strftime('%d/%m/%Y') +self.question[:30]  


    
    

    def save(self):
        
        self.new_id= str(self.day)+str(self.creation_time)+self.question[:30]
       

    
        super(close, self).save()


class error(models.Model):
    
    question = models.TextField(blank=True,null=True)
    question_part = models.TextField(default='',blank=True,null=True)

    day = models.DateField(default=datetime.date.today,db_index=True)
    creation_time= models.TimeField(blank=True, null=True,db_index=True)


    a=models.CharField(max_length=100,default='',blank=True,null=True)
 
    
    b=models.CharField(max_length=100,default='',blank=True,null=True)
 

    c=models.CharField(max_length=100,default='',blank=True,null=True)


    d=models.CharField(max_length=100,default='',blank=True,null=True)


    e=models.CharField(max_length=100,default='',blank=True,null=True)

    f=models.CharField(max_length=100,default='',blank=True,null=True)

    g=models.CharField(max_length=100,default='',blank=True,null=True)
    h=models.CharField(max_length=100,default='',blank=True,null=True)
    i=models.CharField(max_length=100,default='',blank=True,null=True)
    j=models.CharField(max_length=100,default='',blank=True,null=True)

    solution = models.TextField()


    level=models.CharField(max_length=100,default='',blank=True,null=True,db_index=True)
    ans = models.CharField(max_length=100,default='',blank=True,null=True)
    

    new_id=models.CharField(max_length=100,default='',blank=True,null=True,db_index=True)

 
    


    time = models.IntegerField (blank=True,null=True)
    s= (
    ("noun", "noun"),   
    ("pronoun", "pronoun"),
    ("verb", "verb"),
    ("adjective", "adjective"),
    ("adverb", "adverb"),
    ("interjection", "interjection"),
    ("conjunction", "conjunction"),
    ("preposition", "preposition"),
    ("miscellaneous", "miscellaneous"),
    ("article", "article"),
    ("number", "number"),
  
   
   
    

    )
    chapter = models.CharField(max_length=50,
                  choices=s,
                  default="any",blank=True,null=True,db_index=True)
    home = models.BooleanField(default=False,db_index=True)

    class Meta:
        ordering = ["-day",'creation_time']
    def __str__(self):
            return self.day.strftime('%d/%m/%Y') +self.question[:30]  


    
    

    def save(self):
        
        self.new_id= str(self.day)+str(self.creation_time)+self.question[:30]
       

    
        super(error, self).save()










class total_error(models.Model):
    
    total_noun = models.IntegerField (db_index=True,default=5)
    total_noun_page = models.IntegerField (db_index=True,default=5)

    total_pronoun = models.IntegerField (db_index=True,default=5)
    total_pronoun_page = models.IntegerField (db_index=True,default=5)

    total_verb = models.IntegerField (db_index=True,default=5)
    total_verb_page = models.IntegerField (db_index=True,default=5)

    total_adjective = models.IntegerField (db_index=True,default=5)
    total_adjective_page = models.IntegerField (db_index=True,default=5)

    total_adverb = models.IntegerField (db_index=True,default=5)
    total_adverb_page = models.IntegerField (db_index=True,default=5)

    total_interjection = models.IntegerField (db_index=True,default=5)
    total_interjection_page = models.IntegerField (db_index=True,default=5)

    total_conjunction = models.IntegerField (db_index=True,default=5)
    total_conjunction_page = models.IntegerField (db_index=True,default=5)

    total_preposition = models.IntegerField (db_index=True,default=5)
    total_preposition_page = models.IntegerField (db_index=True,default=5)

    total_miscellaneous = models.IntegerField (db_index=True,default=5)
    total_miscellaneous_page = models.IntegerField (db_index=True,default=5)

    total_article = models.IntegerField (db_index=True,default=5)
    total_article_page = models.IntegerField (db_index=True,default=5)

    total_number = models.IntegerField (db_index=True,default=5)
    total_number_page = models.IntegerField (db_index=True,default=5)

  

    
   
    
    


    def save(self):
        totall_noun=reasoning.objects.filter(chapter='noun').count()
        self.total_noun=totall_noun
        totall_pronoun=reasoning.objects.filter(chapter='pronoun').count()
        self.total_pronoun=totall_pronoun
        totall_verb=reasoning.objects.filter(chapter='verb').count()
        self.total_verb=totall_verb
        
        totall_adjective=reasoning.objects.filter(chapter='adjective').count()
        self.total_adjective=totall_adjective
        totall_adverb=reasoning.objects.filter(chapter='adverb').count()
        self.total_adverb=totall_adverb
        totall_conjunction=reasoning.objects.filter(chapter='conjunction').count()
        self.total_conjunction=totall_conjunction
        totall_preposition=reasoning.objects.filter(chapter='preposition').count()
        self.total_preposition=totall_preposition
        totall_miscellaneous=reasoning.objects.filter(chapter='miscellaneous').count()
        self.total_miscellaneous=totall_miscellaneous
        totall_number=reasoning.objects.filter(chapter='number').count()
        self.total_number=totall_number
      
      

        totall_interjection=reasoning.objects.filter(chapter='interjection').count()
        self.total_interjection=totall_interjection
        totall_article=reasoning.objects.filter(chapter='article').count()
        self.total_article=totall_article
     

     
        if totall_noun !=0:
            print(totall_noun)
            
            if(int(totall_noun)%5==0):
                total_noun_page=(int(totall_noun)/5)
            else:
                total_noun_page=(int(totall_noun)/5)+1

            self.total_noun_page= total_noun_page

        if totall_pronoun !=0:
            
            if(int(totall_pronoun)%5==0):
                total_pronoun_page=(int(totall_pronoun)/5)
            else:
                total_pronoun_page=(int(totall_pronoun)/5)+1

            self.total_pronoun_page= total_pronoun_page        


        if totall_verb !=0:
            
            if(int(totall_verb)%5==0):
                total_verb_page=(int(totall_verb)/5)
            else:
                total_verb_page=(int(totall_verb)/5)+1

            self.total_verb_page= total_verb_page        

        if totall_adjective !=0:
            
            if(int(totall_adjective)%5==0):
                total_adjective_page=(int(totall_adjective)/5)
            else:
                total_adjective_page=(int(totall_adjective)/5)+1

            self.total_adjective_page= total_adjective_page        

        if totall_adverb !=0:
            
            if(int(totall_adverb)%5==0):
                total_adverb_page=(int(totall_adverb)/5)
            else:
                total_adverb_page=(int(totall_adverb)/5)+1

            self.total_adverb_page= total_adverb_page        

     
        if totall_interjection !=0:
            
            if(int(totall_interjection)%5==0):
               total_interjection_page=(int(totall_interjection)/5)
            else:
               total_interjection_page=(int(totall_interjection)/5)+1

            self.total_interjection_page=total_interjection_page    

        if totall_conjunction !=0:
            
            if(int(totall_conjunction)%5==0):
                total_conjunction_page=(int(totall_conjunction)/5)
            else:
                total_conjunction_page=(int(totall_conjunction)/5)+1

            self.total_conjunction_page= total_conjunction_page        

        if totall_preposition !=0:
            
            if(int(totall_preposition)%5==0):
                total_preposition_page=(int(totall_preposition)/5)
            else:
                total_preposition_page=(int(totall_preposition)/5)+1

            self.total_preposition_page= total_preposition_page        

        if totall_miscellaneous !=0:
            
            if(int(totall_miscellaneous)%5==0):
                total_miscellaneous_page=(int(totall_miscellaneous)/5)
            else:
                total_miscellaneous_page=(int(totall_miscellaneous)/5)+1

            self.total_miscellaneous_page= total_miscellaneous_page        

        if totall_article !=0:
            
            if(int(totall_article)%5==0):
                total_number_page=(int(totall_article)/5)
            else:
                total_article_page=(int(totall_article)/5)+1

            self.total_article_page= total_article_page        

        if totall_number !=0:
            
            if(int(totall_number)%5==0):
                total_number_page=(int(totall_number)/5)
            else:
                total_number_page=(int(totall_number)/5)+1

            self.total_number_page= total_number_page        

               
  
                


            
        super(total_error, self).save()






class total_close(models.Model):
    
    total_close = models.IntegerField (db_index=True,default=5)
    total_close_page = models.IntegerField (db_index=True,default=5)

  
  

    
   
    
    


    def save(self):
        totall_close=close.objects.count()
        self.total_close=totall_close
     
      


     
        if totall_close !=0:
            
            if(int(totall_close)%1==0):
                total_close_page=(int(totall_close)/1)
            else:
                total_close_page=(int(totall_close)/1)+1

            self.total_close_page= total_close_page

               
  
                


            
        super(total_close, self).save()






class mcq(models.Model):
    s= (
    ("2018", "2018"),   
    ("2019", "2019"),
    ("2020", "2020"),
    )
    year_now = models.CharField(max_length=10,
                          choices=s,
                          default="2018",blank=True,null=True,db_index=True)
    month_ch= (
    ("January", "January"),   
    ("February", "February"),
    ("March", "March"),
    ("April", "April"),
    ("May", "May"),
    ("June", "June"),
    ("July", "July"),
    ("August", "August"),   
    ("September", "September"),
    ("October", "October"),
    ("November", "November"),
    ("December", "December"),
    
    )
    month = models.CharField(max_length=15,
                  choices=month_ch,
                  default="December",blank=True,null=True,db_index=True)
    day = models.DateField(default=datetime.date.today,db_index=True)
    creation_time= models.TimeField(blank=True, null=True)
    question = models.TextField(default='')
    option_1 = models.CharField(max_length=250)
    option_2= models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200)
    option_4 = models.CharField(max_length=200,blank=True, null=True)
    option_5 = models.CharField(max_length=200,null=True,blank=True)
    ans = models.IntegerField (default=1)

    
    appointment  =models.BooleanField(default=False)    
    Art_Culture =models.BooleanField(default=False,db_index=True)    
    Awards_Honours =models.BooleanField(default=False,db_index=True)
    Business_Economy_Banking  =models.BooleanField(default=False,db_index=True)
    Defence =models.BooleanField(default=False,db_index=True)
    Environment =models.BooleanField(default=False,db_index=True)    

    Government_Schemes =models.BooleanField(default=False)
    International =models.BooleanField(default=False,db_index=True)
    medical =models.BooleanField(default=False,db_index=True)
    National = models.BooleanField(default=False,db_index=True)
    obituary =models.BooleanField(default=False)
    Persons_in_News =models.BooleanField(default=False,db_index=True)
    rank =models.BooleanField(default=False)
    Science_Techonlogy = models.BooleanField(default=False,db_index=True)
    
    Sports =models.BooleanField(default=False,db_index=True)
    
    State=models.BooleanField(default=False,db_index=True)
    static_gk =models.BooleanField(default=False)
    important_day =models.BooleanField(default=False)
    agreement =models.BooleanField(default=False)
    mythology =models.BooleanField(default=False)
    


    extra=models.TextField(default='',blank=True,null=True)
    new_id=models.CharField(max_length=300,default='',blank=True,null=True,db_index=True)
    

    class Meta:
        ordering = ["-day"]

        
   
    
    
    def __str__(self):
        return self.day.strftime('%d/%m/%Y') + '     '+ self.question

    def save(self):
        self.new_id= self.question +'===' +self.day.strftime('%d-%m-%Y')
        super(mcq, self).save()




      

class total_mcq(models.Model):
    
    total_mcq = models.IntegerField (db_index=True,default=3)
    total_mcq_page = models.IntegerField (db_index=True,default=3)
    
    Science_Techonlogy=models.IntegerField (db_index=True,default=0)
    
    National = models.IntegerField (db_index=True,default=0)
    
    State=models.IntegerField (db_index=True,default=0)
    
    International =models.IntegerField (db_index=True,default=0)
    
    Business_Economy_Banking  =models.IntegerField (db_index=True,default=0)
    
    Environment =models.IntegerField (db_index=True,default=0)
    
    Defence =models.IntegerField (db_index=True,default=0)
    
    Persons_in_News =models.IntegerField (db_index=True,default=0)
    
    Awards_Honours =models.IntegerField (db_index=True,default=0)
    
    Sports =models.IntegerField (db_index=True,default=0)
    
    Art_Culture =models.IntegerField (db_index=True,default=0)
    
    Government_Schemes =models.IntegerField (db_index=True,default=0)

    medical =models.IntegerField (db_index=True,default=0)
    rank=models.IntegerField (db_index=True,default=0)
    obituary=models.IntegerField (db_index=True,default=0)
    appointment=models.IntegerField (db_index=True,default=0)
    static_gk=models.IntegerField (db_index=True,default=0)
    
    

    
   
    
    


    def save(self):
        totall=mcq.objects.count()
        self.total_mcq= totall
        self.total_mcq_page=int(totall+300)/3

        total_st=mcq.objects.filter(Science_Techonlogy=True).count()
        total_n=mcq.objects.filter(National=True).count()
        total_State=mcq.objects.filter(State=True).count()
        total_International=mcq.objects.filter(International=True).count()
        total_Business_Economy_Banking=mcq.objects.filter(Business_Economy_Banking=True).count()
        total_Environment=mcq.objects.filter(Environment=True).count()
        total_Defence=mcq.objects.filter(Defence=True).count()
        total_Persons_in_News=mcq.objects.filter(Persons_in_News=True).count()
        total_Awards_Honours=mcq.objects.filter(Awards_Honours=True).count()
        total_Sports=mcq.objects.filter(Sports=True).count()
        total_Art_Culture=mcq.objects.filter(Art_Culture=True).count()
        total_Government_Schemes=mcq.objects.filter(Government_Schemes=True).count()
        total_medical=mcq.objects.filter(medical=True).count()
        total_rank=mcq.objects.filter(rank=True).count()
        total_obituary=mcq.objects.filter(obituary=True).count()
        total_appointment=mcq.objects.filter(appointment=True).count()
        total_static_gk =mcq.objects.filter(static_gk=True).count()
        if total_st !=0:
            
            if(int(total_st)%3==0):
                total_page_Science_Techonlogy=(int(total_st)/3)
            else:
                total_page_Science_Techonlogy=(int(total_st)/3)+1

            self.Science_Techonlogy= total_page_Science_Techonlogy        

                


        if total_n !=0:
            
            if(int(total_n)%3==0):
                total_page_National=(int(total_n)/3)
            else:
                total_page_National=(int(total_n)/3)+1
            self.National= total_page_National       

        if total_State !=0:
            
            if(int(total_State)%3==0):
                total_page_State=(int(total_State)/3)

            else:
                total_page_State=(int(total_State)/3)+1
            self.State= total_page_State     

        if total_International !=0:
            
            if(int(total_International)%3==0):
                total_page_International=(int(total_International)/3)
            else:
                total_page_International=(int(total_International)/3)+1
            self.International= total_page_International     

        if total_Business_Economy_Banking !=0:
            
            if(int(total_Business_Economy_Banking)%3==0):
                total_page_Business_Economy_Banking=(int(total_Business_Economy_Banking)/3)

            else:
                total_page_Business_Economy_Banking=(int(total_Business_Economy_Banking)/3)+1

            self.Business_Economy_Banking= total_page_Business_Economy_Banking    

        if total_Environment !=0:
            
            if(int(total_Environment)%3==0):
                total_page_Environment=(int(total_Environment)/3)
            else:
                total_page_Environment=(int(total_Environment)/3)+1
            self.Environment= total_page_Environment     

        if total_Defence !=0:
            
            if(int(total_Defence)%3==0):
                total_page_Defence=(int(total_Defence)/3)
            else:
                total_page_Defence=(int(total_Defence)/3)+1

            self.Defence= total_page_Defence     

        if total_Persons_in_News !=0:
            
            if(int(total_Persons_in_News)%3==0):
                total_page_Persons_in_News=(int(total_Persons_in_News)/3)
            else:
                total_page_Persons_in_News=(int(total_Persons_in_News)/3)+1

            self.Persons_in_News= total_page_Persons_in_News     

        if total_Awards_Honours !=0:
            
            if(int(total_Awards_Honours)%3==0):
                total_page_Awards_Honours=(int(total_Awards_Honours)/3)
            else:
                total_page_Awards_Honours=(int(total_Awards_Honours)/3)+1
            self.Awards_Honours= total_page_Awards_Honours    

        if total_Sports !=0:
            
            if(int(total_Sports)%3==0):
                total_page_Sports=(int(total_Sports)/3)
            else:
                total_page_Sports=(int(total_Sports)/3)+1

            self.Sports= total_page_Sports    

        if total_Art_Culture !=0:
            
            if(int(total_Art_Culture)%3==0):
                total_page_Art_Culture=(int(total_Art_Culture)/3)
            else:
                total_page_Art_Culture=(int(total_Art_Culture)/3)+1

            self.Art_Culture= total_page_Art_Culture     

        if total_Government_Schemes !=0:
            
            if(int(total_Government_Schemes)%3==0):
                total_page_Government_Schemes=(int(total_Government_Schemes)/3)
            else:
                total_page_Government_Schemes=(int(total_Government_Schemes)/3)+1
            self.Government_Schemes= total_page_Government_Schemes

        if total_medical !=0:
            
            if(int(total_medical)%3==0):
                total_page_medical=(int(total_medical)/3)
            else:
                total_page_medical=(int(total_medical)/3)+1

            self.medical= total_page_medical

        if total_rank !=0:
            
            if(int(total_rank)%3==0):
                total_page_rank=(int(total_rank)/3)
            else:
                total_page_rank=(int(total_rank)/3)+1
            self.rank= total_page_rank

        if total_obituary !=0:
            
            if(int(total_obituary)%3==0):
                total_page_obituary=(int(total_obituary)/3)
            else:
                total_page_obituary=(int(total_obituary)/3)+1
            self.obituary= total_page_obituary

        
        if total_appointment !=0:
            
            if(int(total_appointment)%3==0):
                total_page_appointment=(int(total_appointment)/3)
            else:
                total_page_appointment=(int(total_appointment)/3)+1
            self.appointment= total_page_appointment

        if total_static_gk !=0:
            
            if(int(total_static_gk)%3==0):
                total_page_static_gk=(int(total_static_gk)/3)
            else:
                total_page_static_gk=(int(total_static_gk)/3)+1
            self.static_gk= total_page_static_gk



        
        super(total_mcq, self).save()


class mcq_info_2018(models.Model):
    
    total_mcq = models.IntegerField (db_index=True,default=3)
    total_mcq_page = models.IntegerField (db_index=True,default=3)
    
    month_list = models.TextField(default='',null=True,blank=True)

    January = models.TextField(default='',null=True,blank=True)
    February = models.TextField(default='',null=True,blank=True)
    March = models.TextField(default='',null=True,blank=True)
    April = models.TextField(default='',null=True,blank=True)
    May = models.TextField(default='',null=True,blank=True)
    June = models.TextField(default='',null=True,blank=True)
    July = models.TextField(default='',null=True,blank=True)
    August = models.TextField(default='',null=True,blank=True)
    September = models.TextField(default='',null=True,blank=True)
    October = models.TextField(default='',null=True,blank=True)
    November = models.TextField(default='',null=True,blank=True)
    December = models.TextField(default='',null=True,blank=True)

    January_page = models.CharField(max_length=5,blank=True, null=True)
    February_page =models.CharField(max_length=5,blank=True, null=True)
    March_page = models.CharField(max_length=5,blank=True, null=True)
    April_page =models.CharField(max_length=5,blank=True, null=True)
    May_page =models.CharField(max_length=5,blank=True, null=True)
    June_page = models.CharField(max_length=5,blank=True, null=True)
    July_page = models.CharField(max_length=5,blank=True, null=True)
    August_page = models.CharField(max_length=5,blank=True, null=True)
    September_page = models.CharField(max_length=5,blank=True, null=True)
    October_page = models.CharField(max_length=5,blank=True, null=True)
    November_page = models.CharField(max_length=5,blank=True, null=True)
    December_page =models.CharField(max_length=5,blank=True, null=True)

        

    
   
    
    


    def save(self):
        totall=mcq.objects.count()
        self.total_mcq= totall
        self.total_mcq_page=int(totall+300)/3
        jan=1
        feb=2
        mar=3
        apr=4
        may=5
        jun=6
        jul=7
        aug=8
        sep=9
        oct=10
        nov=11
        dec=12
        sort_list=[]

        list_month=(mcq.objects.values_list('month',flat=True).filter(year_now='2018').order_by('month').distinct('month'))
        print(str(list_month))
        month_str=''# month_str :-this string is unnecessary stilli didnt delete it
        
        month_real=''
        month_real=''
        for  val in (list_month):
            
            if month_str == '':
                month_real=str(val)
                month_str=str(val)
                
                
            else:
                month_real=str(val)
                #print(month_real)
                month_str=month_str+" "+str(val)

            list_date=(mcq.objects.values_list('day',flat=True).filter(month=month_real,year_now='2018').order_by('day').distinct('day'))
            
            date_str=''
            count_date=0
            for e in list_date:
                if date_str == '':
                    date_str=str(e)
                    if(month_real =='January'):     
                        date_str =date_str.replace('2018-01-', '')
                        date_str=date_str +' Jan, 2018'
                    elif(month_real == 'February'):
                        date_str =date_str.replace('2018-02-', '')
                        date_str=date_str +' Feb, 2018'
                    elif(month_real =='March'):
                        date_str =date_str.replace('2018-03-', '')
                        date_str=date_str +' Mar, 2018'
                    elif(month_real =='April'):
                        date_str =date_str.replace('2018-04-', '')
                        date_str=date_str +' Apr, 2018'
                    elif(month_real =='May'):
                        date_str =date_str.replace('2018-05-', '')
                        date_str=date_str +' May, 2018'
                    elif(month_real =='June'):
                        date_str =date_str.replace('2018-06-', '')
                        date_str=date_str +' Jun, 2018'
                    elif(month_real =='July'):
                        date_str =date_str.replace('2018-07-', '')
                        date_str=date_str +' Jul, 2018'
                    elif(month_real =='August'):
                        date_str =date_str.replace('2018-08-', '')
                        date_str=date_str +' Aug, 2018'
                    elif(month_real =='September'):
                        date_str =date_str.replace('2018-09-', '')
                        date_str=date_str +' Sept, 2018'
                    elif(month_real =='October'):
                        date_str =date_str.replace('2018-10-', '')
                        date_str=date_str +' Oct, 2018'
                    elif(month_real =='November'):
                        date_str =date_str.replace('2018-11-', '')
                        date_str=date_str +' Nov, 2018'
                    elif(month_real =='December'):
                        date_str =date_str.replace('2018-12-', '')
                        date_str=date_str +' Dec, 2018'
                else:
                    date_str_replace=str(e)
                    
                    if(month_real =='January'):     
                        date_str_replace =date_str_replace.replace('2018-01-', '')
                        date_str_replace=date_str_replace +' Jan, 2018'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real == 'February'):
                        date_str_replace =date_str_replace.replace('2018-02-', '')
                        date_str_replace=date_str_replace +' Feb, 2018'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='March'):
                        date_str_replace =date_str_replace.replace('2018-03-', '')
                        date_str_replace=date_str_replace +' Mar, 2018'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='April'):
                        date_str_replace =date_str_replace.replace('2018-04-', '')
                        date_str_replace=date_str_replace +' Apr, 2018'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='May'):
                        date_str_replace =date_str_replace.replace('2018-05-', '')
                        date_str_replace=date_str_replace +' May, 2018'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='June'):
                        date_str_replace =date_str_replace.replace('2018-06-', '')
                        date_str_replace=date_str_replace +' Jun, 2018'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='July'):
                        date_str_replace =date_str_replace.replace('2018-07-', '')
                        date_str_replace=date_str_replace +' Jul, 2018'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='August'):
                        date_str_replace =date_str_replace.replace('2018-08-', '')
                        date_str_replace=date_str_replace +' Aug, 2018'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='September'):
                        date_str_replace =date_str_replace.replace('2018-09-', '')
                        date_str_replace=date_str_replace +' Sep, 2018'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='October'):
                        date_str_replace =date_str_replace.replace('2018-10-', '')
                        date_str_replace=date_str_replace +' Oct, 2018'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='November'):
                        date_str_replace =date_str_replace.replace('2018-11-', '')
                        date_str_replace=date_str_replace +' Nov, 2018'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='December'):
                        date_str_replace =date_str_replace.replace('2018-12-', '')
                        date_str_replace=date_str_replace +' Dec, 2018'
                        date_str=date_str+"///"+date_str_replace
                count_date=count_date+1
            print(count_date)

            print('m='+month_real)
            if(month_real =='January'):
                sort_list.append(1)
                
                self.January=date_str
                self.January_page=str(count_date)
            elif(month_real == 'February'):
                sort_list.append(2)
                self.February=date_str
                self.February_page=str(count_date)
            elif(month_real =='March'):
                sort_list.append(3)
                self.March=date_str
                self.March_page=str(count_date)
            elif(month_real =='April'):
                sort_list.append(4)
                self.April=date_str
                self.April_page=str(count_date)
            elif(month_real =='May'):
                sort_list.append(5)
                self.May=date_str
                self.May_page=str(count_date)
            elif(month_real =='June'):
                sort_list.append(6)
                self.June=date_str
                self.June_page=str(count_date)
            elif(month_real =='July'):
                sort_list.append(7)
                self.July=date_str
                self.July_page=str(count_date)
            elif(month_real =='August'):
                sort_list.append(8)
                self.August=date_str
                self.August_page=str(count_date)
            elif(month_real =='September'):
                sort_list.append(9)
                self.September=date_str
                self.September_page=str(count_date)
            elif(month_real =='October'):
                sort_list.append(10)
                self.October=date_str
                self.October_page=str(count_date)
            elif(month_real =='November'):
                sort_list.append(11)
                self.November=date_str
                self.November_page=str(count_date)
            elif(month_real =='December'):
                sort_list.append(12)
                self.December=date_str
                self.December_page=str(count_date)
            #print(val.values())

            #print(date_str)
            

            '''for e in (mcq.objects.values_list('day',flat=True).filter(month=month_real).order_by().distinct('day')):
                print(e.day)
            for val_date in enumerate(list_date):
                if date_str == '':
                    date_str=(''.join(val_date.values()))
                else:
                    date_str=date_str+" "+(''.join(val_date.values()))

            print(date_str)'''
                
        sort_list = [int(x) for x in sort_list]
        sort_list.sort()
        print(sort_list)
        month_list_new=[]
        final_month_list=''
        for  val in (sort_list):
            if val==1:
                month_list_new.append('January')
            elif val==2:
                month_list_new.append('February')
            elif val==3:
                month_list_new.append('March')
            elif val==4:
                month_list_new.append('April')
            elif val==5:
                month_list_new.append('May')
            elif val==6:
                month_list_new.append('June')
            elif val==7:
                month_list_new.append('July')
            elif val==8:
                month_list_new.append('August')
            elif val==9:
                month_list_new.append('September')
            elif val==10:
                month_list_new.append('October')
            elif val==11:
                month_list_new.append('November')
            elif val==12:
                month_list_new.append('December')

        for  val in (month_list_new):
            
            if final_month_list == '':
                final_month_list=str(val)
            else:
                final_month_list=final_month_list+" "+str(val)
                
        self.month_list= final_month_list    
        #print(month_str)
        #print(list_date)
        

                
                


                

        
        super(mcq_info_2018, self).save()



class mcq_info_2019(models.Model):
    
    total_mcq = models.IntegerField (db_index=True,default=3)
    total_mcq_page = models.IntegerField (db_index=True,default=3)
    
    month_list = models.TextField(default='',null=True,blank=True)

    January = models.TextField(default='',null=True,blank=True)
    February = models.TextField(default='',null=True,blank=True)
    March = models.TextField(default='',null=True,blank=True)
    April = models.TextField(default='',null=True,blank=True)
    May = models.TextField(default='',null=True,blank=True)
    June = models.TextField(default='',null=True,blank=True)
    July = models.TextField(default='',null=True,blank=True)
    August = models.TextField(default='',null=True,blank=True)
    September = models.TextField(default='',null=True,blank=True)
    October = models.TextField(default='',null=True,blank=True)
    November = models.TextField(default='',null=True,blank=True)
    December = models.TextField(default='',null=True,blank=True)

    January_page = models.CharField(max_length=5,blank=True, null=True)
    February_page =models.CharField(max_length=5,blank=True, null=True)
    March_page = models.CharField(max_length=5,blank=True, null=True)
    April_page =models.CharField(max_length=5,blank=True, null=True)
    May_page =models.CharField(max_length=5,blank=True, null=True)
    June_page = models.CharField(max_length=5,blank=True, null=True)
    July_page = models.CharField(max_length=5,blank=True, null=True)
    August_page = models.CharField(max_length=5,blank=True, null=True)
    September_page = models.CharField(max_length=5,blank=True, null=True)
    October_page = models.CharField(max_length=5,blank=True, null=True)
    November_page = models.CharField(max_length=5,blank=True, null=True)
    December_page =models.CharField(max_length=5,blank=True, null=True)

        

    
   
    
    


    def save(self):
        totall=mcq.objects.count()
        self.total_mcq= totall
        self.total_mcq_page=int(totall+300)/3
        jan=1
        feb=2
        mar=3
        apr=4
        may=5
        jun=6
        jul=7
        aug=8
        sep=9
        oct=10
        nov=11
        dec=12
        sort_list=[]

        list_month=(mcq.objects.values_list('month',flat=True).filter(year_now='2019').order_by('month').distinct('month'))
      
        month_str=''# month_str :-this string is unnecessary stilli didnt delete it
        
        month_real=''
        month_real=''
        for  val in (list_month):
            
            if month_str == '':
                month_real=str(val)
                month_str=str(val)
                
                
            else:
                month_real=str(val)
                #print(month_real)
                month_str=month_str+" "+str(val)

            list_date=(mcq.objects.values_list('day',flat=True).filter(month=month_real,year_now='2019').order_by('day').distinct('day'))
            
            date_str=''
            count_date=0
            for e in list_date:
                if date_str == '':
                    date_str=str(e)
                    if(month_real =='January'):     
                        date_str =date_str.replace('2019-01-', '')
                        date_str=date_str +' Jan, 2019'
                    elif(month_real == 'February'):
                        date_str =date_str.replace('2019-02-', '')
                        date_str=date_str +' Feb, 2019'
                    elif(month_real =='March'):
                        date_str =date_str.replace('2019-03-', '')
                        date_str=date_str +' Mar, 2019'
                    elif(month_real =='April'):
                        date_str =date_str.replace('2019-04-', '')
                        date_str=date_str +' Apr, 2019'
                    elif(month_real =='May'):
                        date_str =date_str.replace('2019-05-', '')
                        date_str=date_str +' May, 2019'
                    elif(month_real =='June'):
                        date_str =date_str.replace('2019-06-', '')
                        date_str=date_str +' Jun, 2019'
                    elif(month_real =='July'):
                        date_str =date_str.replace('2019-07-', '')
                        date_str=date_str +' Jul, 2019'
                    elif(month_real =='August'):
                        date_str =date_str.replace('2019-08-', '')
                        date_str=date_str +' Aug, 2019'
                    elif(month_real =='September'):
                        date_str =date_str.replace('2019-09-', '')
                        date_str=date_str +' Sept, 2019'
                    elif(month_real =='October'):
                        date_str =date_str.replace('2019-10-', '')
                        date_str=date_str +' Oct, 2019'
                    elif(month_real =='November'):
                        date_str =date_str.replace('2019-11-', '')
                        date_str=date_str +' Nov, 2019'
                    elif(month_real =='December'):
                        date_str =date_str.replace('2019-12-', '')
                        date_str=date_str +' Dec, 2019'
                else:
                    date_str_replace=str(e)
                    
                    if(month_real =='January'):     
                        date_str_replace =date_str_replace.replace('2019-01-', '')
                        date_str_replace=date_str_replace +' Jan, 2019'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real == 'February'):
                        date_str_replace =date_str_replace.replace('2019-02-', '')
                        date_str_replace=date_str_replace +' Feb, 2019'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='March'):
                        date_str_replace =date_str_replace.replace('2019-03-', '')
                        date_str_replace=date_str_replace +' Mar, 2019'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='April'):
                        date_str_replace =date_str_replace.replace('2019-04-', '')
                        date_str_replace=date_str_replace +' Apr, 2019'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='May'):
                        date_str_replace =date_str_replace.replace('2019-05-', '')
                        date_str_replace=date_str_replace +' May, 2019'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='June'):
                        date_str_replace =date_str_replace.replace('2019-06-', '')
                        date_str_replace=date_str_replace +' Jun, 2019'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='July'):
                        date_str_replace =date_str_replace.replace('2019-07-', '')
                        date_str_replace=date_str_replace +' Jul, 2019'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='August'):
                        date_str_replace =date_str_replace.replace('2019-08-', '')
                        date_str_replace=date_str_replace +' Aug, 2019'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='September'):
                        date_str_replace =date_str_replace.replace('2019-09-', '')
                        date_str_replace=date_str_replace +' Sep, 2019'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='October'):
                        date_str_replace =date_str_replace.replace('2019-10-', '')
                        date_str_replace=date_str_replace +' Oct, 2019'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='November'):
                        date_str_replace =date_str_replace.replace('2019-11-', '')
                        date_str_replace=date_str_replace +' Nov, 2019'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='December'):
                        date_str_replace =date_str_replace.replace('2019-12-', '')
                        date_str_replace=date_str_replace +' Dec, 2019'
                        date_str=date_str+"///"+date_str_replace
                count_date=count_date+1
            print(count_date)

            print('m='+month_real)
            if(month_real =='January'):
                sort_list.append(1)
                
                self.January=date_str
                self.January_page=str(count_date)
            elif(month_real == 'February'):
                sort_list.append(2)
                self.February=date_str
                self.February_page=str(count_date)
            elif(month_real =='March'):
                sort_list.append(3)
                self.March=date_str
                self.March_page=str(count_date)
            elif(month_real =='April'):
                sort_list.append(4)
                self.April=date_str
                self.April_page=str(count_date)
            elif(month_real =='May'):
                sort_list.append(5)
                self.May=date_str
                self.May_page=str(count_date)
            elif(month_real =='June'):
                sort_list.append(6)
                self.June=date_str
                self.June_page=str(count_date)
            elif(month_real =='July'):
                sort_list.append(7)
                self.July=date_str
                self.July_page=str(count_date)
            elif(month_real =='August'):
                sort_list.append(8)
                self.August=date_str
                self.August_page=str(count_date)
            elif(month_real =='September'):
                sort_list.append(9)
                self.September=date_str
                self.September_page=str(count_date)
            elif(month_real =='October'):
                sort_list.append(10)
                self.October=date_str
                self.October_page=str(count_date)
            elif(month_real =='November'):
                sort_list.append(11)
                self.November=date_str
                self.November_page=str(count_date)
            elif(month_real =='December'):
                sort_list.append(12)
                self.December=date_str
                self.December_page=str(count_date)
            #print(val.values())

            #print(date_str)
            

            '''for e in (mcq.objects.values_list('day',flat=True).filter(month=month_real).order_by().distinct('day')):
                print(e.day)
            for val_date in enumerate(list_date):
                if date_str == '':
                    date_str=(''.join(val_date.values()))
                else:
                    date_str=date_str+" "+(''.join(val_date.values()))

            print(date_str)'''
                
        sort_list = [int(x) for x in sort_list]
        sort_list.sort()
        print(sort_list)
        month_list_new=[]
        final_month_list=''
        for  val in (sort_list):
            if val==1:
                month_list_new.append('January')
            elif val==2:
                month_list_new.append('February')
            elif val==3:
                month_list_new.append('March')
            elif val==4:
                month_list_new.append('April')
            elif val==5:
                month_list_new.append('May')
            elif val==6:
                month_list_new.append('June')
            elif val==7:
                month_list_new.append('July')
            elif val==8:
                month_list_new.append('August')
            elif val==9:
                month_list_new.append('September')
            elif val==10:
                month_list_new.append('October')
            elif val==11:
                month_list_new.append('November')
            elif val==12:
                month_list_new.append('December')

        for  val in (month_list_new):
            
            if final_month_list == '':
                final_month_list=str(val)
            else:
                final_month_list=final_month_list+" "+str(val)
                
        self.month_list= final_month_list    
        #print(month_str)
        #print(list_date)
        

                
                


                

        
        super(mcq_info_2019, self).save()

class mcq_info_2020(models.Model):
    
    total_mcq = models.IntegerField (db_index=True,default=3)
    total_mcq_page = models.IntegerField (db_index=True,default=3)
    
    month_list = models.TextField(default='',null=True,blank=True)

    January = models.TextField(default='',null=True,blank=True)
    February = models.TextField(default='',null=True,blank=True)
    March = models.TextField(default='',null=True,blank=True)
    April = models.TextField(default='',null=True,blank=True)
    May = models.TextField(default='',null=True,blank=True)
    June = models.TextField(default='',null=True,blank=True)
    July = models.TextField(default='',null=True,blank=True)
    August = models.TextField(default='',null=True,blank=True)
    September = models.TextField(default='',null=True,blank=True)
    October = models.TextField(default='',null=True,blank=True)
    November = models.TextField(default='',null=True,blank=True)
    December = models.TextField(default='',null=True,blank=True)

    January_page = models.CharField(max_length=5,blank=True, null=True)
    February_page =models.CharField(max_length=5,blank=True, null=True)
    March_page = models.CharField(max_length=5,blank=True, null=True)
    April_page =models.CharField(max_length=5,blank=True, null=True)
    May_page =models.CharField(max_length=5,blank=True, null=True)
    June_page = models.CharField(max_length=5,blank=True, null=True)
    July_page = models.CharField(max_length=5,blank=True, null=True)
    August_page = models.CharField(max_length=5,blank=True, null=True)
    September_page = models.CharField(max_length=5,blank=True, null=True)
    October_page = models.CharField(max_length=5,blank=True, null=True)
    November_page = models.CharField(max_length=5,blank=True, null=True)
    December_page =models.CharField(max_length=5,blank=True, null=True)

        

    
   
    
    


    def save(self):
        totall=mcq.objects.count()
        self.total_mcq= totall
        self.total_mcq_page=int(totall+300)/3
        jan=1
        feb=2
        mar=3
        apr=4
        may=5
        jun=6
        jul=7
        aug=8
        sep=9
        oct=10
        nov=11
        dec=12
        sort_list=[]

        list_month=(mcq.objects.values_list('month',flat=True).filter(year_now='2020').order_by('month').distinct('month'))
        print(str(list_month))
        month_str=''# month_str :-this string is unnecessary stilli didnt delete it
        
        month_real=''
        month_real=''
        for  val in (list_month):
            
            if month_str == '':
                month_real=str(val)
                month_str=str(val)
                
                
            else:
                month_real=str(val)
                #print(month_real)
                month_str=month_str+" "+str(val)

            list_date=(mcq.objects.values_list('day',flat=True).filter(month=month_real,year_now='2020').order_by('day').distinct('day'))
            
            date_str=''
            count_date=0
            for e in list_date:
                if date_str == '':
                    date_str=str(e)
                    if(month_real =='January'):     
                        date_str =date_str.replace('2020-01-', '')
                        date_str=date_str +' Jan, 2020'
                    elif(month_real == 'February'):
                        date_str =date_str.replace('2020-02-', '')
                        date_str=date_str +' Feb, 2020'
                    elif(month_real =='March'):
                        date_str =date_str.replace('2020-03-', '')
                        date_str=date_str +' Mar, 2020'
                    elif(month_real =='April'):
                        date_str =date_str.replace('2020-04-', '')
                        date_str=date_str +' Apr, 2020'
                    elif(month_real =='May'):
                        date_str =date_str.replace('2020-05-', '')
                        date_str=date_str +' May, 2020'
                    elif(month_real =='June'):
                        date_str =date_str.replace('2020-06-', '')
                        date_str=date_str +' Jun, 2020'
                    elif(month_real =='July'):
                        date_str =date_str.replace('2020-07-', '')
                        date_str=date_str +' Jul, 2020'
                    elif(month_real =='August'):
                        date_str =date_str.replace('2020-08-', '')
                        date_str=date_str +' Aug, 2020'
                    elif(month_real =='September'):
                        date_str =date_str.replace('2020-09-', '')
                        date_str=date_str +' Sept, 2020'
                    elif(month_real =='October'):
                        date_str =date_str.replace('2020-10-', '')
                        date_str=date_str +' Oct, 2020'
                    elif(month_real =='November'):
                        date_str =date_str.replace('2020-11-', '')
                        date_str=date_str +' Nov, 2020'
                    elif(month_real =='December'):
                        date_str =date_str.replace('2020-12-', '')
                        date_str=date_str +' Dec, 2020'
                else:
                    date_str_replace=str(e)
                    
                    if(month_real =='January'):     
                        date_str_replace =date_str_replace.replace('2020-01-', '')
                        date_str_replace=date_str_replace +' Jan, 2020'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real == 'February'):
                        date_str_replace =date_str_replace.replace('2020-02-', '')
                        date_str_replace=date_str_replace +' Feb, 2020'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='March'):
                        date_str_replace =date_str_replace.replace('2020-03-', '')
                        date_str_replace=date_str_replace +' Mar, 2020'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='April'):
                        date_str_replace =date_str_replace.replace('2020-04-', '')
                        date_str_replace=date_str_replace +' Apr, 2020'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='May'):
                        date_str_replace =date_str_replace.replace('2020-05-', '')
                        date_str_replace=date_str_replace +' May, 2020'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='June'):
                        date_str_replace =date_str_replace.replace('2020-06-', '')
                        date_str_replace=date_str_replace +' Jun, 2020'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='July'):
                        date_str_replace =date_str_replace.replace('2020-07-', '')
                        date_str_replace=date_str_replace +' Jul, 2020'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='August'):
                        date_str_replace =date_str_replace.replace('2020-08-', '')
                        date_str_replace=date_str_replace +' Aug, 2020'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='September'):
                        date_str_replace =date_str_replace.replace('2020-09-', '')
                        date_str_replace=date_str_replace +' Sep, 2020'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='October'):
                        date_str_replace =date_str_replace.replace('2020-10-', '')
                        date_str_replace=date_str_replace +' Oct, 2020'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='November'):
                        date_str_replace =date_str_replace.replace('2020-11-', '')
                        date_str_replace=date_str_replace +' Nov, 2020'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='December'):
                        date_str_replace =date_str_replace.replace('2020-12-', '')
                        date_str_replace=date_str_replace +' Dec, 2020'
                        date_str=date_str+"///"+date_str_replace
                count_date=count_date+1
            print(count_date)

            print('m='+month_real)
            if(month_real =='January'):
                sort_list.append(1)
                
                self.January=date_str
                self.January_page=str(count_date)
            elif(month_real == 'February'):
                sort_list.append(2)
                self.February=date_str
                self.February_page=str(count_date)
            elif(month_real =='March'):
                sort_list.append(3)
                self.March=date_str
                self.March_page=str(count_date)
            elif(month_real =='April'):
                sort_list.append(4)
                self.April=date_str
                self.April_page=str(count_date)
            elif(month_real =='May'):
                sort_list.append(5)
                self.May=date_str
                self.May_page=str(count_date)
            elif(month_real =='June'):
                sort_list.append(6)
                self.June=date_str
                self.June_page=str(count_date)
            elif(month_real =='July'):
                sort_list.append(7)
                self.July=date_str
                self.July_page=str(count_date)
            elif(month_real =='August'):
                sort_list.append(8)
                self.August=date_str
                self.August_page=str(count_date)
            elif(month_real =='September'):
                sort_list.append(9)
                self.September=date_str
                self.September_page=str(count_date)
            elif(month_real =='October'):
                sort_list.append(10)
                self.October=date_str
                self.October_page=str(count_date)
            elif(month_real =='November'):
                sort_list.append(11)
                self.November=date_str
                self.November_page=str(count_date)
            elif(month_real =='December'):
                sort_list.append(12)
                self.December=date_str
                self.December_page=str(count_date)
            #print(val.values())

            #print(date_str)
            

            '''for e in (mcq.objects.values_list('day',flat=True).filter(month=month_real).order_by().distinct('day')):
                print(e.day)
            for val_date in enumerate(list_date):
                if date_str == '':
                    date_str=(''.join(val_date.values()))
                else:
                    date_str=date_str+" "+(''.join(val_date.values()))

            print(date_str)'''
                
        sort_list = [int(x) for x in sort_list]
        sort_list.sort()
        print(sort_list)
        month_list_new=[]
        final_month_list=''
        for  val in (sort_list):
            if val==1:
                month_list_new.append('January')
            elif val==2:
                month_list_new.append('February')
            elif val==3:
                month_list_new.append('March')
            elif val==4:
                month_list_new.append('April')
            elif val==5:
                month_list_new.append('May')
            elif val==6:
                month_list_new.append('June')
            elif val==7:
                month_list_new.append('July')
            elif val==8:
                month_list_new.append('August')
            elif val==9:
                month_list_new.append('September')
            elif val==10:
                month_list_new.append('October')
            elif val==11:
                month_list_new.append('November')
            elif val==12:
                month_list_new.append('December')

        for  val in (month_list_new):
            
            if final_month_list == '':
                final_month_list=str(val)
            else:
                final_month_list=final_month_list+" "+str(val)
                
        self.month_list= final_month_list    
        #print(month_str)
        #print(list_date)
        

                
                


                

        
        super(mcq_info_2020, self).save()



class current_affairs_info_2020(models.Model):
    
    total_current_affairs = models.IntegerField (db_index=True,default=3)
    total_current_affairs_page = models.IntegerField (db_index=True,default=3)
    
    month_list = models.TextField(default='',null=True,blank=True)

    January = models.TextField(default='',null=True,blank=True)
    February = models.TextField(default='',null=True,blank=True)
    March = models.TextField(default='',null=True,blank=True)
    April = models.TextField(default='',null=True,blank=True)
    May = models.TextField(default='',null=True,blank=True)
    June = models.TextField(default='',null=True,blank=True)
    July = models.TextField(default='',null=True,blank=True)
    August = models.TextField(default='',null=True,blank=True)
    September = models.TextField(default='',null=True,blank=True)
    October = models.TextField(default='',null=True,blank=True)
    November = models.TextField(default='',null=True,blank=True)
    December = models.TextField(default='',null=True,blank=True)

    January_page = models.CharField(max_length=5,blank=True, null=True)
    February_page =models.CharField(max_length=5,blank=True, null=True)
    March_page = models.CharField(max_length=5,blank=True, null=True)
    April_page =models.CharField(max_length=5,blank=True, null=True)
    May_page =models.CharField(max_length=5,blank=True, null=True)
    June_page = models.CharField(max_length=5,blank=True, null=True)
    July_page = models.CharField(max_length=5,blank=True, null=True)
    August_page = models.CharField(max_length=5,blank=True, null=True)
    September_page = models.CharField(max_length=5,blank=True, null=True)
    October_page = models.CharField(max_length=5,blank=True, null=True)
    November_page = models.CharField(max_length=5,blank=True, null=True)
    December_page =models.CharField(max_length=5,blank=True, null=True)

        

    
   
    
    


    def save(self):
        totall=current_affairs.objects.count()
        self.total_current_affairs= totall
        self.total_current_affairs_page=int(totall+300)/3
        jan=1
        feb=2
        mar=3
        apr=4
        may=5
        jun=6
        jul=7
        aug=8
        sep=9
        oct=10
        nov=11
        dec=12
        sort_list=[]

        list_month=(current_affairs.objects.values_list('month',flat=True).filter(year_now='2020').order_by('month').distinct('month'))
        print(str(list_month))
        month_str=''# month_str :-this string is unnecessary stilli didnt delete it
        
        month_real=''
        month_real=''
        for  val in (list_month):
            
            if month_str == '':
                month_real=str(val)
                month_str=str(val)
                
                
            else:
                month_real=str(val)
                #print(month_real)
                month_str=month_str+" "+str(val)

            list_date=(current_affairs.objects.values_list('day',flat=True).filter(month=month_real,year_now='2020').order_by('day').distinct('day'))
            
            date_str=''
            count_date=0
            for e in list_date:
                if date_str == '':
                    date_str=str(e)
                    if(month_real =='January'):     
                        date_str =date_str.replace('2020-01-', '')
                        date_str=date_str +' Jan, 2020'
                    elif(month_real == 'February'):
                        date_str =date_str.replace('2020-02-', '')
                        date_str=date_str +' Feb, 2020'
                    elif(month_real =='March'):
                        date_str =date_str.replace('2020-03-', '')
                        date_str=date_str +' Mar, 2020'
                    elif(month_real =='April'):
                        date_str =date_str.replace('2020-04-', '')
                        date_str=date_str +' Apr, 2020'
                    elif(month_real =='May'):
                        date_str =date_str.replace('2020-05-', '')
                        date_str=date_str +' May, 2020'
                    elif(month_real =='June'):
                        date_str =date_str.replace('2020-06-', '')
                        date_str=date_str +' Jun, 2020'
                    elif(month_real =='July'):
                        date_str =date_str.replace('2020-07-', '')
                        date_str=date_str +' Jul, 2020'
                    elif(month_real =='August'):
                        date_str =date_str.replace('2020-08-', '')
                        date_str=date_str +' Aug, 2020'
                    elif(month_real =='September'):
                        date_str =date_str.replace('2020-09-', '')
                        date_str=date_str +' Sept, 2020'
                    elif(month_real =='October'):
                        date_str =date_str.replace('2020-10-', '')
                        date_str=date_str +' Oct, 2020'
                    elif(month_real =='November'):
                        date_str =date_str.replace('2020-11-', '')
                        date_str=date_str +' Nov, 2020'
                    elif(month_real =='December'):
                        date_str =date_str.replace('2020-12-', '')
                        date_str=date_str +' Dec, 2020'
                else:
                    date_str_replace=str(e)
                    
                    if(month_real =='January'):     
                        date_str_replace =date_str_replace.replace('2020-01-', '')
                        date_str_replace=date_str_replace +' Jan, 2020'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real == 'February'):
                        date_str_replace =date_str_replace.replace('2020-02-', '')
                        date_str_replace=date_str_replace +' Feb, 2020'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='March'):
                        date_str_replace =date_str_replace.replace('2020-03-', '')
                        date_str_replace=date_str_replace +' Mar, 2020'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='April'):
                        date_str_replace =date_str_replace.replace('2020-04-', '')
                        date_str_replace=date_str_replace +' Apr, 2020'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='May'):
                        date_str_replace =date_str_replace.replace('2020-05-', '')
                        date_str_replace=date_str_replace +' May, 2020'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='June'):
                        date_str_replace =date_str_replace.replace('2020-06-', '')
                        date_str_replace=date_str_replace +' Jun, 2020'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='July'):
                        date_str_replace =date_str_replace.replace('2020-07-', '')
                        date_str_replace=date_str_replace +' Jul, 2020'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='August'):
                        date_str_replace =date_str_replace.replace('2020-08-', '')
                        date_str_replace=date_str_replace +' Aug, 2020'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='September'):
                        date_str_replace =date_str_replace.replace('2020-09-', '')
                        date_str_replace=date_str_replace +' Sep, 2020'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='October'):
                        date_str_replace =date_str_replace.replace('2020-10-', '')
                        date_str_replace=date_str_replace +' Oct, 2020'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='November'):
                        date_str_replace =date_str_replace.replace('2020-11-', '')
                        date_str_replace=date_str_replace +' Nov, 2020'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='December'):
                        date_str_replace =date_str_replace.replace('2020-12-', '')
                        date_str_replace=date_str_replace +' Dec, 2020'
                        date_str=date_str+"///"+date_str_replace
                count_date=count_date+1
            print(count_date)

            print('m='+month_real)
            if(month_real =='January'):
                sort_list.append(1)
                
                self.January=date_str
                self.January_page=str(count_date)
            elif(month_real == 'February'):
                sort_list.append(2)
                self.February=date_str
                self.February_page=str(count_date)
            elif(month_real =='March'):
                sort_list.append(3)
                self.March=date_str
                self.March_page=str(count_date)
            elif(month_real =='April'):
                sort_list.append(4)
                self.April=date_str
                self.April_page=str(count_date)
            elif(month_real =='May'):
                sort_list.append(5)
                self.May=date_str
                self.May_page=str(count_date)
            elif(month_real =='June'):
                sort_list.append(6)
                self.June=date_str
                self.June_page=str(count_date)
            elif(month_real =='July'):
                sort_list.append(7)
                self.July=date_str
                self.July_page=str(count_date)
            elif(month_real =='August'):
                sort_list.append(8)
                self.August=date_str
                self.August_page=str(count_date)
            elif(month_real =='September'):
                sort_list.append(9)
                self.September=date_str
                self.September_page=str(count_date)
            elif(month_real =='October'):
                sort_list.append(10)
                self.October=date_str
                self.October_page=str(count_date)
            elif(month_real =='November'):
                sort_list.append(11)
                self.November=date_str
                self.November_page=str(count_date)
            elif(month_real =='December'):
                sort_list.append(12)
                self.December=date_str
                self.December_page=str(count_date)
            #print(val.values())

            #print(date_str)
            

            '''for e in (current_affairs.objects.values_list('day',flat=True).filter(month=month_real).order_by().distinct('day')):
                print(e.day)
            for val_date in enumerate(list_date):
                if date_str == '':
                    date_str=(''.join(val_date.values()))
                else:
                    date_str=date_str+" "+(''.join(val_date.values()))

            print(date_str)'''
                
        sort_list = [int(x) for x in sort_list]
        sort_list.sort()
        print(sort_list)
        month_list_new=[]
        final_month_list=''
        for  val in (sort_list):
            if val==1:
                month_list_new.append('January')
            elif val==2:
                month_list_new.append('February')
            elif val==3:
                month_list_new.append('March')
            elif val==4:
                month_list_new.append('April')
            elif val==5:
                month_list_new.append('May')
            elif val==6:
                month_list_new.append('June')
            elif val==7:
                month_list_new.append('July')
            elif val==8:
                month_list_new.append('August')
            elif val==9:
                month_list_new.append('September')
            elif val==10:
                month_list_new.append('October')
            elif val==11:
                month_list_new.append('November')
            elif val==12:
                month_list_new.append('December')

        for  val in (month_list_new):
            
            if final_month_list == '':
                final_month_list=str(val)
            else:
                final_month_list=final_month_list+" "+str(val)
                
        self.month_list= final_month_list    
        #print(month_str)
        #print(list_date)
        

                
                


                

        
        super(current_affairs_info_2020, self).save()



class current_affairs_info_2019(models.Model):
    
    total_current_affairs = models.IntegerField (db_index=True,default=3)
    total_current_affairs_page = models.IntegerField (db_index=True,default=3)
    
    month_list = models.TextField(default='',null=True,blank=True)

    January = models.TextField(default='',null=True,blank=True)
    February = models.TextField(default='',null=True,blank=True)
    March = models.TextField(default='',null=True,blank=True)
    April = models.TextField(default='',null=True,blank=True)
    May = models.TextField(default='',null=True,blank=True)
    June = models.TextField(default='',null=True,blank=True)
    July = models.TextField(default='',null=True,blank=True)
    August = models.TextField(default='',null=True,blank=True)
    September = models.TextField(default='',null=True,blank=True)
    October = models.TextField(default='',null=True,blank=True)
    November = models.TextField(default='',null=True,blank=True)
    December = models.TextField(default='',null=True,blank=True)

    January_page = models.CharField(max_length=5,blank=True, null=True)
    February_page =models.CharField(max_length=5,blank=True, null=True)
    March_page = models.CharField(max_length=5,blank=True, null=True)
    April_page =models.CharField(max_length=5,blank=True, null=True)
    May_page =models.CharField(max_length=5,blank=True, null=True)
    June_page = models.CharField(max_length=5,blank=True, null=True)
    July_page = models.CharField(max_length=5,blank=True, null=True)
    August_page = models.CharField(max_length=5,blank=True, null=True)
    September_page = models.CharField(max_length=5,blank=True, null=True)
    October_page = models.CharField(max_length=5,blank=True, null=True)
    November_page = models.CharField(max_length=5,blank=True, null=True)
    December_page =models.CharField(max_length=5,blank=True, null=True)

        

    
   
    
    


    def save(self):
        totall=current_affairs.objects.count()
        self.total_current_affairs= totall
        self.total_current_affairs_page=int(totall+300)/3
        jan=1
        feb=2
        mar=3
        apr=4
        may=5
        jun=6
        jul=7
        aug=8
        sep=9
        oct=10
        nov=11
        dec=12
        sort_list=[]

        list_month=(current_affairs.objects.values_list('month',flat=True).filter(year_now='2019').order_by('month').distinct('month'))
        print(str(list_month))
        month_str=''# month_str :-this string is unnecessary stilli didnt delete it
        
        month_real=''
        month_real=''
        for  val in (list_month):
            
            if month_str == '':
                month_real=str(val)
                month_str=str(val)
                
                
            else:
                month_real=str(val)
                #print(month_real)
                month_str=month_str+" "+str(val)

            list_date=(current_affairs.objects.values_list('day',flat=True).filter(month=month_real,year_now='2019').order_by('day').distinct('day'))
            print(list_date)
            
            date_str=''
            count_date=0
            for e in list_date:
                if date_str == '':
                    date_str=str(e)
                    print(date_str)
                    print(month_real)
                    if(month_real =='January'):     
                        date_str =date_str.replace('2019-01-', '')
                        date_str=date_str +' Jan, 2019'
                    elif(month_real == 'February'):
                        date_str =date_str.replace('2019-02-', '')
                        date_str=date_str +' Feb, 2019'
                    elif(month_real =='March'):
                        date_str =date_str.replace('2019-03-', '')
                        date_str=date_str +' Mar, 2019'
                    elif(month_real =='April'):
                        date_str =date_str.replace('2019-04-', '')
                        date_str=date_str +' Apr, 2019'
                    elif(month_real =='May'):
                        date_str =date_str.replace('2019-05-', '')
                        date_str=date_str +' May, 2019'
                    elif(month_real =='June'):
                        date_str =date_str.replace('2019-06-', '')
                        date_str=date_str +' Jun, 2019'
                    elif(month_real =='July'):
                        date_str =date_str.replace('2019-07-', '')
                        date_str=date_str +' Jul, 2019'
                    elif(month_real =='August'):
                        date_str =date_str.replace('2019-08-', '')
                        date_str=date_str +' Aug, 2019'
                    elif(month_real =='September'):
                        date_str =date_str.replace('2019-09-', '')
                        date_str=date_str +' Sept, 2019'
                    elif(month_real =='October'):
                        date_str =date_str.replace('2019-10-', '')
                        date_str=date_str +' Oct, 2019'
                    elif(month_real =='November'):
                        date_str =date_str.replace('2019-11-', '')
                        date_str=date_str +' Nov, 2019'
                    elif(month_real =='December'):
                        date_str =date_str.replace('2019-12-', '')
                        date_str=date_str +' Dec, 2019'
                else:
                    date_str_replace=str(e)
                    
                    if(month_real =='January'):     
                        date_str_replace =date_str_replace.replace('2019-01-', '')
                        date_str_replace=date_str_replace +' Jan, 2019'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real == 'February'):
                        date_str_replace =date_str_replace.replace('2019-02-', '')
                        date_str_replace=date_str_replace +' Feb, 2019'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='March'):
                        date_str_replace =date_str_replace.replace('2019-03-', '')
                        date_str_replace=date_str_replace +' Mar, 2019'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='April'):
                        date_str_replace =date_str_replace.replace('2019-04-', '')
                        date_str_replace=date_str_replace +' Apr, 2019'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='May'):
                        date_str_replace =date_str_replace.replace('2019-05-', '')
                        date_str_replace=date_str_replace +' May, 2019'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='June'):
                        date_str_replace =date_str_replace.replace('2019-06-', '')
                        date_str_replace=date_str_replace +' Jun, 2019'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='July'):
                        date_str_replace =date_str_replace.replace('2019-07-', '')
                        date_str_replace=date_str_replace +' Jul, 2019'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='August'):
                        date_str_replace =date_str_replace.replace('2019-08-', '')
                        date_str_replace=date_str_replace +' Aug, 2019'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='September'):
                        date_str_replace =date_str_replace.replace('2019-09-', '')
                        date_str_replace=date_str_replace +' Sep, 2019'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='October'):
                        date_str_replace =date_str_replace.replace('2019-10-', '')
                        date_str_replace=date_str_replace +' Oct, 2019'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='November'):
                        date_str_replace =date_str_replace.replace('2019-11-', '')
                        date_str_replace=date_str_replace +' Nov, 2019'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='December'):
                        date_str_replace =date_str_replace.replace('2019-12-', '')
                        date_str_replace=date_str_replace +' Dec, 2019'
                        date_str=date_str+"///"+date_str_replace
                count_date=count_date+1
            print(count_date)

            print('m='+month_real)
            if(month_real =='January'):
                sort_list.append(1)
                
                self.January=date_str
                self.January_page=str(count_date)
            elif(month_real == 'February'):
                sort_list.append(2)
                self.February=date_str
                self.February_page=str(count_date)
            elif(month_real =='March'):
                sort_list.append(3)
                self.March=date_str
                self.March_page=str(count_date)
            elif(month_real =='April'):
                sort_list.append(4)
                self.April=date_str
                self.April_page=str(count_date)
            elif(month_real =='May'):
                sort_list.append(5)
                self.May=date_str
                self.May_page=str(count_date)
            elif(month_real =='June'):
                sort_list.append(6)
                self.June=date_str
                self.June_page=str(count_date)
            elif(month_real =='July'):
                sort_list.append(7)
                self.July=date_str
                self.July_page=str(count_date)
            elif(month_real =='August'):
                sort_list.append(8)
                self.August=date_str
                self.August_page=str(count_date)
            elif(month_real =='September'):
                sort_list.append(9)
                self.September=date_str
                self.September_page=str(count_date)
            elif(month_real =='October'):
                sort_list.append(10)
                self.October=date_str
                self.October_page=str(count_date)
            elif(month_real =='November'):
                sort_list.append(11)
                self.November=date_str
                self.November_page=str(count_date)
            elif(month_real =='December'):
                sort_list.append(12)
                self.December=date_str
                self.December_page=str(count_date)
            #print(val.values())

            #print(date_str)
            

            '''for e in (current_affairs.objects.values_list('day',flat=True).filter(month=month_real).order_by().distinct('day')):
                print(e.day)
            for val_date in enumerate(list_date):
                if date_str == '':
                    date_str=(''.join(val_date.values()))
                else:
                    date_str=date_str+" "+(''.join(val_date.values()))

            print(date_str)'''
                
        sort_list = [int(x) for x in sort_list]
        sort_list.sort()
        print(sort_list)
        month_list_new=[]
        final_month_list=''
        for  val in (sort_list):
            if val==1:
                month_list_new.append('January')
            elif val==2:
                month_list_new.append('February')
            elif val==3:
                month_list_new.append('March')
            elif val==4:
                month_list_new.append('April')
            elif val==5:
                month_list_new.append('May')
            elif val==6:
                month_list_new.append('June')
            elif val==7:
                month_list_new.append('July')
            elif val==8:
                month_list_new.append('August')
            elif val==9:
                month_list_new.append('September')
            elif val==10:
                month_list_new.append('October')
            elif val==11:
                month_list_new.append('November')
            elif val==12:
                month_list_new.append('December')

        for  val in (month_list_new):
            
            if final_month_list == '':
                final_month_list=str(val)
            else:
                final_month_list=final_month_list+" "+str(val)
                
        self.month_list= final_month_list    
        #print(month_str)
        #print(list_date)
        

                
                


                

        
        super(current_affairs_info_2019, self).save()


class current_affairs_info_2018(models.Model):
    
    total_current_affairs = models.IntegerField (db_index=True,default=3)
    total_current_affairs_page = models.IntegerField (db_index=True,default=3)
    
    month_list = models.TextField(default='',null=True,blank=True)

    January = models.TextField(default='',null=True,blank=True)
    February = models.TextField(default='',null=True,blank=True)
    March = models.TextField(default='',null=True,blank=True)
    April = models.TextField(default='',null=True,blank=True)
    May = models.TextField(default='',null=True,blank=True)
    June = models.TextField(default='',null=True,blank=True)
    July = models.TextField(default='',null=True,blank=True)
    August = models.TextField(default='',null=True,blank=True)
    September = models.TextField(default='',null=True,blank=True)
    October = models.TextField(default='',null=True,blank=True)
    November = models.TextField(default='',null=True,blank=True)
    December = models.TextField(default='',null=True,blank=True)

    January_page = models.CharField(max_length=5,blank=True, null=True)
    February_page =models.CharField(max_length=5,blank=True, null=True)
    March_page = models.CharField(max_length=5,blank=True, null=True)
    April_page =models.CharField(max_length=5,blank=True, null=True)
    May_page =models.CharField(max_length=5,blank=True, null=True)
    June_page = models.CharField(max_length=5,blank=True, null=True)
    July_page = models.CharField(max_length=5,blank=True, null=True)
    August_page = models.CharField(max_length=5,blank=True, null=True)
    September_page = models.CharField(max_length=5,blank=True, null=True)
    October_page = models.CharField(max_length=5,blank=True, null=True)
    November_page = models.CharField(max_length=5,blank=True, null=True)
    December_page =models.CharField(max_length=5,blank=True, null=True)

        

    
   
    
    


    def save(self):
        totall=current_affairs.objects.count()
        self.total_current_affairs= totall
        self.total_current_affairs_page=int(totall+300)/3
        jan=1
        feb=2
        mar=3
        apr=4
        may=5
        jun=6
        jul=7
        aug=8
        sep=9
        oct=10
        nov=11
        dec=12
        sort_list=[]

        list_month=(current_affairs.objects.values_list('month',flat=True).filter(year_now='2018').order_by('month').distinct('month'))
        print(str(list_month))
        month_str=''# month_str :-this string is unnecessary stilli didnt delete it
        
        month_real=''
        month_real=''
        for  val in (list_month):
            
            if month_str == '':
                month_real=str(val)
                month_str=str(val)
                
                
            else:
                month_real=str(val)
                print(month_real)
                month_str=month_str+" "+str(val)

            list_date=(current_affairs.objects.values_list('day',flat=True).filter(month=month_real,year_now='2018').order_by('day').distinct('day'))
            
            date_str=''
            count_date=0
            for e in list_date:
                if date_str == '':
                    date_str=str(e)
                    if(month_real =='January'):     
                        date_str =date_str.replace('2018-01-', '')
                        date_str=date_str +' Jan, 2018'
                    elif(month_real == 'February'):
                        date_str =date_str.replace('2018-02-', '')
                        date_str=date_str +' Feb, 2018'
                    elif(month_real =='March'):
                        date_str =date_str.replace('2018-03-', '')
                        date_str=date_str +' Mar, 2018'
                    elif(month_real =='April'):
                        date_str =date_str.replace('2018-04-', '')
                        date_str=date_str +' Apr, 2018'
                    elif(month_real =='May'):
                        date_str =date_str.replace('2018-05-', '')
                        date_str=date_str +' May, 2018'
                    elif(month_real =='June'):
                        date_str =date_str.replace('2018-06-', '')
                        date_str=date_str +' Jun, 2018'
                    elif(month_real =='July'):
                        date_str =date_str.replace('2018-07-', '')
                        date_str=date_str +' Jul, 2018'
                    elif(month_real =='August'):
                        date_str =date_str.replace('2018-08-', '')
                        date_str=date_str +' Aug, 2018'
                    elif(month_real =='September'):
                        date_str =date_str.replace('2018-09-', '')
                        date_str=date_str +' Sept, 2018'
                    elif(month_real =='October'):
                        date_str =date_str.replace('2018-10-', '')
                        date_str=date_str +' Oct, 2018'
                    elif(month_real =='November'):
                        date_str =date_str.replace('2018-11-', '')
                        date_str=date_str +' Nov, 2018'
                    elif(month_real =='December'):
                        date_str =date_str.replace('2018-12-', '')
                        date_str=date_str +' Dec, 2018'
                else:
                    date_str_replace=str(e)
                    
                    if(month_real =='January'):     
                        date_str_replace =date_str_replace.replace('2018-01-', '')
                        date_str_replace=date_str_replace +' Jan, 2018'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real == 'February'):
                        date_str_replace =date_str_replace.replace('2018-02-', '')
                        date_str_replace=date_str_replace +' Feb, 2018'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='March'):
                        date_str_replace =date_str_replace.replace('2018-03-', '')
                        date_str_replace=date_str_replace +' Mar, 2018'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='April'):
                        date_str_replace =date_str_replace.replace('2018-04-', '')
                        date_str_replace=date_str_replace +' Apr, 2018'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='May'):
                        date_str_replace =date_str_replace.replace('2018-05-', '')
                        date_str_replace=date_str_replace +' May, 2018'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='June'):
                        date_str_replace =date_str_replace.replace('2018-06-', '')
                        date_str_replace=date_str_replace +' Jun, 2018'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='July'):
                        date_str_replace =date_str_replace.replace('2018-07-', '')
                        date_str_replace=date_str_replace +' Jul, 2018'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='August'):
                        date_str_replace =date_str_replace.replace('2018-08-', '')
                        date_str_replace=date_str_replace +' Aug, 2018'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='September'):
                        date_str_replace =date_str_replace.replace('2018-09-', '')
                        date_str_replace=date_str_replace +' Sep, 2018'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='October'):
                        date_str_replace =date_str_replace.replace('2018-10-', '')
                        date_str_replace=date_str_replace +' Oct, 2018'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='November'):
                        date_str_replace =date_str_replace.replace('2018-11-', '')
                        date_str_replace=date_str_replace +' Nov, 2018'
                        date_str=date_str+"///"+date_str_replace
                    elif(month_real =='December'):
                        date_str_replace =date_str_replace.replace('2018-12-', '')
                        date_str_replace=date_str_replace +' Dec, 2018'
                        date_str=date_str+"///"+date_str_replace
                count_date=count_date+1
            print(count_date)

            print('m='+month_real)
            if(month_real =='January'):
                sort_list.append(1)
                
                self.January=date_str
                self.January_page=str(count_date)
            elif(month_real == 'February'):
                sort_list.append(2)
                self.February=date_str
                self.February_page=str(count_date)
            elif(month_real =='March'):
                sort_list.append(3)
                self.March=date_str
                self.March_page=str(count_date)
            elif(month_real =='April'):
                sort_list.append(4)
                self.April=date_str
                self.April_page=str(count_date)
            elif(month_real =='May'):
                sort_list.append(5)
                self.May=date_str
                self.May_page=str(count_date)
            elif(month_real =='June'):
                sort_list.append(6)
                self.June=date_str
                self.June_page=str(count_date)
            elif(month_real =='July'):
                sort_list.append(7)
                self.July=date_str
                self.July_page=str(count_date)
            elif(month_real =='August'):
                sort_list.append(8)
                self.August=date_str
                self.August_page=str(count_date)
            elif(month_real =='September'):
                sort_list.append(9)
                self.September=date_str
                self.September_page=str(count_date)
            elif(month_real =='October'):
                sort_list.append(10)
                self.October=date_str
                self.October_page=str(count_date)
            elif(month_real =='November'):
                sort_list.append(11)
                self.November=date_str
                self.November_page=str(count_date)
            elif(month_real =='December'):
                sort_list.append(12)
                self.December=date_str
                self.December_page=str(count_date)
            #print(val.values())

            #print(date_str)
            

            '''for e in (current_affairs.objects.values_list('day',flat=True).filter(month=month_real).order_by().distinct('day')):
                print(e.day)
            for val_date in enumerate(list_date):
                if date_str == '':
                    date_str=(''.join(val_date.values()))
                else:
                    date_str=date_str+" "+(''.join(val_date.values()))

            print(date_str)'''
                
        sort_list = [int(x) for x in sort_list]
        sort_list.sort()
        print(sort_list)
        month_list_new=[]
        final_month_list=''
        for  val in (sort_list):
            if val==1:
                month_list_new.append('January')
            elif val==2:
                month_list_new.append('February')
            elif val==3:
                month_list_new.append('March')
            elif val==4:
                month_list_new.append('April')
            elif val==5:
                month_list_new.append('May')
            elif val==6:
                month_list_new.append('June')
            elif val==7:
                month_list_new.append('July')
            elif val==8:
                month_list_new.append('August')
            elif val==9:
                month_list_new.append('September')
            elif val==10:
                month_list_new.append('October')
            elif val==11:
                month_list_new.append('November')
            elif val==12:
                month_list_new.append('December')

        for  val in (month_list_new):
            
            if final_month_list == '':
                final_month_list=str(val)
            else:
                final_month_list=final_month_list+" "+str(val)
                
        self.month_list= final_month_list    
        #print(month_str)
        #print(list_date)        
        super(current_affairs_info_2018, self).save()


class polity(models.Model):
    chapter= (
    ("1", "1"),   
    ("2", "2"),
    ("3", "3"),("4", "4"),("5", "5"),("6", "6"),("7", "7"),("8", "8"),("9", "9"),("10", "10"),("11", "11"),("12", "12"),("13", "13"),("14", "14"),("15", "15"),("16", "16"),
    ("17", "17"),("18", "18"),("19", "19"),("20", "20"),("21", "21"),("22", "22"),("23", "23"),("24", "24"),("25", "25"),("26", "26"),("27", "27"),("28", "28"),("29", "29"),("30", "30"),
    ("31", "31"),("32", "32"),("33", "33"),("34", "34"),("35", "35"),("36", "36"),("37", "37"),("38", "38"),("39", "39"),("40", "40"),("41", "41"),
    
    )
    chapter = models.CharField(max_length=10,
                          choices=chapter,
                          default="1",db_index=True)
    topic_ch= (
    ("question-answare", "question-answare"),
    
    )
    topic = models.CharField(max_length=18,
                  choices=topic_ch,
                  default="question-answare",blank=True,null=True,db_index=True)
    subtopic_ch= (
    ("mcq", "mcq"),
    
    )
    subtopic = models.CharField(max_length=20,
                  choices=subtopic_ch,
                  default="mcq",blank=True,null=True,db_index=True)
    subtopic_ch2= (
    ("more", "more"),
    
    )
    subtopic_2 = models.CharField(max_length=20,
                  choices=subtopic_ch2,
                  default="more",blank=True,null=True,db_index=True)
    day = models.DateField(default=datetime.date.today,db_index=True)
    creation_time= models.TimeField(blank=True, null=True)
    question = models.TextField(default='')
    option_1 = models.CharField(max_length=250)
    option_2= models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200)
    option_4 = models.CharField(max_length=200,blank=True, null=True)
    option_5 = models.CharField(max_length=200,null=True,blank=True)
    ans = models.IntegerField (default=1)

    year_exam = models.CharField(max_length=250,blank=True, null=True)
    


    extra=models.TextField(default='',blank=True,null=True)
    new_id=models.CharField(max_length=300,default='',blank=True,null=True,db_index=True)
    

    class Meta:
        ordering = ["-day"]
    
    
    def __str__(self):
        return self.day.strftime('%d/%m/%Y') + '     '+ self.question

    def save(self):
        self.new_id= self.question +'===' +self.day.strftime('%d-%m-%Y')
        super(polity, self).save()




      
class total_polity(models.Model):
    
    total_polity = models.IntegerField (db_index=True,default=3)
    total_polity_page = models.IntegerField (db_index=True,default=3)
    
    chapter_1=models.IntegerField (default=0)
    chapter_2=models.IntegerField (default=0)
    chapter_3=models.IntegerField (default=0)
    chapter_4=models.IntegerField (default=0)
    chapter_5=models.IntegerField (default=0)
    chapter_6=models.IntegerField (default=0)
    chapter_7=models.IntegerField (default=0)
    chapter_8=models.IntegerField (default=0)
    chapter_9=models.IntegerField (default=0)
    chapter_10=models.IntegerField (default=0)
    chapter_11=models.IntegerField (default=0)
    chapter_12=models.IntegerField (default=0)
    chapter_13=models.IntegerField (default=0)
    chapter_14=models.IntegerField (default=0)
    chapter_15=models.IntegerField (default=0)
    chapter_16=models.IntegerField (default=0)
    chapter_17=models.IntegerField (default=0)
    chapter_18=models.IntegerField (default=0)
    chapter_19=models.IntegerField (default=0)
    chapter_20=models.IntegerField (default=0)
    chapter_21=models.IntegerField (default=0)
    chapter_22=models.IntegerField (default=0)
    chapter_23=models.IntegerField (default=0)
    chapter_24=models.IntegerField (default=0)
    chapter_25=models.IntegerField (default=0)
    chapter_26=models.IntegerField (default=0)
    chapter_27=models.IntegerField (default=0)
    chapter_28=models.IntegerField (default=0)
    chapter_29=models.IntegerField (default=0)
    chapter_30=models.IntegerField (default=0)
    chapter_31=models.IntegerField (default=0)
    chapter_32=models.IntegerField (default=0)
    chapter_33=models.IntegerField (default=0)
    chapter_34=models.IntegerField (default=0)
    chapter_35=models.IntegerField (default=0)
    chapter_36=models.IntegerField (default=0)
    chapter_37=models.IntegerField (default=0)
    chapter_38=models.IntegerField (default=0)
    chapter_40=models.IntegerField (default=0)
    chapter_41=models.IntegerField (default=0)



    def save(self):
        totall=polity.objects.count()
        self.total_polity= totall
        self.total_polity_page=int(totall)/5

        
        for x in range(1,41):
            total=polity.objects.filter(chapter=str(x)).count()
            if total !=0:
                
                if(int(total)%5==0):
                    total_page=(int(total)/5)
                else:
                    total_page=(int(total)/5)+1
                y='chapter_'+ str(x)

                #self.chapter_1= total_page_1
                self.__dict__[y]=total_page


        
        super(total_polity, self).save()





class history(models.Model):
    chapter= (
    ("1", "1"),   
    ("2", "2"),
    ("3", "3"),("4", "4"),("5", "5"),("6", "6"),("7", "7"),("8", "8"),("9", "9"),("10", "10"),("11", "11"),("12", "12"),("13", "13"),("14", "14"),("15", "15"),("16", "16"),
    ("17", "17"),("18", "18"),("19", "19"),("20", "20"),("21", "21"),("22", "22"),("23", "23"),("24", "24"),("25", "25"),("26", "26"),("27", "27"),("28", "28"),("29", "29"),("30", "30"),
    ("31", "31"),("32", "32"),("33", "33"),("34", "34"),("35", "35"),("36", "36"),("37", "37"),("38", "38"),("39", "39"),("40", "40"),("41", "41"),
    
    )
    chapter = models.CharField(max_length=10,
                          choices=chapter,
                          default="1",db_index=True)
    topic_ch= (
    ("question-answare", "question-answare"),
    
    )
    topic = models.CharField(max_length=18,
                  choices=topic_ch,
                  default="question-answare",blank=True,null=True,db_index=True)
    subtopic_ch= (
    ("mcq", "mcq"),
    
    )
    subtopic = models.CharField(max_length=20,
                  choices=subtopic_ch,
                  default="mcq",blank=True,null=True,db_index=True)
    subtopic_ch2= (
    ("more", "more"),
    
    )
    subtopic_2 = models.CharField(max_length=20,
                  choices=subtopic_ch2,
                  default="more",blank=True,null=True,db_index=True)
    day = models.DateField(default=datetime.date.today,db_index=True)
    creation_time= models.TimeField(blank=True, null=True)
    question = models.TextField(default='')
    option_1 = models.CharField(max_length=250)
    option_2= models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200)
    option_4 = models.CharField(max_length=200,blank=True, null=True)
    option_5 = models.CharField(max_length=200,null=True,blank=True)
    ans = models.IntegerField (default=1)

    year_exam = models.CharField(max_length=250,blank=True, null=True)
    


    extra=models.TextField(default='',blank=True,null=True)
    new_id=models.CharField(max_length=300,default='',blank=True,null=True,db_index=True)
    

    class Meta:
        ordering = ["-day"]
    
    
    def __str__(self):
        return self.day.strftime('%d/%m/%Y') + '     '+ self.question

    def save(self):
        self.new_id= self.question +'===' +self.day.strftime('%d-%m-%Y')
        super(history, self).save()




      
class total_history(models.Model):
    
    total_history = models.IntegerField (db_index=True,default=3)
    total_history_page = models.IntegerField (db_index=True,default=3)
    
    chapter_1=models.IntegerField (default=0)
    chapter_2=models.IntegerField (default=0)
    chapter_3=models.IntegerField (default=0)
    chapter_4=models.IntegerField (default=0)
    chapter_5=models.IntegerField (default=0)
    chapter_6=models.IntegerField (default=0)
    chapter_7=models.IntegerField (default=0)
    chapter_8=models.IntegerField (default=0)
    chapter_9=models.IntegerField (default=0)
    chapter_10=models.IntegerField (default=0)
    chapter_11=models.IntegerField (default=0)
    chapter_12=models.IntegerField (default=0)
    chapter_13=models.IntegerField (default=0)
    chapter_14=models.IntegerField (default=0)
    chapter_15=models.IntegerField (default=0)
    chapter_16=models.IntegerField (default=0)
    chapter_17=models.IntegerField (default=0)
    chapter_18=models.IntegerField (default=0)
    chapter_19=models.IntegerField (default=0)
    chapter_20=models.IntegerField (default=0)
    chapter_21=models.IntegerField (default=0)
    chapter_22=models.IntegerField (default=0)
    chapter_23=models.IntegerField (default=0)
    chapter_24=models.IntegerField (default=0)
    chapter_25=models.IntegerField (default=0)
    chapter_26=models.IntegerField (default=0)
    chapter_27=models.IntegerField (default=0)
    chapter_28=models.IntegerField (default=0)
    chapter_29=models.IntegerField (default=0)
    chapter_30=models.IntegerField (default=0)
    chapter_31=models.IntegerField (default=0)
    chapter_32=models.IntegerField (default=0)
    chapter_33=models.IntegerField (default=0)
    chapter_34=models.IntegerField (default=0)
    chapter_35=models.IntegerField (default=0)
    chapter_36=models.IntegerField (default=0)
    chapter_37=models.IntegerField (default=0)
    chapter_38=models.IntegerField (default=0)
    chapter_40=models.IntegerField (default=0)
    chapter_41=models.IntegerField (default=0)



    def save(self):
        totall=history.objects.count()
        self.total_history= totall
        self.total_history_page=int(totall)/5

        
        for x in range(1,41):
            total=history.objects.filter(chapter=str(x)).count()
            if total !=0:
                
                if(int(total)%5==0):
                    total_page=(int(total)/5)
                else:
                    total_page=(int(total)/5)+1
                y='chapter_'+ str(x)

                #self.chapter_1= total_page_1
                self.__dict__[y]=total_page


        
        super(total_history, self).save()




class geography(models.Model):
    chapter= (
    ("1", "1"),   
    ("2", "2"),
    ("3", "3"),("4", "4"),("5", "5"),("6", "6"),("7", "7"),("8", "8"),("9", "9"),("10", "10"),("11", "11"),("12", "12"),("13", "13"),("14", "14"),("15", "15"),("16", "16"),
    ("17", "17"),("18", "18"),("19", "19"),("20", "20"),("21", "21"),("22", "22"),("23", "23"),("24", "24"),("25", "25"),("26", "26"),("27", "27"),("28", "28"),("29", "29"),("30", "30"),
    ("31", "31"),("32", "32"),("33", "33"),("34", "34"),("35", "35"),("36", "36"),("37", "37"),("38", "38"),("39", "39"),("40", "40"),("41", "41"),
    
    )
    chapter = models.CharField(max_length=10,
                          choices=chapter,
                          default="1",db_index=True)
    topic_ch= (
    ("question-answare", "question-answare"),
    
    )
    topic = models.CharField(max_length=18,
                  choices=topic_ch,
                  default="question-answare",blank=True,null=True,db_index=True)
    subtopic_ch= (
    ("mcq", "mcq"),
    
    )
    subtopic = models.CharField(max_length=20,
                  choices=subtopic_ch,
                  default="mcq",blank=True,null=True,db_index=True)
    subtopic_ch2= (
    ("more", "more"),
    
    )
    subtopic_2 = models.CharField(max_length=20,
                  choices=subtopic_ch2,
                  default="more",blank=True,null=True,db_index=True)
    day = models.DateField(default=datetime.date.today,db_index=True)
    creation_time= models.TimeField(blank=True, null=True)
    question = models.TextField(default='')
    option_1 = models.CharField(max_length=250)
    option_2= models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200)
    option_4 = models.CharField(max_length=200,blank=True, null=True)
    option_5 = models.CharField(max_length=200,null=True,blank=True)
    ans = models.IntegerField (default=1)

    year_exam = models.CharField(max_length=250,blank=True, null=True)
    


    extra=models.TextField(default='',blank=True,null=True)
    new_id=models.CharField(max_length=300,default='',blank=True,null=True,db_index=True)
    

    class Meta:
        ordering = ["-day"]
    
    
    def __str__(self):
        return self.day.strftime('%d/%m/%Y') + '     '+ self.question

    def save(self):
        self.new_id= self.question +'===' +self.day.strftime('%d-%m-%Y')
        super(geography, self).save()




      
class total_geography(models.Model):
    
    total_geography = models.IntegerField (db_index=True,default=3)
    total_geography_page = models.IntegerField (db_index=True,default=3)
    
    chapter_1=models.IntegerField (default=0)
    chapter_2=models.IntegerField (default=0)
    chapter_3=models.IntegerField (default=0)
    chapter_4=models.IntegerField (default=0)
    chapter_5=models.IntegerField (default=0)
    chapter_6=models.IntegerField (default=0)
    chapter_7=models.IntegerField (default=0)
    chapter_8=models.IntegerField (default=0)
    chapter_9=models.IntegerField (default=0)
    chapter_10=models.IntegerField (default=0)
    chapter_11=models.IntegerField (default=0)
    chapter_12=models.IntegerField (default=0)
    chapter_13=models.IntegerField (default=0)
    chapter_14=models.IntegerField (default=0)
    chapter_15=models.IntegerField (default=0)
    chapter_16=models.IntegerField (default=0)
    chapter_17=models.IntegerField (default=0)
    chapter_18=models.IntegerField (default=0)
    chapter_19=models.IntegerField (default=0)
    chapter_20=models.IntegerField (default=0)
    chapter_21=models.IntegerField (default=0)
    chapter_22=models.IntegerField (default=0)
    chapter_23=models.IntegerField (default=0)
    chapter_24=models.IntegerField (default=0)
    chapter_25=models.IntegerField (default=0)
    chapter_26=models.IntegerField (default=0)
    chapter_27=models.IntegerField (default=0)
    chapter_28=models.IntegerField (default=0)
    chapter_29=models.IntegerField (default=0)
    chapter_30=models.IntegerField (default=0)
    chapter_31=models.IntegerField (default=0)
    chapter_32=models.IntegerField (default=0)
    chapter_33=models.IntegerField (default=0)
    chapter_34=models.IntegerField (default=0)
    chapter_35=models.IntegerField (default=0)
    chapter_36=models.IntegerField (default=0)
    chapter_37=models.IntegerField (default=0)
    chapter_38=models.IntegerField (default=0)
    chapter_40=models.IntegerField (default=0)
    chapter_41=models.IntegerField (default=0)



    def save(self):
        totall=geography.objects.count()
        self.total_geography= totall
        self.total_geography_page=int(totall)/5

        
        for x in range(1,41):
            total=geography.objects.filter(chapter=str(x)).count()
            if total !=0:
                
                if(int(total)%5==0):
                    total_page=(int(total)/5)
                else:
                    total_page=(int(total)/5)+1
                y='chapter_'+ str(x)

                #self.chapter_1= total_page_1
                self.__dict__[y]=total_page


        
        super(total_geography, self).save()



class economics(models.Model):
    chapter= (
    ("1", "1"),   
    ("2", "2"),
    ("3", "3"),("4", "4"),("5", "5"),("6", "6"),("7", "7"),("8", "8"),("9", "9"),("10", "10"),("11", "11"),("12", "12"),("13", "13"),("14", "14"),("15", "15"),("16", "16"),
    ("17", "17"),("18", "18"),("19", "19"),("20", "20"),("21", "21"),("22", "22"),("23", "23"),("24", "24"),("25", "25"),("26", "26"),("27", "27"),("28", "28"),("29", "29"),("30", "30"),
    ("31", "31"),("32", "32"),("33", "33"),("34", "34"),("35", "35"),("36", "36"),("37", "37"),("38", "38"),("39", "39"),("40", "40"),("41", "41"),
    
    )
    chapter = models.CharField(max_length=10,
                          choices=chapter,
                          default="1",db_index=True)
    topic_ch= (
    ("question-answare", "question-answare"),
    
    )
    topic = models.CharField(max_length=18,
                  choices=topic_ch,
                  default="question-answare",blank=True,null=True,db_index=True)
    subtopic_ch= (
    ("mcq", "mcq"),
    
    )
    subtopic = models.CharField(max_length=20,
                  choices=subtopic_ch,
                  default="mcq",blank=True,null=True,db_index=True)
    subtopic_ch2= (
    ("more", "more"),
    
    )
    subtopic_2 = models.CharField(max_length=20,
                  choices=subtopic_ch2,
                  default="more",blank=True,null=True,db_index=True)
    day = models.DateField(default=datetime.date.today,db_index=True)
    creation_time= models.TimeField(blank=True, null=True)
    question = models.TextField(default='')
    option_1 = models.CharField(max_length=250)
    option_2= models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200)
    option_4 = models.CharField(max_length=200,blank=True, null=True)
    option_5 = models.CharField(max_length=200,null=True,blank=True)
    ans = models.IntegerField (default=1)

    year_exam = models.CharField(max_length=250,blank=True, null=True)
    


    extra=models.TextField(default='',blank=True,null=True)
    new_id=models.CharField(max_length=300,default='',blank=True,null=True,db_index=True)
    

    class Meta:
        ordering = ["-day"]
    
    
    def __str__(self):
        return self.day.strftime('%d/%m/%Y') + '     '+ self.question

    def save(self):
        self.new_id= self.question +'===' +self.day.strftime('%d-%m-%Y')
        super(economics, self).save()




      
class total_economics(models.Model):
    
    total_economics = models.IntegerField (db_index=True,default=3)
    total_economics_page = models.IntegerField (db_index=True,default=3)
    
    chapter_1=models.IntegerField (default=0)
    chapter_2=models.IntegerField (default=0)
    chapter_3=models.IntegerField (default=0)
    chapter_4=models.IntegerField (default=0)
    chapter_5=models.IntegerField (default=0)
    chapter_6=models.IntegerField (default=0)
    chapter_7=models.IntegerField (default=0)
    chapter_8=models.IntegerField (default=0)
    chapter_9=models.IntegerField (default=0)
    chapter_10=models.IntegerField (default=0)
    chapter_11=models.IntegerField (default=0)
    chapter_12=models.IntegerField (default=0)
    chapter_13=models.IntegerField (default=0)
    chapter_14=models.IntegerField (default=0)
    chapter_15=models.IntegerField (default=0)
    chapter_16=models.IntegerField (default=0)
    chapter_17=models.IntegerField (default=0)
    chapter_18=models.IntegerField (default=0)
    chapter_19=models.IntegerField (default=0)
    chapter_20=models.IntegerField (default=0)
    chapter_21=models.IntegerField (default=0)
    chapter_22=models.IntegerField (default=0)
    chapter_23=models.IntegerField (default=0)
    chapter_24=models.IntegerField (default=0)
    chapter_25=models.IntegerField (default=0)
    chapter_26=models.IntegerField (default=0)
    chapter_27=models.IntegerField (default=0)
    chapter_28=models.IntegerField (default=0)
    chapter_29=models.IntegerField (default=0)
    chapter_30=models.IntegerField (default=0)
    chapter_31=models.IntegerField (default=0)
    chapter_32=models.IntegerField (default=0)
    chapter_33=models.IntegerField (default=0)
    chapter_34=models.IntegerField (default=0)
    chapter_35=models.IntegerField (default=0)
    chapter_36=models.IntegerField (default=0)
    chapter_37=models.IntegerField (default=0)
    chapter_38=models.IntegerField (default=0)
    chapter_40=models.IntegerField (default=0)
    chapter_41=models.IntegerField (default=0)



    def save(self):
        totall=economics.objects.count()
        self.total_economics= totall
        self.total_economics_page=int(totall)/5

        
        for x in range(1,41):
            total=economics.objects.filter(chapter=str(x)).count()
            if total !=0:
                
                if(int(total)%5==0):
                    total_page=(int(total)/5)
                else:
                    total_page=(int(total)/5)+1
                y='chapter_'+ str(x)

                #self.chapter_1= total_page_1
                self.__dict__[y]=total_page


        
        super(total_economics, self).save()

class physics(models.Model):
    chapter= (
    ("1", "1"),   
    ("2", "2"),
    ("3", "3"),("4", "4"),("5", "5"),("6", "6"),("7", "7"),("8", "8"),("9", "9"),("10", "10"),("11", "11"),("12", "12"),("13", "13"),("14", "14"),("15", "15"),("16", "16"),
    ("17", "17"),("18", "18"),("19", "19"),("20", "20"),("21", "21"),("22", "22"),("23", "23"),("24", "24"),("25", "25"),("26", "26"),("27", "27"),("28", "28"),("29", "29"),("30", "30"),
    ("31", "31"),("32", "32"),("33", "33"),("34", "34"),("35", "35"),("36", "36"),("37", "37"),("38", "38"),("39", "39"),("40", "40"),("41", "41"),
    
    )
    chapter = models.CharField(max_length=10,
                          choices=chapter,
                          default="1",db_index=True)
    topic_ch= (
    ("question-answare", "question-answare"),
    
    )
    topic = models.CharField(max_length=18,
                  choices=topic_ch,
                  default="question-answare",blank=True,null=True,db_index=True)
    subtopic_ch= (
    ("mcq", "mcq"),
    
    )
    subtopic = models.CharField(max_length=20,
                  choices=subtopic_ch,
                  default="mcq",blank=True,null=True,db_index=True)
    subtopic_ch2= (
    ("more", "more"),
    
    )
    subtopic_2 = models.CharField(max_length=20,
                  choices=subtopic_ch2,
                  default="more",blank=True,null=True,db_index=True)
    day = models.DateField(default=datetime.date.today,db_index=True)
    creation_time= models.TimeField(blank=True, null=True)
    question = models.TextField(default='')
    option_1 = models.CharField(max_length=250)
    option_2= models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200)
    option_4 = models.CharField(max_length=200,blank=True, null=True)
    option_5 = models.CharField(max_length=200,null=True,blank=True)
    ans = models.IntegerField (default=1)

    year_exam = models.CharField(max_length=250,blank=True, null=True)
    


    extra=models.TextField(default='',blank=True,null=True)
    new_id=models.CharField(max_length=300,default='',blank=True,null=True,db_index=True)
    

    class Meta:
        ordering = ["-day"]
    
    
    def __str__(self):
        return self.day.strftime('%d/%m/%Y') + '     '+ self.question

    def save(self):
        self.new_id= self.question +'===' +self.day.strftime('%d-%m-%Y')
        super(physics, self).save()




      
class total_physics(models.Model):
    
    total_physics = models.IntegerField (db_index=True,default=3)
    total_physics_page = models.IntegerField (db_index=True,default=3)
    
    chapter_1=models.IntegerField (default=0)
    chapter_2=models.IntegerField (default=0)
    chapter_3=models.IntegerField (default=0)
    chapter_4=models.IntegerField (default=0)
    chapter_5=models.IntegerField (default=0)
    chapter_6=models.IntegerField (default=0)
    chapter_7=models.IntegerField (default=0)
    chapter_8=models.IntegerField (default=0)
    chapter_9=models.IntegerField (default=0)
    chapter_10=models.IntegerField (default=0)
    chapter_11=models.IntegerField (default=0)
    chapter_12=models.IntegerField (default=0)
    chapter_13=models.IntegerField (default=0)
    chapter_14=models.IntegerField (default=0)
    chapter_15=models.IntegerField (default=0)
    chapter_16=models.IntegerField (default=0)
    chapter_17=models.IntegerField (default=0)
    chapter_18=models.IntegerField (default=0)
    chapter_19=models.IntegerField (default=0)
    chapter_20=models.IntegerField (default=0)
    chapter_21=models.IntegerField (default=0)
    chapter_22=models.IntegerField (default=0)
    chapter_23=models.IntegerField (default=0)
    chapter_24=models.IntegerField (default=0)
    chapter_25=models.IntegerField (default=0)
    chapter_26=models.IntegerField (default=0)
    chapter_27=models.IntegerField (default=0)
    chapter_28=models.IntegerField (default=0)
    chapter_29=models.IntegerField (default=0)
    chapter_30=models.IntegerField (default=0)
    chapter_31=models.IntegerField (default=0)
    chapter_32=models.IntegerField (default=0)
    chapter_33=models.IntegerField (default=0)
    chapter_34=models.IntegerField (default=0)
    chapter_35=models.IntegerField (default=0)
    chapter_36=models.IntegerField (default=0)
    chapter_37=models.IntegerField (default=0)
    chapter_38=models.IntegerField (default=0)
    chapter_40=models.IntegerField (default=0)
    chapter_41=models.IntegerField (default=0)



    def save(self):
        totall=physics.objects.count()
        self.total_physics= totall
        self.total_physics_page=int(totall)/5

        
        for x in range(1,41):
            total=physics.objects.filter(chapter=str(x)).count()
            if total !=0:
                
                if(int(total)%5==0):
                    total_page=(int(total)/5)
                else:
                    total_page=(int(total)/5)+1
                y='chapter_'+ str(x)

                #self.chapter_1= total_page_1
                self.__dict__[y]=total_page


        
        super(total_physics, self).save()


class biology(models.Model):
    chapter= (
    ("1", "1"),   
    ("2", "2"),
    ("3", "3"),("4", "4"),("5", "5"),("6", "6"),("7", "7"),("8", "8"),("9", "9"),("10", "10"),("11", "11"),("12", "12"),("13", "13"),("14", "14"),("15", "15"),("16", "16"),
    ("17", "17"),("18", "18"),("19", "19"),("20", "20"),("21", "21"),("22", "22"),("23", "23"),("24", "24"),("25", "25"),("26", "26"),("27", "27"),("28", "28"),("29", "29"),("30", "30"),
    ("31", "31"),("32", "32"),("33", "33"),("34", "34"),("35", "35"),("36", "36"),("37", "37"),("38", "38"),("39", "39"),("40", "40"),("41", "41"),
    
    )
    chapter = models.CharField(max_length=10,
                          choices=chapter,
                          default="1",db_index=True)
    topic_ch= (
    ("question-answare", "question-answare"),
    
    )
    topic = models.CharField(max_length=18,
                  choices=topic_ch,
                  default="question-answare",blank=True,null=True,db_index=True)
    subtopic_ch= (
    ("mcq", "mcq"),
    
    )
    subtopic = models.CharField(max_length=20,
                  choices=subtopic_ch,
                  default="mcq",blank=True,null=True,db_index=True)
    subtopic_ch2= (
    ("more", "more"),
    
    )
    subtopic_2 = models.CharField(max_length=20,
                  choices=subtopic_ch2,
                  default="more",blank=True,null=True,db_index=True)
    day = models.DateField(default=datetime.date.today,db_index=True)
    creation_time= models.TimeField(blank=True, null=True)
    question = models.TextField(default='')
    option_1 = models.CharField(max_length=250)
    option_2= models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200)
    option_4 = models.CharField(max_length=200,blank=True, null=True)
    option_5 = models.CharField(max_length=200,null=True,blank=True)
    ans = models.IntegerField (default=1)

    year_exam = models.CharField(max_length=250,blank=True, null=True)
    


    extra=models.TextField(default='',blank=True,null=True)
    new_id=models.CharField(max_length=300,default='',blank=True,null=True,db_index=True)
    

    class Meta:
        ordering = ["-day"]
    
    
    def __str__(self):
        return self.day.strftime('%d/%m/%Y') + '     '+ self.question

    def save(self):
        self.new_id= self.question +'===' +self.day.strftime('%d-%m-%Y')
        super(biology, self).save()




      
class total_biology(models.Model):
    
    total_biology = models.IntegerField (db_index=True,default=3)
    total_biology_page = models.IntegerField (db_index=True,default=3)
    
    chapter_1=models.IntegerField (default=0)
    chapter_2=models.IntegerField (default=0)
    chapter_3=models.IntegerField (default=0)
    chapter_4=models.IntegerField (default=0)
    chapter_5=models.IntegerField (default=0)
    chapter_6=models.IntegerField (default=0)
    chapter_7=models.IntegerField (default=0)
    chapter_8=models.IntegerField (default=0)
    chapter_9=models.IntegerField (default=0)
    chapter_10=models.IntegerField (default=0)
    chapter_11=models.IntegerField (default=0)
    chapter_12=models.IntegerField (default=0)
    chapter_13=models.IntegerField (default=0)
    chapter_14=models.IntegerField (default=0)
    chapter_15=models.IntegerField (default=0)
    chapter_16=models.IntegerField (default=0)
    chapter_17=models.IntegerField (default=0)
    chapter_18=models.IntegerField (default=0)
    chapter_19=models.IntegerField (default=0)
    chapter_20=models.IntegerField (default=0)
    chapter_21=models.IntegerField (default=0)
    chapter_22=models.IntegerField (default=0)
    chapter_23=models.IntegerField (default=0)
    chapter_24=models.IntegerField (default=0)
    chapter_25=models.IntegerField (default=0)
    chapter_26=models.IntegerField (default=0)
    chapter_27=models.IntegerField (default=0)
    chapter_28=models.IntegerField (default=0)
    chapter_29=models.IntegerField (default=0)
    chapter_30=models.IntegerField (default=0)
    chapter_31=models.IntegerField (default=0)
    chapter_32=models.IntegerField (default=0)
    chapter_33=models.IntegerField (default=0)
    chapter_34=models.IntegerField (default=0)
    chapter_35=models.IntegerField (default=0)
    chapter_36=models.IntegerField (default=0)
    chapter_37=models.IntegerField (default=0)
    chapter_38=models.IntegerField (default=0)
    chapter_40=models.IntegerField (default=0)
    chapter_41=models.IntegerField (default=0)



    def save(self):
        totall=biology.objects.count()
        self.total_biology= totall
        self.total_biology_page=int(totall)/5

        
        for x in range(1,41):
            total=biology.objects.filter(chapter=str(x)).count()
            if total !=0:
                
                if(int(total)%5==0):
                    total_page=(int(total)/5)
                else:
                    total_page=(int(total)/5)+1
                y='chapter_'+ str(x)

                #self.chapter_1= total_page_1
                self.__dict__[y]=total_page


        
        super(total_biology, self).save()


class chemistry(models.Model):
    chapter= (
    ("1", "1"),   
    ("2", "2"),
    ("3", "3"),("4", "4"),("5", "5"),("6", "6"),("7", "7"),("8", "8"),("9", "9"),("10", "10"),("11", "11"),("12", "12"),("13", "13"),("14", "14"),("15", "15"),("16", "16"),
    ("17", "17"),("18", "18"),("19", "19"),("20", "20"),("21", "21"),("22", "22"),("23", "23"),("24", "24"),("25", "25"),("26", "26"),("27", "27"),("28", "28"),("29", "29"),("30", "30"),
    ("31", "31"),("32", "32"),("33", "33"),("34", "34"),("35", "35"),("36", "36"),("37", "37"),("38", "38"),("39", "39"),("40", "40"),("41", "41"),
    
    )
    chapter = models.CharField(max_length=10,
                          choices=chapter,
                          default="1",db_index=True)
    topic_ch= (
    ("question-answare", "question-answare"),
    
    )
    topic = models.CharField(max_length=18,
                  choices=topic_ch,
                  default="question-answare",blank=True,null=True,db_index=True)
    subtopic_ch= (
    ("mcq", "mcq"),
    
    )
    subtopic = models.CharField(max_length=20,
                  choices=subtopic_ch,
                  default="mcq",blank=True,null=True,db_index=True)
    subtopic_ch2= (
    ("more", "more"),
    
    )
    subtopic_2 = models.CharField(max_length=20,
                  choices=subtopic_ch2,
                  default="more",blank=True,null=True,db_index=True)
    day = models.DateField(default=datetime.date.today,db_index=True)
    creation_time= models.TimeField(blank=True, null=True)
    question = models.TextField(default='')
    option_1 = models.CharField(max_length=250)
    option_2= models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200)
    option_4 = models.CharField(max_length=200,blank=True, null=True)
    option_5 = models.CharField(max_length=200,null=True,blank=True)
    ans = models.IntegerField (default=1)

    year_exam = models.CharField(max_length=250,blank=True, null=True)
    


    extra=models.TextField(default='',blank=True,null=True)
    new_id=models.CharField(max_length=300,default='',blank=True,null=True,db_index=True)
    

    class Meta:
        ordering = ["-day"]
    
    
    def __str__(self):
        return self.day.strftime('%d/%m/%Y') + '     '+ self.question

    def save(self):
        self.new_id= self.question +'===' +self.day.strftime('%d-%m-%Y')
        super(chemistry, self).save()




      
class total_chemistry(models.Model):
    
    total_chemistry = models.IntegerField (db_index=True,default=3)
    total_chemistry_page = models.IntegerField (db_index=True,default=3)
    
    chapter_1=models.IntegerField (default=0)
    chapter_2=models.IntegerField (default=0)
    chapter_3=models.IntegerField (default=0)
    chapter_4=models.IntegerField (default=0)
    chapter_5=models.IntegerField (default=0)
    chapter_6=models.IntegerField (default=0)
    chapter_7=models.IntegerField (default=0)
    chapter_8=models.IntegerField (default=0)
    chapter_9=models.IntegerField (default=0)
    chapter_10=models.IntegerField (default=0)
    chapter_11=models.IntegerField (default=0)
    chapter_12=models.IntegerField (default=0)
    chapter_13=models.IntegerField (default=0)
    chapter_14=models.IntegerField (default=0)
    chapter_15=models.IntegerField (default=0)
    chapter_16=models.IntegerField (default=0)
    chapter_17=models.IntegerField (default=0)
    chapter_18=models.IntegerField (default=0)
    chapter_19=models.IntegerField (default=0)
    chapter_20=models.IntegerField (default=0)
    chapter_21=models.IntegerField (default=0)
    chapter_22=models.IntegerField (default=0)
    chapter_23=models.IntegerField (default=0)
    chapter_24=models.IntegerField (default=0)
    chapter_25=models.IntegerField (default=0)
    chapter_26=models.IntegerField (default=0)
    chapter_27=models.IntegerField (default=0)
    chapter_28=models.IntegerField (default=0)
    chapter_29=models.IntegerField (default=0)
    chapter_30=models.IntegerField (default=0)
    chapter_31=models.IntegerField (default=0)
    chapter_32=models.IntegerField (default=0)
    chapter_33=models.IntegerField (default=0)
    chapter_34=models.IntegerField (default=0)
    chapter_35=models.IntegerField (default=0)
    chapter_36=models.IntegerField (default=0)
    chapter_37=models.IntegerField (default=0)
    chapter_38=models.IntegerField (default=0)
    chapter_40=models.IntegerField (default=0)
    chapter_41=models.IntegerField (default=0)



    def save(self):
        totall=chemistry.objects.count()
        self.total_chemistry= totall
        self.total_chemistry_page=int(totall)/5

        
        for x in range(1,41):
            total=chemistry.objects.filter(chapter=str(x)).count()
            if total !=0:
                
                if(int(total)%5==0):
                    total_page=(int(total)/5)
                else:
                    total_page=(int(total)/5)+1
                y='chapter_'+ str(x)

                #self.chapter_1= total_page_1
                self.__dict__[y]=total_page


        
        super(total_chemistry, self).save()
