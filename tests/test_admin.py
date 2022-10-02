from django.test import TestCase
from django.contrib.admin.sites import AdminSite
# Account
from freelancer.account.admin import ApprovedUserFilter, UserProfileAdmin
from freelancer.account.models import Profile, User


class AccountAdminTestCase(TestCase):
    """Represents a TestCase for the `account model` in `account/admin.py`"""
    fixtures = ["dev_initial_data.json"]

    def setUp(self) -> None:
        self.users = User.objects.all()
        self.profile = Profile.objects.get(user=self.users.get(id=1))
        self.app_admin = UserProfileAdmin(User, AdminSite())

    def test_admin_unapproved_users(self):
        """Test unapproved users"""
        self.profile.approved = False
        self.profile.save()

        unapproved_list_filter = ApprovedUserFilter(
            request=None, params={"user_status": "unapproved"}, model=None, model_admin=None)
        queryset = unapproved_list_filter.queryset(
            request=None, queryset=self.users)
        unapproved_users = queryset.filter(user_profile__approved=False)
        self.assertGreaterEqual(unapproved_users.count(), 1)

    def test_admin_approved_users(self):
        """Test approved users"""
        self.profile.approved = True
        self.profile.save()

        approved_list_filter = ApprovedUserFilter(
            request=None, params={"user_status": "approved"}, model=None, model_admin=None)
        queryset = approved_list_filter.queryset(
            request=None, queryset=self.users)
        approved_users = queryset.filter(user_profile__approved=True)
        self.assertEqual(approved_users.count(), 1)

    def test_admin_all_users(self):
        """Test all users(approved and unapproved)"""
        none_list_filter = ApprovedUserFilter(
            request=None, params={"user_status": ""}, model=None, model_admin=None)
        queryset = none_list_filter.queryset(
            request=None, queryset=self.users)
        all_users = queryset.all()
        self.assertGreaterEqual(all_users.count(), 1)

    def test_admin_is_approved_user(self):
        """Test 'is_approved' method field in 'list_display'"""
        self.profile.approved = True
        self.profile.save()

        is_approved_user = self.app_admin.is_verified(self.users.get(id=1))
        is_unapproved_user = self.app_admin.is_verified(self.users.get(id=2))
        self.assertTrue(is_approved_user)
        self.assertFalse(is_unapproved_user)
