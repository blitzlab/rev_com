from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, ListView,
                                    DetailView, CreateView, DeleteView)
from django.core import exceptions as e
from main.models import (Wallet, PremiumUser, AllEarnings, PremiumUser)
from django.http import JsonResponse
from django.contrib.messages.views import SuccessMessageMixin
from .models import (Image, ImageViewCountDown, ImageViewReward, Viewer,
                        ImagePostReward, ImageViewLimit)
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.db.models import F

# Create your views here.
@login_required
def image_list_view(request):
    image_list = list()
    counter = 0
    images = Image.objects.filter(approved=True)
    try:
        wallet_balance = Wallet.objects.get(user=request.user)

    except e.ObjectDoesNotExist:
         wallet_balance = Wallet.objects.create(user=request.user, balance=0)

    image_viewed = Viewer.objects.all()

    user_package = PremiumUser.objects.filter(user=request.user).count()
    image_view_reward = ImageViewReward.objects.get(pk=1)
    if user_package == 1:
        reward = image_view_reward.premium_viewer_reward
    elif user_package < 1:
        reward = image_view_reward.ordinary_viewer_reward


    from datetime import datetime
    from dateutil import parser


    for image in images:
        if counter >= 12:
            break;
        # v_image = {"image":image}
        if image.viewed:
            for view in image_viewed:
                if image == view.image:
                    if view.viewer == request.user:
                        if parser.parse(view.display_till) >= timezone.now():
                            v_image = {"image":image, "viewed":True}
                            image_list.append(v_image)
                        else: continue
                    else:
                        v_image = {"image":image, "viewed":False}
                        image_list.append(v_image)
                else: continue
        else:
            v_image = {"image":image, "viewed":False}
            image_list.append(v_image)
            counter+=1

    print(image_list)
    return render(request, "image/image_list.html", {"wallet_balance":wallet_balance.balance, "images": image_list, "reward":reward})

class ImageCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Image
    fields = ["image_url", "image_title", "image_type", "site_name", "your_name", "comment"]
    template_name="image/image_form.html"
    success_message = "Image submitted for approval"
    extra_tags ="image_submitted"


    def form_valid(self, form):
        form.instance.user = self.request.user
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message, extra_tags=self.extra_tags)
        return super(ImageCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            wallet_balance = Wallet.objects.get(user=self.request.user)

        except e.ObjectDoesNotExist:
             wallet_balance = Wallet.objects.create(user=self.request.user, balance=0)

        post_reward = ImagePostReward.objects.get(pk=1)
        user_package = PremiumUser.objects.filter(user=self.request.user).count()
        if user_package == 1:
            bonus = post_reward.premium_member_reward
        elif user_package < 1:
            bonus = post_reward.ordinary_member_reward

        my_images = Image.objects.filter(user=self.request.user).order_by("-date_published")[:2]
        my_pending_images = Image.objects.filter(user=self.request.user, approved=False).count()
        context.update({"wallet_balance":wallet_balance.balance,
                        "my_images":my_images, "bonus": bonus,
                        "pending_images":my_pending_images})



        return context


def image_detail(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login to view image", extra_tags="warn")
        return redirect('image:images')
    try:
        image = Image.objects.get(pk=pk)
    except e.ObjectDoesNotExist:
         messages.warning(request, "Image does not exist", extra_tags="warn")
         return redirect('image:images')

    if image.viewed and Viewer.objects.filter(viewer=request.user, image=image):
        messages.warning(request, "You have earned on this image", extra_tags="warn")
        return redirect('image:images')

    now = timezone.now()
    # Get current day date object
    # like: 12/02/2019 00:00:00
    today = now.replace(hour=0).replace(minute=0).replace(second=0).replace(microsecond=0)
    daily_view_limit = ImageViewLimit.objects.get(pk=1)
    view_count = Viewer.objects.filter(viewer=request.user, date_viewed__gte=today, date_viewed__lte=today + timedelta(days=1)).count()
    print(view_count)
    if view_count >= daily_view_limit.limit:
        messages.warning(request, "You have reached your image view limit for today, please try again tommorrow")
        return redirect('image:images')



    try:
        wallet_balance = Wallet.objects.get(user=request.user)

    except e.ObjectDoesNotExist:
         wallet_balance = Wallet.objects.create(user=request.user, balance=0)

    context = {"image":image, "wallet_balance":wallet_balance.balance}
    return render(request, "image/image_detail.html", context)



#Fetch Image view countdown
def get_countdown(request):

    if request.is_ajax or None:
            id_count = 1
            while True:
                try:
                    countdown = ImageViewCountDown.objects.get(pk=id_count)
                    break
                except e.ObjectDoesNotExist:
                    id_count += 1
            response = JsonResponse({"countdown": countdown.seconds}, status=200)
    #
    return response


def image_view_proccess(request):
    if request.is_ajax or None:
        user = request.user
        image_id = request.GET.get("imageId")
        image = Image.objects.get(pk=image_id)
        if Viewer.objects.filter(viewer=user, image=image).count() >= 1:
            message = F"You have earned on this image once"
            response = JsonResponse({"message": message}, status=200)
        else:
            image.viewed = True
            image.save()
            Viewer.objects.create(viewer=user, image=image,
            # date_viewed=timezone.now(),
            display_till = timezone.now() + timezone.timedelta(hours=1))
            # image.viewer = user.pk
            # image.date_viewed = timezone.now()
            # image.display_till = timezone.now() + timezone.timedelta(hours=1)
            user_wallet = Wallet.objects.get(user=user)
            user_package = PremiumUser.objects.filter(user=user).count()
            image_view_bonus = ImageViewReward.objects.get(pk=1)
            if user_package == 1:
                # image_view_bonus = ImageViewReward.objects.get(pk=1)
                # UserLogins.objects.create(user=user)
                bonus = image_view_bonus.premium_viewer_reward
                user_wallet.balance = F('balance') + bonus
                user_wallet.save(update_fields=['balance'])
                AllEarnings.objects.create(user=user, amount=bonus)
                # messages.success(self.request, f"Login successful {image_view_bonus} naira login bonus has been added to your wallet")
            elif user_package < 1:
                # image_view_bonus = LoginBonus.objects.get(pk=1)
                # UserLogins.objects.create(user=user)
                bonus = image_view_bonus.ordinary_viewer_reward
                user_wallet.balance = F('balance') + bonus
                user_wallet.save(update_fields=['balance'])
                AllEarnings.objects.create(user=user, amount=bonus)
            message = F"Your wallet has been credited with {bonus} naira viewer's bonus"
            response = JsonResponse({"message": message}, status=200)
    return response


class ImageDeleteView(DeleteView):
    model = Image
    success_url = reverse_lazy('image:add_image')
