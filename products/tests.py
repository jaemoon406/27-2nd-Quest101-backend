import jwt, json

from django.test import TestCase, Client
from datetime import datetime

from quest101.settings import SECRET_KEY, ALGORITHM
from products.models import *
from users.models import *


class OrderViewTest(TestCase):
    def setUp(self):
        User.objects.bulk_create(
            [
                User(
                    id=1,
                    name="이땡땡",
                    kakao_id=33243,
                    is_creator=False
                ),

                User(
                    id=2,
                    name="김가나",
                    kakao_id=40343,
                    is_creator=True
                )
            ]
        )

        Category.objects.bulk_create(
            [
                Category(
                    id=1,
                    name="category1"
                ),

                Category(
                    id=2,
                    name="category2"
                )
            ]
        )

        SubCategory.objects.bulk_create(
            [
                SubCategory(
                    id=1,
                    name="sports",
                    category_id=2
                ),

                SubCategory(
                    id=2,
                    name="cook",
                    category_id=1
                )
            ]
        )

        Level.objects.bulk_create(
            [
                Level(
                    id=1,
                    level="초급"
                ),

                Level(
                    id=2,
                    level="중급"
                )
            ]
        )

        Course.objects.bulk_create(
            [
                Course(
                    id=1,
                    thumbnail_image_url='ewrrwaa.com',
                    name="Enjoy korean food",
                    price=30000,
                    start_date="2021-12-16",
                    end_date="2021-12-16",
                    payment_period=5,
                    level_id=1,
                    user_id=2,
                    sub_category_id=1
                ),

                Course(
                    id=2,
                    thumbnail_image_url="sjflafj.com",
                    name="Enjoy Sports",
                    price=50000,
                    start_date="2021-12-16",
                    end_date="2021-12-16",
                    payment_period=3,
                    level_id=2,
                    user_id=1,
                    sub_category_id=2
                )
            ]
        )

        Media.objects.bulk_create(
            [
                Media(
                    id=1,
                    url="abc.com",
                    course_id=2
                ),

                Media(
                    id=2,
                    url="def.com",
                    course_id=1
                )
            ]
        )

        UserCourse.objects.create(
            id=1,
            user_id=1,
            course_id=1
        )

        global headers
        token = jwt.encode({'user': 1}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"HTTP_Authorization": token}

    def tearDown(self):
        User.objects.all().delete()
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Course.objects.all().delete()
        Media.objects.all().delete()
        UserCourse.objects.all().delete()
        Level.objects.all().delete()

    def test_orderview_success(self):
        client = Client()
        response = client.post('/products/order/2', **headers)

        self.assertEqual(response.json(),
                         {"message": "SUCCESS"}
                         )

    def test_orderview_user_already_exists(self):
        client = Client()
        response = client.post('/products/order/1', **headers)

        self.assertEqual(response.json(),
                         {"message": "USER ALREADY EXISTS"}
                         )

    def test_orderview_integrity_error(self):
        client = Client()
        response = client.post('/products/order/5', **headers)

        self.assertEqual(response.json(),
                         {"message": "INVALID_VALUE"}
                         )


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
        Category.objects.create(
            id=1,
            name='a'
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
        Comment.objects.bulk_create(
            [
                Comment(
                    id=1,
                    content='a',
                    user_id=1,
                    course_id=1
                ),
                Comment(
                    id=2,
                    content='b',
                    user_id=1,
                    course_id=1
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
        Comment.objects.all().delete()

    def test_comment_post_success(self):
        client = Client()
        header = {"HTTP_Authorization": self.token}

        comment = {
            'course_id': 2,
            'content': 'a'
        }
        result = [{
            'id': 3,
            'name': 'a',
            'content': 'a',
        }]

        response = client.post('/products/comments/2', json.dumps(comment), **header, content_type='application/json')
        self.assertEqual(response.json(), {'message': result})
        self.assertEqual(response.status_code, 201)

    def test_comment_post_key_error(self):
        client = Client()
        header = {"HTTP_Authorization": self.token}

        comment = {}

        response = client.post('/products/comments/1', json.dumps(comment), **header, content_type='application/json')
        self.assertEqual(response.json(), {'message': 'KEY_ERROR'})
        self.assertEqual(response.status_code, 401)

    def test_comment_get_success(self):
        client = Client()
        response = client.get('/products/comments/1')

        course_comments = [
            {
                'id': 1,
                'name': 'a',
                'content': 'a'
            },
            {
                'id': 2,
                'name': 'a',
                'content': 'b'
            }]

        self.assertEqual(response.json(), {'result': course_comments})
        self.assertEqual(response.status_code, 201)

    def test_comment_delete_success(self):
        client = Client()
        header = {"HTTP_Authorization": self.token}

        body = {
            'comment_id': 1
        }

        response = client.delete('/products/comments/1', json.dumps(body), **header)
        self.assertEqual(response.json(), {'message': 'SUCCESS_DELETE'})
        self.assertEqual(response.status_code, 201)

    def test_comment_delete_doesnotexist(self):
        client = Client()
        header = {"HTTP_Authorization": self.token}

        body = {
            'comment_id': 3
        }

        response = client.delete('/products/comments/1', json.dumps(body), **header)
        self.assertEqual(response.json(), {'message': 'INVAILD_COMMENT'})
        self.assertEqual(response.status_code, 401)


class ProductTest(TestCase):

    def setUp(self):
        User.objects.bulk_create(
            [
                User(
                    id=1,
                    name="bear",
                    kakao_id=484248,
                    profile_image="myimage123.com"),
                User(
                    id=2,
                    name="tiger",
                    kakao_id=879845,
                    profile_image="myprofile123.com")
            ]
        )

        Category.objects.bulk_create([
            Category(
                id=1,
                name="category1"),
            Category(
                id=2,
                name="category2")
        ])

        SubCategory.objects.bulk_create([
            SubCategory(
                id=1,
                name="sports",
                category_id=2),
            SubCategory(
                id=2,
                name="cook",
                category_id=1)
        ])

        Level.objects.bulk_create([
            Level(
                id=1,
                level="초급"),
            Level(
                id=2,
                level="중급")
        ])

        Course.objects.bulk_create([
            Course(
                id=1,
                thumbnail_image_url='ewrrwaa.com',
                name="Enjoy korean food",
                price=30000,
                start_date="2021-12-16",
                end_date="2021-12-16",
                payment_period=5,
                level_id=1,
                user_id=2,
                sub_category_id=1,
                discount_rate=30,
                description="abcd"),
            Course(
                id=2,
                thumbnail_image_url="sjflafj.com",
                name="Enjoy Sports",
                price=50000,
                start_date="2021-12-16",
                end_date="2021-12-16",
                payment_period=3,
                level_id=2,
                user_id=1,
                sub_category_id=2,
                discount_rate=20,
                description="efgh")
        ])

        Media.objects.bulk_create([
            Media(
                id=1,
                url="abc.com",
                course_id=2),
            Media(
                id=2,
                url="def.com",
                course_id=1)
        ])

        Like.objects.bulk_create([
            Like(
                id=1,
                course_id=1,
                user_id=2),
            Like(
                id=2,
                course_id=2,
                user_id=1)
        ])

        Stat.objects.bulk_create([
            Stat(
                id=1,
                name="wisdom"),
            Stat(
                id=2,
                name="strength")
        ])

        CourseStat.objects.bulk_create([
            CourseStat(
                id=1,
                stat_id=1,
                course_id=2,
                score=50),
            CourseStat(
                id=2,
                stat_id=2,
                course_id=1,
                score=70
            )
        ])

        global headers
        token = jwt.encode({'user': 2}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"HTTP_Authorization": token}

    def tearDown(self):
        User.objects.all().delete()
        SubCategory.objects.all().delete()
        Course.objects.all().delete()
        Media.objects.all().delete()
        Like.objects.all().delete()
        Stat.objects.all().delete()
        CourseStat.objects.all().delete()

    def test_productview_get_suceess(self):
        client = Client()
        response = client.get('/products/detail/1', **headers)
        self.maxDiff = None

        self.assertEqual(response.json(),
                         {'results': {
                             "course_id": 1,
                             "sub_category": "sports",
                             "course_name": "Enjoy korean food",
                             "thumbnail_url": "ewrrwaa.com",
                             "page_image": "def.com",
                             "course_level": "초급",
                             "price": "30000.00",
                             "payment_period": 5,
                             "discount_rate": 30,
                             "discount_price": "9000.00",
                             "course_like": 1,
                             "course_stat": [{"stat_name": "strength", "score": 70}],
                             "is_like_True": True,
                             "user_name": "tiger",
                             "profile_image": "myprofile123.com",
                             "description": "abcd"
                         }
                         }
                         )

        self.assertEqual(response.status_code, 200)

    def test_productview_get_doesnotexist(self):
        client = Client()
        response = client.get('/products/detail/3')

        self.assertEqual(response.json(),
                         {"message": "INVALID_COURSE"})

        self.assertEqual(response.status_code, 401)


class ProductListTest(TestCase):
    def setUp(self):
        User.objects.bulk_create([
            User(
                id=1,
                name="user1",
                kakao_id=484248),
            User(
                id=2,
                name="user2",
                kakao_id=879845
            )
        ])

        Category.objects.bulk_create([
            Category(
                id=1,
                name="category1"),
            Category(
                id=2,
                name="category2"
            )
        ])

        SubCategory.objects.bulk_create([
            SubCategory(
                id=1,
                name="sub1",
                category_id=2),
            SubCategory(
                id=2,
                name="sub2",
                category_id=1),
            SubCategory(
                id=3,
                name="sub3",
                category_id=1)
        ])

        Level.objects.bulk_create([
            Level(
                id=1,
                level="초급"),
            Level(
                id=2,
                level="중급")
        ])

        Course.objects.bulk_create([
            Course(
                id=1,
                thumbnail_image_url='ewrrwaa.com',
                name="Enjoy korean food",
                price=30000,
                start_date="2021-12-16",
                end_date="2022-12-16",
                payment_period=5,
                level_id=1,
                user_id=2,
                sub_category_id=2),
            Course(
                id=2,
                thumbnail_image_url="sjflafj.com",
                name="Enjoy Sports",
                price=30000,
                start_date="2021-12-16",
                end_date="2022-12-16",
                payment_period=3,
                level_id=2,
                user_id=1,
                sub_category_id=2),
            Course(
                id=3,
                thumbnail_image_url="unsplash123,com",
                name="Enjoy drawing",
                price=30000,
                start_date="2021-12-16",
                end_date="2022-12-16",
                payment_period=3,
                level_id=2,
                user_id=1,
                sub_category_id=1),
            Course(
                id=4,
                thumbnail_image_url="unsplash567,com",
                name="Enjoy best_seller",
                price=30000,
                start_date="2021-12-16",
                end_date="2022-12-16",
                payment_period=5,
                level_id=2,
                user_id=2,
                sub_category_id=1)
        ])

        Like.objects.bulk_create([
            Like(
                id=1,
                course_id=1,
                user_id=2),
            Like(
                id=2,
                course_id=3,
                user_id=1),
        ])

        Stat.objects.bulk_create([
            Stat(
                id=1,
                name="wisdom"),
            Stat(
                id=2,
                name="strength"),
            Stat(
                id=3,
                name="charm"),
            Stat(
                id=4,
                name="artistry")
        ])

        CourseStat.objects.bulk_create([
            CourseStat(
                id=1,
                course_id=1,
                stat_id=1,
                score=50),
            CourseStat(
                id=2,
                course_id=2,
                stat_id=2,
                score=70),
            CourseStat(
                id=3,
                course_id=3,
                stat_id=3,
                score=80),
            CourseStat(
                id=4,
                course_id=4,
                stat_id=4,
                score=70)
        ])

        global headers
        token = jwt.encode({'user': 1}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"HTTP_Authorization": token}

    def tearDown(self):
        User.objects.all().delete()
        SubCategory.objects.all().delete()
        Course.objects.all().delete()
        Like.objects.all().delete()
        Stat.objects.all().delete()
        Level.objects.all().delete()
        CourseStat.objects.all().delete()

    def test_productlist_get_filter_category(self):
        client = Client()
        self.maxDiff = None
        response = client.get('/products?category=category2', **headers)

        self.assertEqual(response.json(),
                         {'results': [{
                             "course_id": 3,
                             "thumbnail": "unsplash123,com",
                             "user_name": "user1",
                             "sub_category": "sub1",
                             "course_name": "Enjoy drawing",
                             "price": "30000.00",
                             "payment_period": 3,
                             "discount_rate": "30%",
                             "discount_price": "10000.00",
                             "course_like": 1,
                             "is_like_True": True
                         },
                             {
                                 "course_id": 4,
                                 "thumbnail": "unsplash567,com",
                                 "user_name": "user2",
                                 "sub_category": "sub1",
                                 "course_name": "Enjoy best_seller",
                                 "price": "30000.00",
                                 "payment_period": 5,
                                 "discount_rate": "30%",
                                 "discount_price": "10000.00",
                                 "course_like": 0,
                                 "is_like_True": False
                             }]
                         }
                         )

        self.assertEqual(response.status_code, 200)

    def test_productlist_get_filter_sub_category(self):
        client = Client()
        self.maxDiff = None
        response = client.get('/products?sub_category=sub2', **headers)

        self.assertEqual(response.json(),
                         {'results': [{
                             "course_id": 1,
                             "thumbnail": "ewrrwaa.com",
                             "user_name": "user2",
                             "sub_category": "sub2",
                             "course_name": "Enjoy korean food",
                             "price": "30000.00",
                             "payment_period": 5,
                             "discount_rate": "30%",
                             "discount_price": "10000.00",
                             "course_like": 1,
                             "is_like_True": False
                         },
                             {
                                 "course_id": 2,
                                 "thumbnail": "sjflafj.com",
                                 "user_name": "user1",
                                 "sub_category": "sub2",
                                 "course_name": "Enjoy Sports",
                                 "price": "30000.00",
                                 "payment_period": 3,
                                 "discount_rate": "30%",
                                 "discount_price": "10000.00",
                                 "course_like": 0,
                                 "is_like_True": False
                             }]
                         }
                         )

        self.assertEqual(response.status_code, 200)

    def test_productlist_get_filter_stat_one(self):
        client = Client()
        self.maxDiff = None
        response = client.get('/products?stat=wisdom', **headers)

        self.assertEqual(response.json(),
                         {"results": [
                             {
                                 "course_id": 1,
                                 "thumbnail": "ewrrwaa.com",
                                 "user_name": "user2",
                                 "sub_category": "sub2",
                                 "course_name": "Enjoy korean food",
                                 "price": "30000.00",
                                 "payment_period": 5,
                                 "discount_rate": "30%",
                                 "discount_price": "10000.00",
                                 "course_like": 1,
                                 "is_like_True": False
                             }
                         ]
                         }
                         )

        self.assertEqual(response.status_code, 200)

    def test_productlist_get_filter_stat1_2(self):
        client = Client()
        self.maxDiff = None
        response = client.get('/products?stat=wisdom&stat=strength', **headers)

        self.assertEqual(response.json(),
                         {'results': [
                             {
                                 "course_id": 2,
                                 "thumbnail": "sjflafj.com",
                                 "user_name": "user1",
                                 "sub_category": "sub2",
                                 "course_name": "Enjoy Sports",
                                 "price": "30000.00",
                                 "payment_period": 3,
                                 "discount_rate": "30%",
                                 "discount_price": "10000.00",
                                 "course_like": 0,
                                 "is_like_True": False
                             },
                             {
                                 "course_id": 1,
                                 "thumbnail": "ewrrwaa.com",
                                 "user_name": "user2",
                                 "sub_category": "sub2",
                                 "course_name": "Enjoy korean food",
                                 "price": "30000.00",
                                 "payment_period": 5,
                                 "discount_rate": "30%",
                                 "discount_price": "10000.00",
                                 "course_like": 1,
                                 "is_like_True": False
                             }
                         ]
                         }
                         )

        self.assertEqual(response.status_code, 200)

    def test_productlist_get_filter_stat1_2_3(self):
        client = Client()
        self.maxDiff = None
        response = client.get('/products?stat=wisdom&stat=strength&stat=charm', **headers)

        self.assertEqual(response.json(),
                         {'results': [
                             {
                                 "course_id": 3,
                                 "thumbnail": "unsplash123,com",
                                 "user_name": "user1",
                                 "sub_category": "sub1",
                                 "course_name": "Enjoy drawing",
                                 "price": "30000.00",
                                 "payment_period": 3,
                                 "discount_rate": "30%",
                                 "discount_price": "10000.00",
                                 "course_like": 1,
                                 "is_like_True": True
                             },
                             {
                                 "course_id": 2,
                                 "thumbnail": "sjflafj.com",
                                 "user_name": "user1",
                                 "sub_category": "sub2",
                                 "course_name": "Enjoy Sports",
                                 "price": "30000.00",
                                 "payment_period": 3,
                                 "discount_rate": "30%",
                                 "discount_price": "10000.00",
                                 "course_like": 0,
                                 "is_like_True": False
                             },
                             {
                                 "course_id": 1,
                                 "thumbnail": "ewrrwaa.com",
                                 "user_name": "user2",
                                 "sub_category": "sub2",
                                 "course_name": "Enjoy korean food",
                                 "price": "30000.00",
                                 "payment_period": 5,
                                 "discount_rate": "30%",
                                 "discount_price": "10000.00",
                                 "course_like": 1,
                                 "is_like_True": False
                             }
                         ]
                         }
                         )

        self.assertEqual(response.status_code, 200)

    def test_productlist_get_filter_stat_all(self):
        client = Client()
        self.maxDiff = None
        response = client.get('/products?stat=wisdom&stat=strength&stat=charm&stat=artistry', **headers)

        self.assertEqual(response.json(),
                         {'results': [
                             {
                                 "course_id": 1,
                                 "thumbnail": "ewrrwaa.com",
                                 "user_name": "user2",
                                 "sub_category": "sub2",
                                 "course_name": "Enjoy korean food",
                                 "price": "30000.00",
                                 "payment_period": 5,
                                 "discount_rate": "30%",
                                 "discount_price": "10000.00",
                                 "course_like": 1,
                                 "is_like_True": False
                             },
                             {
                                 "course_id": 2,
                                 "thumbnail": "sjflafj.com",
                                 "user_name": "user1",
                                 "sub_category": "sub2",
                                 "course_name": "Enjoy Sports",
                                 "price": "30000.00",
                                 "payment_period": 3,
                                 "discount_rate": "30%",
                                 "discount_price": "10000.00",
                                 "course_like": 0,
                                 "is_like_True": False
                             },
                             {
                                 "course_id": 3,
                                 "thumbnail": "unsplash123,com",
                                 "user_name": "user1",
                                 "sub_category": "sub1",
                                 "course_name": "Enjoy drawing",
                                 "price": "30000.00",
                                 "payment_period": 3,
                                 "discount_rate": "30%",
                                 "discount_price": "10000.00",
                                 "course_like": 1,
                                 "is_like_True": True
                             },
                             {
                                 "course_id": 4,
                                 "thumbnail": "unsplash567,com",
                                 "user_name": "user2",
                                 "sub_category": "sub1",
                                 "course_name": "Enjoy best_seller",
                                 "price": "30000.00",
                                 "payment_period": 5,
                                 "discount_rate": "30%",
                                 "discount_price": "10000.00",
                                 "course_like": 0,
                                 "is_like_True": False
                             }
                         ]
                         }
                         )

        self.assertEqual(response.status_code, 200)

    def test_productlist_get_filter_all(self):
        client = Client()
        self.maxDiff = None
        response = client.get('/products?category=category1&sub_category=sub2&stat=strength', **headers)

        self.assertEqual(response.json(),
                         {"results": [{
                             "course_id": 2,
                             "thumbnail": "sjflafj.com",
                             "user_name": "user1",
                             "sub_category": "sub2",
                             "course_name": "Enjoy Sports",
                             "price": "30000.00",
                             "payment_period": 3,
                             "discount_rate": "30%",
                             "discount_price": "10000.00",
                             "course_like": 0,
                             "is_like_True": False
                         }
                         ]
                         }
                         )

        self.assertEqual(response.status_code, 200)


class LikeViewTest(TestCase):
    def setUp(self):
        User.objects.bulk_create([
            User(
                id=1,
                name="bear",
                kakao_id=484248),
            User(
                id=2,
                name="tiger",
                kakao_id=879845)
        ])

        Category.objects.bulk_create([
            Category(
                id=1,
                name="category1"),
            Category(
                id=2,
                name="category2")
        ])

        SubCategory.objects.bulk_create([
            SubCategory(
                id=1,
                name="sports",
                category_id=2),
            SubCategory(
                id=2,
                name="cook",
                category_id=1)
        ])

        Level.objects.bulk_create([
            Level(
                id=1,
                level="초급"),
            Level(
                id=2,
                level="중급")
        ])

        Course.objects.bulk_create([
            Course(
                id=1,
                thumbnail_image_url='ewrrwaa.com',
                name="Enjoy korean food",
                price=30000,
                start_date="2021-12-16",
                end_date="2021-12-16",
                payment_period=5,
                level_id=1,
                user_id=2,
                sub_category_id=1),
            Course(
                id=2,
                thumbnail_image_url="sjflafj.com",
                name="Enjoy Sports",
                price=50000,
                start_date="2021-12-16",
                end_date="2021-12-16",
                payment_period=3,
                level_id=2,
                user_id=1,
                sub_category_id=2)
        ])

        Stat.objects.bulk_create([
            Stat(
                id=1,
                name="wisdom"),
            Stat(
                id=2,
                name="strength"
            )
        ])

        CourseStat.objects.bulk_create([
            CourseStat(
                id=1,
                stat_id=1,
                course_id=2,
                score=50),
            CourseStat(
                id=2,
                stat_id=2,
                course_id=1,
                score=70)
        ])

        Like.objects.create(
            id=1,
            user_id=2,
            course_id=2
        )

        global headers
        token = jwt.encode({'user': 2}, SECRET_KEY, algorithm=ALGORITHM)
        headers = {"HTTP_Authorization": token}

    def tearDown(self):
        User.objects.all().delete()
        SubCategory.objects.all().delete()
        Course.objects.all().delete()
        Like.objects.all().delete()
        Stat.objects.all().delete()
        CourseStat.objects.all().delete()

    def test_post_likeview_success(self):
        client = Client()
        course_id = {"course_id": 1}
        response = client.post('/products/like', json.dumps(course_id), content_type='application/json', **headers)

        self.assertEqual(response.json(),
                         {"message": "SUCCESS_LIKE"}
                         )
        self.assertEqual(response.status_code, 200)

    def test_likeview_post_delete_like(self):
        client = Client()
        course_id = {"course_id": 2}
        response = client.post('/products/like', json.dumps(course_id), content_type='application/json', **headers)

        self.assertEqual(response.json(),
                         {"message": "DELETE_LIKE"})

        self.assertEqual(response.status_code, 200)

    def test_likeviews_integrityerror(self):
        client = Client()
        course_id = {"course_id": 3}
        response = client.post('/products/like', json.dumps(course_id), content_type='application/json', **headers)

        self.assertEqual(response.json(),
                         {"message": "INVALID_VALUE"})

        self.assertEqual(response.status_code, 400)
