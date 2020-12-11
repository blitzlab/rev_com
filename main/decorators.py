from .extends import *
def login_reward(func):
    def reward_user(user):

        now = timezone.now()
        # Get current day date object
        # like: 12/02/2019 00:00:00
        today = now.replace(hour=0).replace(minute=0).replace(second=0).replace(microsecond=0)


        user_logins = UserLogins.objects.filter(
            user=user,
            date__gte=today,
            date__lte=today + timedelta(days=1)
        ).count()
        if user_logins < 1:
            user_wallet = Wallet.objects.get(user=user)
            user_package = PremiumUser.objects.filter(user=user).count()
            if user_package == 1:
                login_bonus = PremiumLoginBonus.objects.get(pk=1)
                UserLogins.objects.create(user=user)
                user_wallet.balance = F('balance') + login_bonus.amount
                user_wallet.save(update_fields=['balance'])
                AllEarnings.objects.create(user=user, amount=login_bonus.amount)
                messages.success(self.request, f"Login successful! your wallet have credited with {login_bonus} naira login bonus")
            elif user_package < 1:
                login_bonus = LoginBonus.objects.get(pk=1)
                UserLogins.objects.create(user=user)
                user_wallet.balance = F('balance') + login_bonus.amount
                user_wallet.save(update_fields=['balance'])
                AllEarnings.objects.create(user=user, amount=login_bonus.amount)
                messages.success(self.request, f"Login successful {login_bonus} naira login bonus has been added to your wallet")
        print("It worked")
        return func(user)
    return reward_user
