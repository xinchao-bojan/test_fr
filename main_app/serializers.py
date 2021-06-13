from rest_framework import serializers
from .models import *


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class TypingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Typing
        fields = '__all__'

    answer_set = AnswerSerializer(many=True)


class ChoiceMoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoiceMore
        fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Typing
        fields = '__all__'

    more = ChoiceMoreSerializer()
    answer_set = AnswerSerializer(many=True)


class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = '__all__'

    # question_set = QuestionSerializer(many=True)
