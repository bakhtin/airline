from django.urls import path
import blog.views
from blog.views import PostDetailView

urlpatterns = [
    path('', blog.views.news),
    path('<int:pk>/', PostDetailView.as_view()),
]
