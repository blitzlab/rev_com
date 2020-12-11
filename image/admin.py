from django.contrib import admin
from . import models
from main import models as m
from django.db.models import F
from django.template.loader import render_to_string
from django.contrib.auth import get_permission_codename
from django.core.mail import EmailMultiAlternatives

# Register your models here.

class ImageAdmin(admin.ModelAdmin):
    list_display = ["image_title", "image_type", "site_name", "approved", "date_published"]
    search_fields = ["user__username", "image_title", "site_name", "approved"]

    actions = ['approve_image','reject_image']

    def reject_image(self, request, queryset):
        queryset.update(approved=False, status="Rejected")

    def approve_image(self, request, queryset):
        post_reward = models.ImagePostReward.objects.get(pk=1)
        queryset.update(approved=True, status="Approved")
        for object in queryset:
            user = m.User.object.get(pk=object.user.pk)#Get Image poster object
            user_wallet = m.Wallet.objects.get(user=user)#Get Image poster wallet
            user_package = m.PremiumUser.objects.filter(user=user).count()
            if user_package == 1:
                bonus = post_reward.premium_member_reward
                user_wallet.balance = F('balance') + bonus
                user_wallet.save(update_fields=['balance'])
                m.AllEarnings.objects.create(user=user, amount=bonus)
            elif user_package < 1:
                bonus = post_reward.ordinary_member_reward
                user_wallet.balance = F('balance') + bonus
                user_wallet.save(update_fields=['balance'])
                m.AllEarnings.objects.create(user=user, amount=bonus)

            # admin = User.object.filter(is_superuser = True)
            subject = "Image Approval Notification"

            message = render_to_string('image/image_approval_notification.html', {
                "user": user.username,# admin username,
                "bonus": bonus
            })

            msg = EmailMultiAlternatives(subject, message, "simplerefers@gmail.com", [user.email])
            msg.attach_alternative(message, "text/html")
            msg.send()



    approve_image.allowed_permissions = ('approve',)
    reject_image.allowed_permissions = ('reject',)

    def has_approve_permission(self, request):
        """Does the user have the approve image permission?"""
        opts = self.opts
        codename = get_permission_codename('approve', opts)
        return request.user.has_perm('%s.%s' % (opts.app_label, codename))

    def has_reject_permission(self, request):
        """Does the user have the reject image permission?"""
        opts = self.opts
        codename = get_permission_codename('reject', opts)
        return request.user.has_perm('%s.%s' % (opts.app_label, codename))

    readonly_fields = ["approved"]
    readonly_fields = ["status"]
    filter_horizontal = ()


class ImageViewRewardAdmin(admin.ModelAdmin):
    list_display = ["ordinary_viewer_reward", "premium_viewer_reward"]
    filter_horizontal = ()
    fieldsets = ()


class ImageViewTable(admin.ModelAdmin):
    list_display = ["image", "viewer", "date_viewed"]
    filter_horizontal = ()
    fieldsets = ()


admin.site.register(models.Image, ImageAdmin)
admin.site.register(models.ImageViewReward, ImageViewRewardAdmin)
admin.site.register(models.ImageViewCountDown)
admin.site.register(models.ImagePostReward)
admin.site.register(models.Viewer, ImageViewTable)
admin.site.register(models.ImageViewLimit)
