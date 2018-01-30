from __future__ import unicode_literals
from django.db import models
import re

username_REGEX = re.compile('^[_a-z0-9-]+(.[_a-z0-9-]+)@[a-z0-9-]+(.[a-z0-9-]+)(.[a-z]{2,4})$')

class BlogManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) == 0:
            errors['empty_name'] = 'Name cannot be empty'
        if len(postData['username']) == 0:
            errors['empty_username'] = 'username cannot be empty'
        if len(postData['password']) == 0:
            errors['empty_password'] = 'Password cannot be empty'
        if len(postData['password_confirmation']) == 0:
            errors['empty_password_confirmation'] = 'Password confirmation cannot be empty'
        if len(postData['name']) < 3:
            errors['name_error'] = 'Name should have at least three characters.'
        if len(postData['username']) < 3:
            errors['username_error'] = 'Username should have at least three characters.'
        for user in User.objects.filter(username = postData['username']):
            if user:
                errors['repeated_username'] = 'The username already exists. Please use a different one.'
        if len(postData['password']) < 8:
            errors['password'] = 'Password needs to be at least 8 characters long.'
        if postData['password'] != postData['password_confirmation']:
            errors['password_confirmation'] = 'Passwords have to match.'

        return errors

    def item_validator(self, postData):
        errors = {}

        if len(postData['item']) == 0:
            errors['item_empty'] = 'Item cannot be empty'

        if len(postData['item']) < 4:
            errors['item'] = 'Item should have more than three characters.'

        return errors

class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    date_hired = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BlogManager()

class Item(models.Model):
    item = models.CharField(max_length = 255)
    added_by = models.ForeignKey(User, related_name = 'my_item')
    wished_by = models.ManyToManyField(User, related_name = 'wish_list')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BlogManager()
