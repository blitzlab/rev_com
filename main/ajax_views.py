from .extends import *

def forgot_pass_ajax(request):

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


def signup_ajax(request):
    if request.is_ajax or None:
        signup_form = UserSignUpForm(data = request.POST)

        if signup_form.is_valid():
            # refid = signup_form.cleaned_data["refid"]
            user = signup_form.save(commit = False)


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

            response = JsonResponse({"code":1}, status=200)
        else:
            response = JsonResponse({"code":0}, status=400)
            # return render(request, "main/user_signup.html", {"signup":signup_form })

    return response

def login_ajax(request):
    if request.is_ajax or None:
        email =  request.POST.get('email')
        password =  request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is None:
            return JsonResponse({"code":0}, status=400)

        @login_reward
        def login_user(user):
            return login(request, user)

        login_user(user)
    return JsonResponse({"code":1, "userid":user.pk}, status=200)
