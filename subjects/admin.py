from django.contrib import admin

# Register your models here.
from .models import *
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('createdAt',)

class CommnetAdmin(admin.ModelAdmin):
    readonly_fields = ('createdAt',)

admin.site.register(Subject)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommnetAdmin)
admin.site.register(isLiked)
admin.site.register(isScrapped)
admin.site.register(LikedSubject)
admin.site.register(PostVote)
admin.site.register(CommentVote)
