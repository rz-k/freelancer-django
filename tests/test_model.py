from django.test import TestCase
from datetime import timedelta
from django.utils.text import slugify

# Account
from freelancer.account.models import User, Profile, avatar_directory_path

# FAQ
from freelancer.faq.models import Faq

# Payment
from freelancer.payment.models import Payment

# Pricing
from freelancer.pricing.models import PricingTag, PricingPanel, ActivePricingPanel

# Project
from freelancer.project.models import Category, Project, ApplyProject, Conversation, document_directory_path

# Resume
from freelancer.resume.models import CV, max_value_current_year


class AccountModelTestCase(TestCase):
    fixtures = ["dev_initial_data.json"]

    def setUp(self) -> None:
        self.user = User.objects.first()
        self.profile = Profile.objects.get(user=self.user)
        self.profile.avatar = "users/1/profile/avatar.jpg"
        self.profile.save()

    def test_avatar_dir_path(self):
        file_name = "avatar.jpg"
        dir_path = avatar_directory_path(self, file_name)
        self.assertEqual(dir_path, self.profile.avatar)

    def test_get_avatar_url(self):
        avatar = self.user.get_avatar()
        self.assertEqual(avatar, self.profile.avatar.url)

    def test_get_default_avatar(self):
        self.profile.avatar = ""
        self.profile.save()
        avatar = self.user.get_avatar()
        self.assertNotEqual(avatar, self.profile.avatar)

    def test_str_profile_username(self):
        profile_username = str(self.profile)
        username = self.user.username
        self.assertEqual(profile_username, username)


class FAQModelTestCase(TestCase):
    fixtures = ["dev_initial_data.json"]

    def setUp(self) -> None:
        self.faq = Faq.objects.first()

    def test_str_faq_question_txt(self):
        self.assertEqual(str(self.faq), self.faq.question)


class PaymentModelTestCase(TestCase):
    fixtures = ["dev_initial_data.json"]

    def setUp(self) -> None:
        self.payment = Payment.objects.first()

    def test_str_payment(self):
        username = self.payment.user.username
        payment_type = self.payment.payment_type
        self.assertEqual(str(self.payment), f"{payment_type} | {username}")


class PricingTestCase(TestCase):
    fixtures = ["dev_initial_data.json"]

    def setUp(self) -> None:
        self.tag = PricingTag.objects.first()
        self.pric_panel = PricingPanel.objects.first()
        self.active_panel = ActivePricingPanel.objects.first()

    def test_str_pricing_tag(self):
        name = self.tag.name
        self.assertEqual(str(self.tag), name)

    def test_str_pricing_panel(self):
        panel_type = self.pric_panel.panel_type
        self.assertEqual(str(self.pric_panel), panel_type)

    def test_expire_user_active_pricing_panel(self):
        self.assertTrue(self.active_panel.is_expire())

    def test_not_expire_user_active_pricing_panel(self):
        self.active_panel.expire_time = self.active_panel.expire_time + \
            timedelta(days=60)
        self.assertFalse(self.active_panel.is_expire())

    def test_days_left_to_expire_active_panel(self):
        self.assertLessEqual(self.active_panel.days_left(), 0)

    def test_no_days_left_to_expire_active_panel(self):
        self.active_panel.expire_time = self.active_panel.expire_time + \
            timedelta(days=60)
        self.assertGreater(self.active_panel.days_left(), 0)

    def test_user_has_apply(self):
        self.assertGreater(self.active_panel.has_apply(), 0)

    def test_user_does_not_have_an_apply(self):
        self.active_panel.apply_counter = 500
        self.assertLessEqual(self.active_panel.has_apply(), 0)


class ProjectTestCase(TestCase):
    fixtures = ["dev_initial_data.json"]

    def setUp(self) -> None:
        self.user = User.objects.first()
        self.category = Category.objects.first()
        self.project = Project.objects.first()
        self.conversation = Conversation.objects.first()
        self.apply_project = ApplyProject.objects.first()

    def test_document_dir_path(self):
        file_name = "cv.pdf"
        path = "users/1/conversation/"
        dir_path = document_directory_path(self, file_name)
        self.assertIn(path, dir_path)

    def test_category_str(self):
        name = self.category.name
        self.assertEqual(str(self.category), name)

    def test_project_str(self):
        title = self.project.title
        self.assertEqual(str(self.project), title)

    def test_save_project(self):
        title = "Test slug"
        self.project.title = title
        self.project.save()
        slugify_title = slugify(title)
        self.assertEqual(self.project.slug, slugify_title)

    def test_get_tags_project(self):
        tags = self.project.tags
        join_tags = " ,".join(tags)
        self.assertEqual(self.project.get_tags(), join_tags)

    def test_str_apply_project(self):
        username_title = f"{self.apply_project.user.username} : {self.apply_project.project.title}"
        self.assertEqual(str(self.apply_project), username_title)


class ResumeTestCase(TestCase):
    fixtures = ["dev_initial_data.json"]

    def setUp(self) -> None:
        self.cv = CV.objects.first()

    def test_max_start_work_experience_year(self):
        self.assertIsNone(max_value_current_year(2022))

    def test_max_end_work_experience_year(self):
        self.assertIsNone(max_value_current_year(2022))

    def test_str_cv_email(self):
        email = self.cv.user.email
        self.assertEqual(str(self.cv), email)
