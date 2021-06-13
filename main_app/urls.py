from django.urls import path, include

from .views import *

urlpatterns = [
    path('interview/create/', CreateInterviewView.as_view()),
    path('interview/<int:pk>/update/', UpdateInterviewView.as_view()),
    path('interview/<int:pk>/delete', DeleteInterviewView.as_view()),
    path('interview/<int:pk>/question/create/choice/', CreateChoiceQuestionView.as_view()),
    path('interview/<int:pk>/question/create/type/', CreateTypingQuestionView.as_view()),
    path('interview/<int:interview_pk>/question/<int:question_pk>/update/', UpdateQuestionView.as_view()),
    path('interview/<int:interview_pk>/question/<int:question_pk>/delete/', DeleteQuestionView.as_view()),

    path('interview/list/all/', ListOfActiveInterviewsView.as_view()),
    path('interview/<int:interview_pk>/', PassAnInterviewView.as_view()),
    path('interview/list/own/', ListOfPassedInterviewsView.as_view()),

]
