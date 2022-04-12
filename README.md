# E-Shop website using Django

## Intro

This project was made to learn Django's basic stuff, such as CRUD'ing (Create, Read, Update, Delete) models in views; authenticating and authorising users via custom form; managing permissions both on server-side and on client-side; filtering objects via form; session's variables manipulation and GET & POST requests manipulation; class-based views and function-based views.

This differs from my previous web-site, RentUments, where the focus was more on HTML, CSS, and Django's way to load templates.
I am also not following any video tutorials for this project, I am simply using docs, stack overflow and google for any possible errors that occur.

## Accessing the website

1. Install [Python](https://www.python.org/downloads/);
2. Install Django: in console type (make sure you have PIP in your PATH variable) `pip install Django`;
3. Copy the contents of the repository to your working directory;
4. Run in console `python %location_of_your_directory%/manage.py runserver`
5. If everything goes correctly you should see the line "Starting development server at http://127.0.0.1:8000/"
6. Open another tab or window in your console and enter `python %location_of_your_directory%/manage.py makemigrations` then `python %location_of_your_directory%/manage.py migrate`
7. **AS AN EXTRA PRECAUTIOS STEP YOU CAN WRITE IN YOUR CONSOLE NEXT COMMANDS:** 
*	`python %location_of_your_directory%/manage.py makemigrations products`
*	`python %location_of_your_directory%/manage.py migrate products`
*	`python %location_of_your_directory%/manage.py makemigrations profiles`
*	`python %location_of_your_directory%/manage.py migrate profiles`
*	`python %location_of_your_directory%/manage.py makemigrations cart`
*	`python %location_of_your_directory%/manage.py migrate cart`
8. Open your browser and enter the url given in the previous line.

## Guide

### Preliminary actions

Before accessing the website open your console and run `python %location_of_your_directory%/manage.py createsuperuser` then enter any *username*, *email* (not required), *password*, *password again*. You have created the superuser, which has access to the 'admin' panel. Now you can work with the website.

When accessing the web-site for the first time, the first thing you should do is type in your URL-bar: 'http://127.0.0.1:8000/admin/' (or click on 'admin' on the navbar) and enter the **superuser**'s credentials (the ones you typed in your console before). Now you should navigate to the 'Groups' panel and create the group called 'Workers', exactly like that, capital 'W'.
This was a hack that I used in the beginning of the project because I didn't want to manage all the permissions through the admin panel, but didn't know how to make dynamically changing group so I sticked with hard-coding 'Workers'.

### Creating accounts for workers

If you want to create 'worker-users' ('работяг') who have more permissions than normal users, but not as much as superusers, then after creating the user you should add the worker's profile manually to the 'Workers' group via 'Users' panel. 
You can create accounts using admin panel or via the site itself (click 'Login' on the navbar then on 'Create Account' button). Below are both ways of doing it
**Admin panel**:
* Go to http://127.0.0.1:8000/admin/
* Click on yellow '**+**' sign near *Users* panel.
* Enter credentials.

**Using site's login system**:
* Go to http://127.0.0.1:8000/
* Click on *Login* on the navbar.
* Click on *Create Account* button.
* Enter credentials.

**Note**: If you don't want to come up with some crazy password combination, then you should probably consider the second way of creating an account, because I didn't put any password-validation or complication system there exactly for that.

After creating an account, go to http://127.0.0.1:8000/admin/, click on *Users* panel (not **+** sign or *change*), click on desired worker's profile, scroll down to 'Groups', double-click on 'Workers', then scroll down and click *Save*.
**Congratulations, you have made an account for your worker!**

### Permissions

#### Unauthorised users
* Examine the products;
* Filter them by maker or category;
* Use contacts form;
* Create new accounts.

#### Authorised customers
* Examine the products;
* Filter products by maker or category;
* Add products to cart;
* Remove products from cart one-by-one or altogether;
* Update own profile;
* Delete own profile;
* Use contacts form;
* Create new accounts.

#### Workers
* Examine the products;
* Filter products by maker or category;
* Add products to database;
* Edit products in database;
* Remove products from database;
* Add products to cart;
* Remove products from cart one-by-one or altogether;
* Update own profile;
* Delete own profile;
* Use contacts form;
* Create new accounts.

#### Superusers and admins
* Examine the products;
* Filter products by maker or category;
* Add products to database;
* Edit products in database;
* Remove products from database;
* Add products to cart;
* Remove products from cart one-by-one or altogether;
* Examine all profiles;
* Update all profiles;
* Delete all profiles;
* Use contacts form;
* Create new accounts;
* Access admin panel.

#### Optional info
Contacts form sends message to the console, so you can read and test how it works.
In settings SECRET_KEY is left as-is.
Some errors and exceptions are handled server-side and some client-side for educational purposes.
As of now I'll concentrate on HTML & CSS, because the backbone of website is ready.
All the validators will be added later.

## Thank you for trying out my project!
[Telegram](t.me/SXRU1)
