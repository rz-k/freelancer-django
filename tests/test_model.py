from django.test import TestCase
from freelancer.account.models import User, Profile, avatar_directory_path


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