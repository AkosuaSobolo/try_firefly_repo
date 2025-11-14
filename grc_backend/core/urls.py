from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"teams", views.TeamViewSet)
router.register(r"registrations", views.RegistrationViewSet)
router.register(r"articles", views.ArticleViewSet)
router.register(r"faqs", views.FAQViewSet)

urlpatterns = router.urls
