# from allauth.account.adapter import DefaultAccountAdapter
# from allauth.account.utils import user_field
#
#
# class CustomAccountAdapter(DefaultAccountAdapter):
#     def save_user(self, request, user, form, commit=True):
#         # data = form.cleaned_data
#         # user = super().save_user(request, user, form, False)
#         # nickname = data.get("nickname")
#         # if nickname:
#         #     user.nickname = nickname
#         #
#         # user.save()
#         # print('adapter is working ---------------------')
#         # return user
#
#         user = super().save_user(request, user, form, False)
#         user_field(user, 'nickname', request.data.get('nickname'))
#         user.save()
#         return user
