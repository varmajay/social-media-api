from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import *

# Register your models here.

@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ['id','name','email']



@admin.register(UserToken)
class AdminUserToken(admin.ModelAdmin):
    list_display = ['user',]



@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    list_display = ['user','image','caption','created_at','likes','id']

@admin.register(Comment)
class AdminComment(admin.ModelAdmin):
    list_display = ['user','post_user','post_id','comment','date','id']
    def post_user(self, obj):
        return obj.post.user
    def post_id(self, obj):
        return obj.post.id

@admin.register(Follower)
class AdminFollower(admin.ModelAdmin):
    list_display = ['user','follower','id']


@admin.register(LikePost)
class AdminLikePost(admin.ModelAdmin):
    list_display = ['post','user','id']