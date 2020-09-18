from django.contrib.auth.decorators import login_required
from django.urls import path, include
from . import views

app_name = 'quiz'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('', include("django.contrib.auth.urls")),
    path('<int:pk>/', login_required(views.QuestionsListView.as_view()), name='questionslist'),
    path('<int:pk>/question', login_required(views.QuestionView.as_view()), name='question'),
    path('<int:pk>/results/', login_required(views.ResultsView.as_view()), name='results'),
    path('<int:question_id>/selection/', views.selection, name='selection'),
    path("register/", views.register, name="register"),
    path("about/", views.about, name="about")

]
