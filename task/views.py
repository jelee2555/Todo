from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from task.models import Task
from task.serializers import TaskSerializer


class TaskAPIView(APIView):
    # 01-02 task 생성
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskEachAPIView(APIView):
    # 01-01 task 조회
    def get(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({'message': '해당 id의 task가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)





class TaskListAPIView(APIView):
    # 02-01 task list 불러오기
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskDateListAPIView(APIView):
    # 03-01 날짜별 task list 불러오기
    def get(self, request):
        queryset = Task.objects.all()
        date = self.request.query_params.get('date')
        if date is not None:
            queryset = queryset.filter(task_date=date)
            serializer = TaskSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)



