import json
from json import JSONDecodeError

from products.models import Comment
from core.utils import Authorize
from django.db import transaction
from django.views import View
from django.http import JsonResponse
from django.db import IntegrityError
from django.db.models import (Q, F, Sum)
from .models import Like
from users.models import *
from core.utils import AuthorizeProduct


class OrderView(View):
    @Authorize
    def post(self, request, course_id):
        try:
            course_stat_id = CourseStat.objects.filter(course_id=course_id)
            with transaction.atomic():
                for course_stat_ids in course_stat_id:
                    UserCourseStat.objects.create(
                        user_id=request.user.id,
                        course_stat=course_stat_ids
                    )
                UserCourse.objects.create(
                    course_id=course_id,
                    user_id=request.user.id
                )
                return JsonResponse({"message": "SUCCESS"}, status=200)

        except IntegrityError:
            return JsonResponse({"message": "USER ALREADY EXISTS"}, status=401)

        except CourseStat.DoesNotExist:
            return JsonResponse({"message": "INVAILD_COURSE_STAT"}, status=401)


class CommentView(View):
    @Authorize
    def post(self, request, course_id):
        try:
            data = json.loads(request.body)
            user_id = request.user.id

            Comment.objects.create(content=data['content'], course_id=course_id, user_id=user_id)

            comments = Course.objects.get(id=course_id).comment_set.all()
            course_comments = [{
                'id': comment.id,
                'name': comment.user.name,
                'content': comment.content
            } for comment in comments]

            return JsonResponse({'message': course_comments}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=401)

    def get(self, request, course_id):
        try:
            comments = Course.objects.get(id=course_id).comment_set.all()
            course_comments = [{
                'id': comment.id,
                'name': comment.user.name,
                'content': comment.content
            } for comment in comments]

            return JsonResponse({'result': course_comments}, status=200)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=401)

    @Authorize
    def delete(self, request, course_id):
        try:
            user_id = request.user.id
            data = json.loads(request.body)
            comment_id = data['comment_id']

            comment = Comment.objects.get(id=comment_id, user_id=user_id)
            comment.delete()

            return JsonResponse({'message': 'SUCCESS_DELETE'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=401)

        except Comment.DoesNotExist:
            return JsonResponse({'message': 'INVAILD_COMMENT'}, status=401)


class LikeView(View):
    @Authorize
    def post(self, request):
        try:
            data = json.loads(request.body)
            course_id = data["course_id"]

            like, created = Like.objects.get_or_create(course_id=course_id, user_id=request.user.id)

            if not created:
                like.delete()
                return JsonResponse({"message": "DELETE_LIKE"}, status=200)
            return JsonResponse({"message": "SUCCESS_LIKE"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except JSONDecodeError:
            return JsonResponse({"message": "JSON_DECODE_ERROR"}, status=400)

        except IntegrityError:
            return JsonResponse({"message": "INVALID_VALUE"}, status=400)


class ProductView(View):
    @AuthorizeProduct
    def get(self, request, course_id):
        try:
            print(request.body, '========================================')
            course = Course.objects.get(id=course_id)
            stats = course.coursestat_set.all().select_related('stat')
            media = course.media_set.get()

            results = {
                "course_id": course.id,
                "sub_category": course.sub_category.name,
                "course_name": course.name,
                "description": course.description,
                "thumbnail_url": course.thumbnail_image_url,
                "course_level": course.level.level,
                "price": course.price,
                "payment_period": course.payment_period,
                "discount_rate": course.discount_rate,
                "discount_price": course.price * course.discount_rate / 100,
                "page_image": media.url,
                "course_like": course.like_set.count(),
                "charm_stat": 3,
                "art_stat": 5,
                "health_stat": 6,
                "intellect_stat": 10,
                "is_like_True": course.like_set.filter(user=request.user).exists(),
                "user_name": course.user.name,
                "profile_image": course.user.profile_image
            }
            return JsonResponse({"results": results}, status=200)

        except Course.DoesNotExist:

            return JsonResponse({"message": "INVALID_COURSE"}, status=401)


class ProductListView(View):
    @AuthorizeProduct
    def get(self, request):
        category = request.GET.get('category', None)
        sub_category = request.GET.get('sub_category', None)
        stat = request.GET.getlist('stat', None)
        q = Q()

        if category:
            q &= Q(sub_category__category__name=category)

        if sub_category:
            q &= Q(sub_category__name=sub_category)

        if stat:
            q &= Q(coursestat__stat__name__in=stat)

        products = Course.objects.prefetch_related('like_set').filter(q).distinct()

        results = [{"course_id": product.id,
                    "thumbnail": product.thumbnail_image_url,
                    "user_name": product.user.name,
                    "sub_category": product.sub_category.name,
                    "course_name": product.name,
                    "price": product.price,
                    "payment_period": product.payment_period,
                    "discount_rate": product.discount_rate,
                    "discount_price": product.price * product.discount_rate / 100,
                    "course_like": product.like_set.count(),
                    "is_like_True": product.like_set.filter(user=request.user).exists(),

                    } for product in products]

        return JsonResponse({"results": results}, status=200)