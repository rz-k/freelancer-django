from django.test import TestCase
from django.contrib.admin.sites import AdminSite
# Account
from freelancer.account.admin import ApprovedUserFilter, UserProfileAdmin
from freelancer.account.models import Profile, User
# Project
from freelancer.project.admin import CategoryFilter
from freelancer.project.models import Category


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
        self.assertGreaterEqual(queryset.count(), 1)

    def test_admin_approved_users(self):
        """Test approved users"""
        self.profile.approved = True
        self.profile.save()

        approved_list_filter = ApprovedUserFilter(
            request=None, params={"user_status": "approved"}, model=None, model_admin=None)
        queryset = approved_list_filter.queryset(
            request=None, queryset=self.users)
        self.assertEqual(queryset.count(), 2)

    def test_admin_all_users(self):
        """Test all users(approved and unapproved)"""
        none_list_filter = ApprovedUserFilter(
            request=None, params={"user_status": ""}, model=None, model_admin=None)
        queryset = none_list_filter.queryset(
            request=None, queryset=self.users)
        self.assertGreaterEqual(queryset.count(), 1)

    def test_admin_is_approved_user(self):
        """Test 'is_approved' method field in 'list_display'"""
        self.profile.approved = True
        self.profile.save()

        is_approved_user = self.app_admin.is_approved(self.users.get(id=1))
        is_unapproved_user = self.app_admin.is_approved(self.users.get(id=3))
        self.assertTrue(is_approved_user)
        self.assertFalse(is_unapproved_user)


class ProjectAdminTestCase(TestCase):
    fixtures = ["dev_initial_data.json"]

    def setUp(self) -> None:
        self.category = Category.objects.all()

    def test_admin_category_parent(self):
        children_list_filter = CategoryFilter(
            request=None, params={"category_type": "parent"}, model=None, model_admin=None)
        queryset = children_list_filter.queryset(
            request=None, queryset=self.category)
        self.assertGreaterEqual(queryset.count(), 1)

    def test_admin_category_children(self):
        parent_list_filter = CategoryFilter(
            request=None, params={"category_type": "children"}, model=None, model_admin=None)
        queryset = parent_list_filter.queryset(
            request=None, queryset=self.category)
        self.assertGreaterEqual(queryset.count(), 1)

    def test_admin_category_all(self):
        parent_list_filter = CategoryFilter(
            request=None, params={"category_type": "all"}, model=None, model_admin=None)
        queryset = parent_list_filter.queryset(
            request=None, queryset=self.category)
        self.assertGreaterEqual(queryset.count(), 1)