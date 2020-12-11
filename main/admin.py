from . import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_permission_codename
# from django.contrib.auth.forms import ReadOnlyPasswordHashField


class AdminUser(UserAdmin):
    list_display = ["first_name", "last_name", "username", "email", "last_login", "email_confirmed", "is_admin", "is_staff", "is_active", "registered_on"]
    search_fields = ["username", "email"]
    readonly_fields = ["is_admin", "is_staff", "is_active", "is_superuser", "registered_on", "last_login"]

    filter_horizontal = ()
    list_filter = ["gender", "country", "is_active", "is_admin", "is_staff"]
    fieldsets = ()

class WalletAdmin(admin.ModelAdmin):
    # readonly_fields = ["user", "balance",]
    search_fields = ["user__username"]
    fieldsets = ()

class UserLoginsAdmin(admin.ModelAdmin):
    list_display = ["user", "date",]
    search_fields = ["user__username"]
    filter_horizontal = ()
    fieldsets = ()

class BlogAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "slug", "status", "published_on"]
    search_fields = ["author__username", "title"]

    actions = ['publish_post',]

    def publish_post(self, request, queryset):
        queryset.update(status='Published')

    publish_post.allowed_permissions = ('publish',)

    def has_publish_permission(self, request):
        """Does the user have the publish post permission?"""
        opts = self.opts
        codename = get_permission_codename('publish', opts)
        return request.user.has_perm('%s.%s' % (opts.app_label, codename))

    readonly_fields = ["status"]
    filter_horizontal = ()
    fieldsets = ()

class CommentAdmin(admin.ModelAdmin):
    list_display = ["blog", "user", "comment", "commented_on"]
    search_fields = ["blog__title", "user__username", "commented_on"]
    filter_horizontal = ()
    fieldsets = ()

class WithdrawRequest(admin.ModelAdmin):
    list_display = ["user", "amount", "account_number", "bank_name", "status", "request_on",]

    actions = ['approve_withdraw', 'decline_withdraw']

    def approve_withdraw(self, request, queryset):
        queryset.update(status='Approved')
    def decline_withdraw(self, request, queryset):
        queryset.update(status='Declined')

    approve_withdraw.allowed_permissions = ('approve',)
    decline_withdraw.allowed_permissions = ('decline',)

    def has_approve_permission(self, request):
        """Does the user have the approve permission?"""
        opts = self.opts
        codename = get_permission_codename('approve', opts)
        return request.user.has_perm('%s.%s' % (opts.app_label, codename))

    def has_decline_permission(self, request):
        """Does the user have the deline permission?"""
        opts = self.opts
        codename = get_permission_codename('decline', opts)
        return request.user.has_perm('%s.%s' % (opts.app_label, codename))

    filter_horizontal = ()
    fieldsets = ()



# Register your models here.
app_models = (models.PremiumUser, models.Upgrade,
                models.SignupBonus, models.CommentBonus,
                models.LoginBonus, models.PremiumLoginBonus, models.ReferBonus,
                models.PremiumUserReferUpgradeBonus, models.PremiumUserCommentBonus,
                models.PremiumReferBonus, models.BlogLikeBonus, models.PremiumBlogLikeBonus,
                models.BlogLike, models.MinimumWithdrawAmount)

admin.site.register(models.User, AdminUser)
admin.site.register(app_models)
admin.site.register(models.WithdrawRequest, WithdrawRequest)
admin.site.register(models.Blog, BlogAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.UserLogins, UserLoginsAdmin)
admin.site.register(models.Wallet, WalletAdmin)
# admin.site.register(models.WithdrawRequest, WithdrawRequest)
