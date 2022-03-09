from unittest.mock import patch, MagicMock
import jwt

from datetime import datetime

from django.test import TestCase, Client

from quest101.settings import SECRET_KEY, ALGORITHM
from products.models import *
from users.models import *
from users.models import User


class KakaoLoginTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            kakao_id="01924234",
            name="박정현",
            email="hailey@gmail.com",
            profile_image="https://ifh.cc/g/ElNIU1.jpg",
            phone_number="01012341234",
        )

    def tearDown(self):
        User.objects.all().delete()

    @patch('users.views.requests')
    def test_kakaologinview_get_success(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "id": 2008761000,
                    "connected_at": "2021-12-10T03:56:15Z",
                    "properties": {
                        "nickname": "박정현",
                        "profile_image": "https://ifh.cc/g/ElNIU1.jpg",
                        "thumbnail_image": "https://ifh.cc/g/ElNIU1.jpg"
                    },
                    "kakao_account": {
                        "profile_needs_agreement": False,
                        "profile": {
                            "nickname": "박정현",
                            "thumbnail_image_url": "https://ifh.cc/g/ElNIU1.jpg",
                            "profile_image_url": "https://ifh.cc/g/ElNIU1.jpg",
                            "is_default_image": False
                        },
                        "has_email": True,
                        "email_needs_agreement": False,
                        "is_email_valid": True,
                        "is_email_verified": True,
                        "email": "hailey@gmail.com",
                        "has_phone_number": True,
                        "phone_number_needs_agreement": False,
                        "phone_number": "+82 10-9109-5601",
                        "has_birthday": True,
                        "birthday_needs_agreement": True,
                        "has_gender": True,
                        "gender_needs_agreement": False,
                        "gender": "female",
                        "is_kakaotalk_user": True
                    }
                }

        mocked_requests.get = MagicMock(return_value=MockedResponse())
        headers = {"HTTP_Authorization": "가짜 access_token"}
        response = client.get("/users/kakaosignin", **headers)

        access_token = response.json()['access_token']

        self.assertEqual(response.json(), {'message': 'SUCCESS', 'access_token': access_token})
        self.assertEqual(response.status_code, 200 | 201)


class CommentTest(TestCase):
    def setUp(self):
        User.objects.bulk_create(
            [
                User(
                    id=1,
                    name='a',
                    profile_image='a',
                    description='a',
                    kakao_id=1,
                    is_creator=False,
                ),
                User(
                    id=2,
                    name='b',
                    description='b',
                    kakao_id=2,
                    is_creator=True
                )
            ]
        )
        SubCategory.objects.create(
            id=1,
            name='a1',
            category_id=1
        )
        Level.objects.create(
            id=1,
            level='a'
        )
        Course.objects.bulk_create(
            [
                User(
                    id=1,
                    name='a',
                    thumbnail_image_url='a',
                    description='a',
                    price=100,
                    start_date=datetime(2021, 12, 12, 12, 12, 1),
                    end_date=datetime(2021, 12, 12, 12, 12, 2),
                    payment_period=1,
                    user_id=2,
                    sub_category_id=1,
                    level_id=1),
                User(
                    id=2,
                    name='b',
                    thumbnail_image_url='b',
                    description='b',
                    price=100,
                    start_date=datetime(2021, 12, 12, 12, 12, 1),
                    end_date=datetime(2021, 12, 12, 12, 12, 2),
                    payment_period=2,
                    user_id=2,
                    sub_category_id=1,
                    level_id=1
                )
            ]
        )
        Stat.objects.bulk_create(
            [
                Stat(id=1, name='a'),
                Stat(id=2, name='b'),
                Stat(id=3, name='c'),
                Stat(id=4, name='d')
            ]
        )

        CourseStat.objects.bulk_create(
            [
                CourseStat(
                    id=1,
                    course_id=1,
                    stat_id=1,
                    score=3
                ),
                CourseStat(
                    id=2,
                    course_id=1,
                    stat_id=2,
                    score=1
                ),
                CourseStat(
                    id=3,
                    course_id=1,
                    stat_id=3,
                    score=2
                ),
                CourseStat(
                    id=4,
                    course_id=1,
                    stat_id=4,
                    score=6
                )
            ]
        )
        UserCourseStat.objects.bulk_create(
            [
                UserCourseStat(
                    id=1,
                    user_id=1,
                    course_stat_id=1
                ),
                UserCourseStat(
                    id=2,
                    user_id=1,
                    course_stat_id=2
                ),
                UserCourseStat(
                    id=3,
                    user_id=1,
                    course_stat_id=3
                ),
                UserCourseStat(
                    id=4,
                    user_id=1,
                    course_stat_id=4
                )
            ]
        )
        self.token = jwt.encode({'user': 1}, SECRET_KEY, ALGORITHM)

    def tearDown(self):
        User.objects.all().delete()
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Level.objects.all().delete()
        Course.objects.all().delete()
        CourseStat.objects.all().delete()
        UserCourseStat.objects.all().delete()

    def test_user_get_success(self):
        client = Client()
        header = {"HTTP_Authorization": self.token}
        result = {
            "id": 1,
            "name": "a",
            "stats": [
                {
                    "stat_name": "a",
                    "stat": 3
                },
                {
                    "stat_name": "b",
                    "stat": 1
                },
                {
                    "stat_name": "c",
                    "stat": 2
                },
                {
                    "stat_name": "d",
                    "stat": 6
                }]
        }

        response = client.get('/users/user', **header, content_type='application/json')

        self.assertEqual(response.json(), {'result': result})
        self.assertEqual(response.status_code, 200)
