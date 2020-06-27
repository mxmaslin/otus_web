# Final project 

I've chosen the ecommerce site for Otus "Python web-developer" final project.

Site's owner (seller) can deploy items for sale, and discount coupons at `http://127.0.0.1:8000/admin/`. Prior to this actions, create a superuser using `./manage.py createsuperuser` command. 

Site's visitor (buyer) can select items for purchase, filter them using items categories, apply discounts, and proceed to checkout. The project's entry point is `http://127.0.0.1:8000/`. For the sake of demonstration, create some items for sale as site's owner.

To implement the project, I've used

- [django_project_boilerplate](https://github.com/justdjango/django_project_boilerplate)
- [django-allauth](https://github.com/pennersr/django-allauth) for signup/logging in stuff
- [mdbootstrap](https://mdbootstrap.com/freebies/jquery/e-commerce/) templates theme 

Instructions:

1. Install python requirements.
2. Create superuser.
3. Using admin interface, create items and discount coupons.
4. Run `./manage runserver`.
5. Browse items categories, choose items to purchase, proceed to checkout. 
 
The application developed for [Web-разработчик на Python](https://otus.ru/lessons/webpython/) training course.
