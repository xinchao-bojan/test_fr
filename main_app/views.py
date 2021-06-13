from datetime import datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status, permissions

from .serializers import *
from .models import *

'''
Actions for admin
'''

'''
Actions with Interiews
'''


class CreateInterviewView(APIView):
    """Creating an interview"""

    permission_classes = [permissions.IsAdminUser]

    class body(serializers.Serializer):
        title = serializers.CharField()
        description = serializers.CharField()
        date_start = serializers.DateField()
        date_finish = serializers.DateField()

    @swagger_auto_schema(operation_description='Check application by id',
                         request_body=body(),
                         responses={
                             '201': InterviewSerializer(),
                             '400': 'KeyError',
                             '400': 'change date to correct',
                         })
    def post(self, request):
        try:
            title = request.data['title']
            description = request.data['description']
            date_start = datetime.strptime(request.data['date_start'], '%Y-%m-%d').date()
            date_finish = datetime.strptime(request.data['date_finish'], '%Y-%m-%d').date()
        except ValueError:
            return Response('change date to correct', status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response('KeyError', status=status.HTTP_400_BAD_REQUEST)
        if date_start > date_finish:
            return Response('change date to correct', status=status.HTTP_400_BAD_REQUEST)
        i = Interview.objects.create(title=title, date_start=date_start, date_finish=date_finish,
                                     description=description)
        serializer = InterviewSerializer(i, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateInterviewView(APIView):
    """Updating an interview"""

    permission_classes = [permissions.IsAdminUser]

    class body1(serializers.Serializer):
        title = serializers.CharField()
        description = serializers.CharField()
        date_finish = serializers.DateField()

    @swagger_auto_schema(operation_description='Check application by id',
                         request_body=body1(),
                         responses={
                             '200': InterviewSerializer(),
                             '400': 'KeyError',
                             '400': 'change date to correct',
                             '400': 'Interview Does Not Exist',
                         })
    def put(self, request, pk):
        try:
            title = request.data['title']
            description = request.data['description']
            date_finish = datetime.strptime(request.data['date_finish'], '%Y-%m-%d').date()
            i = Interview.objects.get(pk=pk)
        except ValueError:
            return Response('change date to correct', status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response('KeyError', status=status.HTTP_400_BAD_REQUEST)
        except Interview.DoesNotExist:
            return Response('Interview Does Not Exist', status=status.HTTP_400_BAD_REQUEST)
        if i.date_start > date_finish:
            return Response('change date to correct', status=status.HTTP_400_BAD_REQUEST)
        i.title = title
        i.description = description
        i.date_finish = date_finish
        i.save()
        serializer = InterviewSerializer(i, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteInterviewView(APIView):
    """Deleting an interview"""
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(operation_description='Check application by id',
                         responses={
                             '200': 'deleted',
                             '400': 'Interview Does Not Exist',
                         })
    def delete(self, request, pk):
        try:
            i = Interview.objects.get(pk=pk)
        except Interview.DoesNotExist:
            return Response('Interview Does Not Exist', status=status.HTTP_400_BAD_REQUEST)
        i.delete()
        return Response('deleted', status=status.HTTP_200_OK)


'''
Actions with Questions
'''


class CreateChoiceQuestionView(APIView):
    """Creating choices question"""

    permission_classes = [permissions.IsAdminUser]

    class body2(serializers.Serializer):
        class answer(serializers.Serializer):
            text = serializers.CharField()

        text = serializers.CharField()
        multiple_answer = serializers.BooleanField()
        answers = serializers.ListSerializer(child=answer())

    @swagger_auto_schema(operation_description='Check application by id',
                         request_body=body2(),
                         responses={
                             '201': ChoiceSerializer(),
                             '400': 'KeyError',
                             '400': 'Interview Does Not Exist',
                         })
    def post(self, request, pk):
        try:
            text = request.data['text']
            interview = Interview.objects.get(pk=pk)
            multiple_answer = bool(request.data['multiple_answer'])
            answers = request.data['answers']
        except KeyError:
            return Response('KeyError', status=status.HTTP_400_BAD_REQUEST)
        except Interview.DoesNotExist:
            return Response('Interview Does Not Exist', status=status.HTTP_400_BAD_REQUEST)
        q = Choice.objects.create(text=text, interview=interview)
        ChoiceMore.objects.create(choice=q, multiple_answer=multiple_answer)
        for elem in answers:
            try:
                Answer.objects.create(question=q, text=elem['text'])
            except KeyError:
                return Response('KeyError', status=status.HTTP_400_BAD_REQUEST)

        serializer = ChoiceSerializer(q, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateTypingQuestionView(APIView):
    """Creating typing question"""
    permission_classes = [permissions.IsAdminUser]

    class body3(serializers.Serializer):
        text = serializers.CharField()

    @swagger_auto_schema(operation_description='Check application by id',
                         request_body=body3(),
                         responses={
                             '201': TypingSerializer(),
                             '400': 'KeyError',
                             '400': 'Interview Does Not Exist',
                         })
    def post(self, request, pk):
        try:
            text = request.data['text']
            interview = Interview.objects.get(pk=pk)
        except KeyError:
            return Response('KeyError', status=status.HTTP_400_BAD_REQUEST)
        except Interview.DoesNotExist:
            return Response('Interview Does Not Exist', status=status.HTTP_400_BAD_REQUEST)
        q = Typing.objects.create(text=text, interview=interview)
        serializer = TypingSerializer(q, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateQuestionView(APIView):
    """Updating a question"""

    permission_classes = [permissions.IsAdminUser]

    class body4(serializers.Serializer):
        class answer1(serializers.Serializer):
            text = serializers.CharField()

        text = serializers.CharField()
        type = serializers.CharField()
        multiple_answer = serializers.BooleanField()
        answers = serializers.ListSerializer(child=answer1())

    @swagger_auto_schema(operation_description='Check application by id',
                         request_body=body4(),
                         responses={
                             '200': ChoiceSerializer(),
                             '400': 'KeyError',
                             '400': 'Interview Does Not Exist',
                         })
    def put(self, request, interview_pk, question_pk):
        try:
            i = Interview.objects.get(pk=interview_pk)
            q = Question.objects.get(pk=question_pk, interview=i)
            type = request.data['type']
            text = request.data['text']
        except Question.DoesNotExist:
            return Response('Question Does Not Exist', status=status.HTTP_400_BAD_REQUEST)
        except Interview.DoesNotExist:
            return Response('Question Does Not Exist', status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response('KeyError', status=status.HTTP_400_BAD_REQUEST)
        q.text = text
        if type == Question.Types.TYPING:
            if q.type == Question.Types.CHOICE:
                c = Choice.objects.get(pk=q.pk)
                c.more.delete()
            q.answer_set.all().delete()
            q.type = Question.Types.TYPING
            q.save()
            t = Typing.objects.get(pk=q.pk)
            serializer = TypingSerializer(t, context={'request': request})

        elif type == Question.Types.CHOICE:
            q.answer_set.all().delete()
            try:
                c = Choice.objects.get(pk=q.pk)
                c.more.delete()
            except Choice.DoesNotExist:
                q.type = Question.Types.CHOICE
                q.save()
                c = Choice.objects.get(pk=q.pk)
            try:
                multiple_answer = bool(request.data['multiple_answer'])
                answers = request.data['answers']
            except KeyError:
                return Response('KeyError', status=status.HTTP_400_BAD_REQUEST)
            ChoiceMore.objects.create(choice=c, multiple_answer=multiple_answer)
            for elem in answers:
                try:
                    Answer.objects.create(question=q, text=elem['text'])
                except KeyError:
                    return Response('KeyError', status=status.HTTP_400_BAD_REQUEST)
            serializer = ChoiceSerializer(c, context={'request': request})

        else:
            return Response('something went wrong', status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteQuestionView(APIView):
    """Deleting a question"""

    @swagger_auto_schema(operation_description='Check application by id',
                         responses={
                             '200': 'deleted',
                             '400': 'KeyError',
                             '400': 'Question Does Not Exist',
                         })
    def delete(self, request, interview_pk, question_pk):
        try:
            i = Interview.objects.get(pk=interview_pk)
            q = Question.objects.get(pk=question_pk, interview=i)
        except Question.DoesNotExist:
            return Response('Question Does Not Exist', status=status.HTTP_400_BAD_REQUEST)
        except Interview.DoesNotExist:
            return Response('Question Does Not Exist', status=status.HTTP_400_BAD_REQUEST)
        q.answer_set.all().delete()
        try:
            c = Choice.objects.get(pk=q.pk)
            c.more.delete()
            c.delete()
        except Choice.DoesNotExist:
            t = Typing.objects.get(pk=q.pk)
            t.delete()
        return Response('deleted', status=status.HTTP_200_OK)


'''
Actions for user
'''


class ListOfActiveInterviewsView(generics.ListAPIView):
    serializer_class = InterviewSerializer
    """Get list of active interviews"""
    queryset = Interview.objects.filter(date_start__lte=datetime.date(datetime.now()),
                                        date_finish__gte=datetime.date(datetime.now())).order_by('-id')


class PassAnInterviewView(APIView):
    """Pass an interview"""

    @swagger_auto_schema(operation_description='Check application by id',
                         responses={
                             '200': TypingSerializer(many=True),
                             '400': 'Interview Does Not Exist',
                         })
    def get(self, request, interview_pk):
        try:
            i = Interview.objects.get(pk=interview_pk)
        except Interview.DoesNotExist:
            return Response('Interview Does Not Exist', status=status.HTTP_400_BAD_REQUEST)

        serializer1 = ChoiceSerializer(Choice.objects.filter(interview=i), many=True, context={'request': request})
        serializer2 = TypingSerializer(Typing.objects.filter(interview=i), many=True, context={'request': request})
        return Response(serializer1.data + serializer2.data, status=status.HTTP_200_OK)

    class body5(serializers.Serializer):
        class answer2(serializers.Serializer):
            id = serializers.IntegerField()
            type = serializers.CharField()
            choice = serializers.ListSerializer(child=serializers.IntegerField())
            text = serializers.CharField()

        answers = serializers.ListSerializer(child=answer2())

    @swagger_auto_schema(operation_description='Check application by id',
                         request_body=body5(),
                         responses={
                             '200': InterviewSerializer(),
                             '400': 'KeyError',
                             '400': 'Interview Does Not Exist',
                             '400': 'Question Does Not Exist',
                             '400': 'something went wrong',
                         })
    def post(self, request, interview_pk):
        try:
            answers = request.data['answers']
            i = Interview.objects.get(pk=interview_pk)
        except Interview.DoesNotExist:
            return Response('Question Does Not Exist', status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response('KeyError', status=status.HTTP_400_BAD_REQUEST)
        for elem in answers:
            if elem['type'] == "TYPING":
                try:
                    q = Question.objects.get(pk=elem['id'], interview=i)
                    text = elem['text']
                except KeyError:
                    return Response('KeyError', status=status.HTTP_400_BAD_REQUEST)
                except Question.DoesNotExist:
                    return Response('Question Does Not Exist', status=status.HTTP_400_BAD_REQUEST)
                if q.type != Question.Types.TYPING:
                    return Response('something went wrong', status=status.HTTP_400_BAD_REQUEST)
                a = Answer.objects.create(text=text, question=q)
                a.user_set.add(request.user)
            elif elem['type'] == "CHOICE":
                try:
                    q = Question.objects.get(pk=elem['id'], interview=i)
                    choice = elem['choice']
                except KeyError:
                    return Response('KeyError', status=status.HTTP_400_BAD_REQUEST)
                except Question.DoesNotExist:
                    return Response('Question Does Not Exist', status=status.HTTP_400_BAD_REQUEST)
                if q.type != Question.Types.CHOICE:
                    return Response('something went wrong', status=status.HTTP_400_BAD_REQUEST)

                if len(choice) == 1:
                    try:
                        a = Answer.objects.get(question=q, pk=choice[0])
                        a.user_set.add(request.user)
                    except Answer.DoesNotExist:
                        return Response('Answer Does Not Exist', status=status.HTTP_400_BAD_REQUEST)

                elif len(choice) > 1:
                    for answer in choice:
                        try:
                            a = Answer.objects.get(question=q, pk=answer)
                            multiple_answer = Choice.objects.get(pk=q.pk).more.multiple_answer
                            if not multiple_answer:
                                return Response('something went wrong', status=status.HTTP_400_BAD_REQUEST)
                            a.user_set.add(request.user)
                        except Answer.DoesNotExist:
                            return Response('Answer Does Not Exist', status=status.HTTP_400_BAD_REQUEST)
                        except Choice.DoesNotExist:
                            return Response('Choice Does Not Exist', status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response('something went wrong', status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response('something went wrong', status=status.HTTP_400_BAD_REQUEST)
        i.respondents.add(request.user)
        i = Interview.objects.get(pk=i.pk)
        serializer = InterviewSerializer(i, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListOfPassedInterviewsView(APIView):
    """List of passed interviews"""

    def get(self, request):
        user = request.user
        data = []
        for interview in user.interview_set.all():
            unit = {'interview': interview.title}
            body = []
            for question in interview.question_set.all():
                query = question.answer_set.all() & user.answer_set.all()
                if query.count() >= 1:
                    qna = {
                        'question': question.text,
                        'answer': AnswerSerializer(query, context={'request': request}, many=True).data
                    }
                    body.append(qna)
            unit['body'] = body
            data.append(unit)
        return Response(data)
