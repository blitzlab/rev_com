from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import views as auth_view
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from .token import account_activation_token
from django.core import exceptions as e
# import requests as req
import pytz
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.db.models import Sum
from paystack.signals import payment_verified
from django.dispatch import receiver
from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, ListView, DetailView
from django.http import JsonResponse
from django.core import serializers
from django.db.models import F
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView
from .models import (User, Wallet, SignupBonus,UserLogins, PremiumUser,
                        LoginBonus, PremiumLoginBonus, ReferBonus,
                            Upgrade, AllEarnings, Blog, Comment,
                                CommentBonus, BlogLike, BlogLikeBonus,
                                    PremiumBlogLikeBonus, PremiumUserCommentBonus,
                                        MinimumWithdrawAmount, PremiumReferBonus,
                                        PremiumUserReferUpgradeBonus)
from django.core.mail import EmailMultiAlternatives
from django.db import IntegrityError
import random
from django.conf import settings
from django.urls import reverse_lazy, reverse
from itertools import chain
from datetime import timedelta
from django.utils import timezone
from .forms import (UserSignUpForm, ContactForm, WithdrawRequestForm,
                        BlogCommentForm, PasswordResetEmailForm,
                        ResetPasswordForm)
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from .decorators import login_reward
