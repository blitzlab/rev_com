from .extends import *


# Create your views here.
class IndexView(TemplateView, auth_view.LoginView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
        # print("Not authenticated!")

            try:
                wallet_balance = Wallet.objects.get(user=self.request.user)

            except e.ObjectDoesNotExist:
                 wallet_balance = Wallet.objects.create(user=self.request.user, balance=0)
            context.update({"wallet_balance":wallet_balance.balance})



        return context

class AboutView(IndexView):
    template_name = "main/about-us.html"

class ContactView(TemplateView):
    template_name = "main/contact-us.html"
    form = ContactForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            print(self.request.user)
        # print("Not authenticated!")
            wallet_balance = Wallet.objects.get(user=self.request.user)
            context.update({"wallet_balance":wallet_balance.balance})

        context.update({"form": self.form})

        return context


#Contact form views
def contact_form_view(request):
    if request.is_ajax and request.method == "POST" or None:
        bind_form = ContactForm(request.POST)
        if bind_form.is_valid():
            username = bind_form.cleaned_data["username"]
            sender_email = bind_form.cleaned_data["email"]
            message = bind_form.cleaned_data["message"]
            admin = User.object.filter(is_superuser = True)
            subject = "Contact Form"
            for adm in admin:

                message = render_to_string('main/contact_form_template.html', {
                    "admin": adm.username,# admin username,
                    "sender_name":username,
                    "sender_email":sender_email,
                    "message":message
                })
                # send_mail(
                #     subject,
                #     message,
                #     "admin@simplerefers.com",
                #     # f"{sender_email}", #from sender
                #     [adm.email], #to admin
                #     fail_silently=False,
                # )
                msg = EmailMultiAlternatives(subject, message, "simplerefers@gmail.com", [adm.email])
                msg.attach_alternative(message, "text/html")
                msg.send()
            response = JsonResponse({"message": "Message sent successfully"}, status=200)
        else:
             response = JsonResponse({"message": "Message not sent"}, status=400)
    return response

#Faq View
class FaqView(IndexView):
    template_name = "main/faq.html"


# User opgrade view
class UpgradeView(TemplateView):
    template_name = "main/upgrade.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                Upgrade_package = Upgrade.objects.get(name="Premium")
            except e.ObjectDoesNotExist:
                 Upgrade_package = Upgrade.objects.create(name="Premium", price=0)


            premuim_user = PremiumUser.objects.filter(user=self.request.user).count()
            if premuim_user == 1:
                user_package = True
            elif premuim_user == 0:
                user_package = False
            if self.request.user.is_authenticated:
                try:
                    wallet_balance = Wallet.objects.get(user=self.request.user)
                except e.ObjectDoesNotExist:
                     wallet_balance = Wallet.objects.create(user=self.request.user, balance=0)

            context.update({
                "wallet_balance":wallet_balance.balance,
                "package_name":Upgrade_package.name,
                "package_price":Upgrade_package.price,
                "user_email": self.request.user.email,
                "user_package": user_package
            })
        return context

    def render_to_response(self, context):

        if not self.request.user.is_authenticated:
            messages.info(self.request, "Please login")
            return redirect('main:login')

        return super(UpgradeView, self).render_to_response(context)


@receiver(payment_verified)
def on_payment_verified(sender, ref, amount, **kwargs):
    """
    ref: paystack reference sent back.
    amount: amount in Naira.
    """
    pass

def upgrade_success_view(request):
    user = request.user
    try:
        upgrade_user = PremiumUser.objects.create(user=user)
        upgrade_user.save()
    except IntegrityError:
        # messages.success(request, "You are a premium ")
        return redirect('main:index')
    # Get premium_reffer
    check_referrer = User.object.filter(ref_id=user.referrer).count()
    if check_referrer == 1:
        referrer = User.object.get(ref_id=user.referrer)
        # get referrer package
        referrer_package = PremiumUser.objects.filter(user=referrer).count()
        if referrer_package == 1:

            # get referrer wallet
            check_wallet = Wallet.objects.filter(user=referrer).count()
            premium_user_refer_upgrade_bonus = PremiumUserReferUpgradeBonus.objects.get(pk=1)
            if check_wallet == 1:
                referrer_wallet = Wallet.objects.get(user=referrer)
                referrer_wallet.balance = F('balance') + premium_user_refer_upgrade_bonus.amount
                referrer_wallet.save(update_fields=['balance'])
                AllEarnings.objects.create(user=referrer, amount=premium_user_refer_upgrade_bonus.amount)
            else:
                Wallet.objects.create(user=referrer, balance=premium_user_refer_upgrade_bonus.amount)
                AllEarnings.objects.create(user=referrer, amount=premium_user_refer_upgrade_bonus.amount)

    return render(request, "main/upgrade_success.html", {"wallet_balance":Wallet.objects.get(user=user)})

#Generate referal link
def referal_link_view(request):
    current_site = get_current_site(request)

    if request.is_ajax or None:
        username = request.GET.get("username")
        # print(username)
    #
        if request.user.is_authenticated:
            user_ref_id = request.user.ref_id
            # print(user_ref_id)
    #
            ref_link = render_to_string('main/referal_link.html', {
                'domain': current_site.domain,
                'refid': user_ref_id
            })
            # print(ref_link)
            # ser_instance = serializers.serialize('json', [ ref_link, ])
            response = JsonResponse({"reflink": ref_link}, status=200)
        else:
            response = JsonResponse({"error": "User unknown"}, status=400)
    #
    return response

#Register user
def user_signup(request, refid="None"):
    if request.user.is_authenticated:
        messages.info(request, "Your are currently logged in")
        return redirect('main:index')
    current_site = get_current_site(request)
    if not refid == "None":
        checkrefid = User.object.filter(ref_id=refid).count()
        if checkrefid == 0:
            refid=None
            messages.error(request, "Invalid referal link, please register below")

    signup_form = UserSignUpForm(initial = {"refid":refid}, auto_id=False)

    # other_data = MemberDataForm()
    if request.method == "POST" or None:
        signup_form = UserSignUpForm(data = request.POST)
        # other_data = MemberDataForm(data = request.POST)
        #
        if signup_form.is_valid():
            print(signup_form)
            refid = signup_form.cleaned_data["refid"]
            user = signup_form.save(commit = False)
            #     user.set_password(user.password)
            if User.object.filter(ref_id=refid).count() == 1:
                referrer = User.object.get(ref_id=refid)
                user.referrer = referrer.ref_id
                # Reward referrer
                user_wallet = Wallet.objects.get(user=referrer)
                user_package = PremiumUser.objects.filter(user=referrer).count()
                if user_package == 1:
                    refer_bonus = PremiumReferBonus.objects.get(pk=1)
                    user_wallet.balance = F('balance') + refer_bonus.amount
                    user_wallet.save(update_fields=['balance'])
                    AllEarnings.objects.create(user=referrer, amount=refer_bonus.amount)
                elif user_package < 1:
                    refer_bonus = ReferBonus.objects.get(pk=1)
                    user_wallet.balance = F('balance') + refer_bonus.amount
                    user_wallet.save(update_fields=['balance'])
                    AllEarnings.objects.create(user=referrer, amount=refer_bonus.amount)
                # Send email to referrer
                subject = 'Referrer Bonus'
                message = render_to_string('main/referrer_notification_email.html', {
                    'user': referrer,
                })

                send_mail(
                    subject,
                    message,
                    # f"admin@{current_site.domain}",
                    "simplerefers@gmail.com",
                    [referrer.email],
                    fail_silently=False,
                )


            user.ref_id = str(random.randrange(1, 9999, 4))
            user.save()
            signup_bonus = SignupBonus.objects.get(pk=1)
            credit_user_wallet = Wallet(user=user, balance=float(str(signup_bonus)))
            credit_user_wallet.save()
            AllEarnings.objects.create(user=user, amount=signup_bonus.amount)
            current_site = get_current_site(request)

            subject = 'Email Verification'
            message = render_to_string('main/account_verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_mail(
                subject,
                message,
                # f"admin@{current_site.domain}",
                "simplerefers@gmail.com",
                [user.email],
                fail_silently=False,
            )
            # user.email_user(subject, message)


            messages.success(request, "User registered successfuly")
            messages.info(request, "Please check your email box to verify your account, thanks.")
        else:
            messages.error(request, "Cannot register user")
            # return render(request, "main/user_signup.html", {"signup":signup_form })

    return render(request, "main/user_signup.html", {"signup_form":signup_form, "refid":refid, "domain":current_site.domain })


def verify_user_email(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.object.get(pk=uid)
        print(uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.email_confirmed = True
        user.save()
        print("Your email has been verified successfuly")
        messages.success(request, "Your email has been verified successfuly")
        return redirect('main:index')
    else:
        print("Email verification failed")
        messages.error(request, "Email verification failed")
        return redirect('main:index')


class UserLoginView(auth_view.LoginView):
    template_name = "main/user_login.html"


    def get_success_url(self):
        '''Here the part where you can implement your login logic'''
        # Get the client from the user object
        user = self.request.user

        @login_reward
        def get_reward(user):
            settings.LOGIN_REDIRECT_URL = f"/profile/{user.pk}/"
            return redirect(settings.LOGIN_REDIRECT_URL)

        get_reward(user)
        # now = timezone.now()
        # # Get current day date object
        # # like: 12/02/2019 00:00:00
        # today = now.replace(hour=0).replace(minute=0).replace(second=0).replace(microsecond=0)
        #
        #
        # user_logins = UserLogins.objects.filter(
        #     user=user,
        #     date__gte=today,
        #     date__lte=today + timedelta(days=1)
        # ).count()
        # if user_logins < 1:
        #     user_wallet = Wallet.objects.get(user=user)
        #     user_package = PremiumUser.objects.filter(user=user).count()
        #     if user_package == 1:
        #         login_bonus = PremiumLoginBonus.objects.get(pk=1)
        #         UserLogins.objects.create(user=user)
        #         user_wallet.balance = F('balance') + login_bonus.amount
        #         user_wallet.save(update_fields=['balance'])
        #         AllEarnings.objects.create(user=user, amount=login_bonus.amount)
        #         messages.success(self.request, f"Login successful! your wallet have credited with {login_bonus} naira login bonus")
        #     elif user_package < 1:
        #         login_bonus = LoginBonus.objects.get(pk=1)
        #         UserLogins.objects.create(user=user)
        #         user_wallet.balance = F('balance') + login_bonus.amount
        #         user_wallet.save(update_fields=['balance'])
        #         AllEarnings.objects.create(user=user, amount=login_bonus.amount)
        #         messages.success(self.request, f"Login successful {login_bonus} naira login bonus has been added to your wallet")

        return super().get_success_url()


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     current_site = get_current_site(self.request)
    #     print(self.request.user.pk)
    #     print(self.request.user)
    #     # wb = Wallet.objects.get(user=self.request.user)
    #     # print(wb)
    #     context.update({
    #         self.redirect_field_name: self.get_redirect_url(),
    #         'site': current_site,
    #         'site_name': current_site.name,
    #         **(self.extra_context or {})
    #     })
    #     return context





class BlogView(ListView):
    model = Blog
    paginate_by = 4
    context_object_name = 'object'
    template_name="main/blog_list.html"

    queryset = model.objects.filter(status="Published").order_by('-published_on').annotate(comment_count = Count('comment'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # comment_count = Blog.objects.annotate(Count('comment'))
        if user.is_authenticated:
            wallet_balance = Wallet.objects.get(user=user)
            context.update({
                "wallet_balance": wallet_balance.balance,
            })
        # context['now'] = timezone.now()
        return context

class BlogDetailView(DetailView):
    model = Blog
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_slug = self.kwargs['slug']
        blog_comment_form = BlogCommentForm(initial = {"blog_slug":blog_slug}, auto_id=False)

        # Get comment Bonus

        user = self.request.user
        if user.is_authenticated:
            wallet_balance = Wallet.objects.get(user=user)
            user_package = PremiumUser.objects.filter(user=user).count()
            if user_package == 1:
                comment_bonus = PremiumUserCommentBonus.objects.get(pk=1) or 0.00
            elif user_package == 0:
                comment_bonus = CommentBonus.objects.get(pk=1) or 0.00
            context.update({
                "wallet_balance": wallet_balance.balance,
                "comment_bonus": comment_bonus.amount,
            })
        like_count = BlogLike.objects.filter(blog__slug=blog_slug).count()
        comment_count = Comment.objects.filter(blog__slug=blog_slug).count()
        comments = Comment.objects.filter(blog__slug=blog_slug).order_by('-commented_on')
        context.update({
            "like_count": like_count,
            "comment_count": comment_count,
            "comments": comments,
            "comment_form": blog_comment_form
        })
        return context

def withdraw_request_view(request):
    if request.method == "POST" or None:
        form = WithdrawRequestForm(data = request.POST)
        # other_data = MemberDataForm(data = request.POST)

        if form.is_valid():
            amount = form.cleaned_data["amount"]
            minimum_withdrawable_amount = MinimumWithdrawAmount.objects.get(pk=1)

            withdrawable_amount = minimum_withdrawable_amount.amount
            wallet_balance = Wallet.objects.get(user=request.user)
            if amount <= int(withdrawable_amount):
                messages.success(request, "Withdraw can not be proccessd because amount is lower than the minimum withdrawable amount", extra_tags="withdraw_submitted_message")
                return redirect('main:profile', pk=request.user.pk)

            if amount > wallet_balance.balance or wallet_balance.balance - amount < 0 :
                messages.success(request, "You don't have up to the requested amount", extra_tags="withdraw_submitted_message")
                return redirect('main:profile', pk=request.user.pk)

            wallet_balance.balance = F('balance') - amount
            wallet_balance.save(update_fields=['balance'])
            withdraw_form = form.save(commit=False)
            withdraw_form.user = request.user
            form.save()
            messages.success(request, "Request sumitted for proccessing", extra_tags="withdraw_submitted_message")
            return redirect('main:profile', pk=request.user.pk)

class UserProfile(SuccessMessageMixin, LoginRequiredMixin, TemplateView, UpdateView):
    form = WithdrawRequestForm()
    model = User
    fields = ["first_name", "last_name", "username", "email", "phone_number"]
    template_name = "main/user_profile.html"
    success_message = "Profile Updated"
    extra_tags ="profile_updated"

    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message, extra_tags=self.extra_tags)
        return response

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        #Get number of referred user daily

        now = timezone.now()
        # Get current day date object
        # like: 12/02/2019 00:00:00
        today = now.replace(hour=0).replace(minute=0).replace(second=0).replace(microsecond=0)

        # Get the client from the user object
        user = self.request.user
        daily_referred_count = User.object.filter(
            referrer=user.ref_id,
            registered_on__gte=today,
            registered_on__lte=today + timedelta(days=1)
        ).count()

        # Get total number of reffered user
        total_referred_count = User.object.filter(
            referrer=user.ref_id
        ).count()

        # Get number of reffered premium user
        premium_reffered_user = PremiumUser.objects.filter(
        user__referrer=user.ref_id
        ).count()
        # GEt all earnings
        all_ernings = AllEarnings.objects.filter(user=user).aggregate(Sum("amount"))['amount__sum'] or 0.00

        try:
            withdraw_amount = MinimumWithdrawAmount.objects.get(pk=1)

        except e.ObjectDoesNotExist:
             withdraw_amount = MinimumWithdrawAmount.objects.create(amount=0)


        wallet_balance = Wallet.objects.get(user=self.request.user)
        context.update({
        "wallet_balance":wallet_balance.balance,
        "today_referred":daily_referred_count,
        "total_referred":total_referred_count,
        "premium_user":premium_reffered_user,
        "all_ernings":all_ernings,
        "minimum_withdraw_amount":withdraw_amount,
        "withdraw_form":self.form
        })

        return context

def comment_proccess(request):
    if request.method == "POST" or None:
        comment =  BlogCommentForm(data = request.POST)
        user = request.user
        if user.is_authenticated:

            if comment.is_valid():
                blog_slug = comment.cleaned_data["blog_slug"]
                blog_obj = Blog.objects.get(slug=blog_slug) or None
                comment_inst = comment.save(commit=False)

                comment_inst.blog = blog_obj
                comment_inst.user = user
                comment_inst.save()
                # Comment Reward
                comment_count = Comment.objects.filter(blog=blog_obj, user=user).count()
                if comment_count == 1:
                    # Get user package
                    # Check if reward is still available
                    bonus_end = blog_obj.published_on + timedelta(hours=12)
                    if not timezone.now() >= bonus_end:
                        user_wallet = Wallet.objects.get(user=user)
                        user_package = PremiumUser.objects.filter(user=user).count()
                        if user_package == 1:
                            comment_bonus = PremiumUserCommentBonus.objects.get(pk=1)
                            user_wallet.balance = F('balance') + comment_bonus.amount
                            user_wallet.save(update_fields=['balance'])
                            AllEarnings.objects.create(user=user, amount=comment_bonus.amount)
                            messages.success(request, "Comment published", extra_tags="comment_published")
                            messages.success(request, f"You have been rewarded with {comment_bonus} naira comment bonus", extra_tags="comment_published")
                        elif user_package < 1:
                            comment_bonus = CommentBonus.objects.get(pk=1)
                            user_wallet.balance = F('balance') + comment_bonus.amount
                            user_wallet.save(update_fields=['balance'])
                            AllEarnings.objects.create(user=user, amount=comment_bonus.amount)
                            messages.success(request, "Comment published", extra_tags="comment_published")
                            messages.success(request, f"You have been rewarded with {comment_bonus} naira comment bonus", extra_tags="comment_published")
                        # response = redirect('main:blog-detail', slug=blog_slug)
                    else:
                        messages.success(request, "Comment published", extra_tags="comment_published")
                else:
                    messages.success(request, "Comment published", extra_tags="comment_published")
                response = redirect('main:blog-detail', slug=blog_slug)
        else:
            messages.info(request, "Login is required to post a comment")
            response = redirect("main:login")
    return response

def blog_like(request):
    if request.is_ajax or None:
        blog_slug = request.GET.get("blog_slug")
        # print(username)
        user = request.user
        if user.is_authenticated:
            blog_obj = Blog.objects.get(slug=blog_slug) or None
            blog_like_count = BlogLike.objects.filter(blog=blog_obj, user=user).count() # Blog like Reward
            all_blog_like_count = BlogLike.objects.filter(blog=blog_obj).count()
            if blog_like_count == 0:
                try:
                    BlogLike.objects.create(blog=blog_obj, user=user, status=True)
                except Exception as e:
                    print(e)

                # Check if reward is still available
                bonus_end = blog_obj.published_on + timedelta(hours=12)
                if not timezone.now() >= bonus_end:
                    user_wallet = Wallet.objects.get(user=user)
                    user_package = PremiumUser.objects.filter(user=user).count()
                    if user_package == 1:
                        blog_like_bonus = PremiumBlogLikeBonus.objects.get(pk=1)
                        user_wallet.balance = F('balance') + blog_like_bonus.amount
                        user_wallet.save(update_fields=['balance'])
                        AllEarnings.objects.create(user=user, amount=blog_like_bonus.amount)
                    elif user_package < 1:
                        blog_like_bonus = BlogLikeBonus.objects.get(pk=1)
                        user_wallet.balance = F('balance') + blog_like_bonus.amount
                        user_wallet.save(update_fields=['balance'])
                        AllEarnings.objects.create(user=user, amount=blog_like_bonus.amount)

                response = JsonResponse({"liked": True, "all_like":all_blog_like_count}, status=200)
            else:
                response = JsonResponse({"liked": True, "all_like":all_blog_like_count}, status=200)
        else:
            response = JsonResponse({"liked": False}, status=200)
    #
    return response


def forgot_pass(request):

    # form = PasswordResetEmailForm()
    if request.is_ajax and request.method == "POST" or None:
        email =  request.POST.get('email')

        # if form.is_valid():
        current_site = get_current_site(request)
        print(email)
        try:
            user = User.object.get(email=email)
            subject = 'Password Reset'
            message = render_to_string('main/password_reset_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_mail(
                subject,
                message,
                # f"admin@{current_site.domain}",
                "simplerefers@gmail.com",
                [user.email],
                fail_silently=False,
            )
            # user.email_user(subject, message)


            response = JsonResponse({"code":1}, status=200)

        except e.ObjectDoesNotExist:
            # raise forms.ValidationError("You have forgotten about Fred!")
            response = JsonResponse({"code":0}, status=400)



    return response


def validate_password_reset_link(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.object.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
        messages.error(request, "Error occured!")

    if user is not None and account_activation_token.check_token(user, token):
        action = redirect('main:reset-password', pk=user.pk)
    else:
        messages.error(request, "Password reset failed")
        action =  redirect('main:forgot-password')
    return action


def reset_password(request, pk):
    form = ResetPasswordForm()

    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            pass1 = form.cleaned_data["password1"]
            pass2 = form.cleaned_data["password2"]

            if pass1 != pass2:
                messages.error(request, "Password must match")
            else:

                try:
                    user = User.object.get(pk=pk)
                    user.set_password(pass1)
                    user.save()
                    messages.success(request, "Password changed successfully")
                except e.ObjectDoesNotExist:
                    messages.error(request, "Password reset failed")

    return render(request, "main/password_reset.html", {"form":form})
