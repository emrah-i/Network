from django.contrib import admin
from .models import User, Post, Comment, UserFollow

class UserFollowInline(admin.TabularInline):
    model = UserFollow
    fk_name = 'is_now_following'
    extra = 0
    readonly_fields = ('datetime_followed', )
    verbose_name_plural = 'Followers'

class UserFollowingInline(admin.TabularInline):
    model = UserFollow
    fk_name = 'user'
    extra = 0
    readonly_fields = ('datetime_followed', )
    verbose_name_plural = 'Following'

class UserAdmin(admin.ModelAdmin):
    inlines = [UserFollowInline, UserFollowingInline]
    list_display = ('username', 'follower_count', 'following_count')

    def follower_count(self, obj):
        return obj.is_now_following.count()
    follower_count.short_description = 'Follower Count'

    def following_count(self, obj):
        return obj.user.count()
    follower_count.short_description = 'Following Count'

admin.site.register(User, UserAdmin)
admin.site.register(UserFollow)
admin.site.register(Post)
admin.site.register(Comment)
