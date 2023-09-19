# myapp1
Django project myApp1 is simple app for administration of daily needs in fictive production plant. 
This project is divied in three packages, created like standard Django apps:
  -  users
  -  food
  -  maintenance

Users:
  There are 3 models:
  -  Profile
  -  Role
  -  Workcenter

    Profile
      This model contains parameters to each user, who register to this app

    Role
      This model define role. Each role gives to it's user access to different section of application

    Workcenter
      This model represents workcenter to assign Accidents and Tasks in maintenance Section

Maintenance:
  There are 2 models:
  -  Accident
  -  MaintenanceTask

    
    Accident
      This model contains parameters to accidents. Each Accident is linked to Workcenter and Profile. 

    MaintenanceTask
      This model contains parameters to task. Each Accident is linked to Accident and Profiles.
      

Food:
  There are 7 models:
  -  PizzaDayDay
  -  PizzaOrder
  -  LunchMeal
  -  LunchMenu
  -  LunchMenuOption
  -  LunchOrder
  -  TransactionHistory

    
    PizzaDayDay
      Represent day to which is possible to order pizza.

    PizzaOrder
      This model contains information to each pizzaorder(which, which pizza, to which time, to which PizzaDayDay.

    LunchMeal
      In this model is represent just some meal(short text & price) 

    LunchMenu
      This model represent just date, to which can be created LunchMenu

    LunchMenuOption
      This model contains just type of meal and quantity available for orders in that day.

    LunchOrder
      This model contains connection to Profile and LunchMenuOption

    Transaction history
      This model is prepared just for storing all transactions(orders nad payments) for cases that meal will be deleted from database.
      
Views function and url routes saved standardly in files which Django creates. Static files and templates also.

In api folder is prepared few endpoints just for GET method.

User authentication is made according to django.contrib.auth.


     
