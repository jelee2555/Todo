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
    def get_object(self, pk):
        try:
            task = Task.objects.get(pk=pk)
            return task
        except Task.DoesNotExist:
            return None

    # 01-01 task 조회
    def get(self, request, pk):
        task = self.get_object(pk)
        if task is not None:
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': '해당 id의 task가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    # 01-03 task 수정
    def patch(self, request, pk):
        task = self.get_object(pk)
        if task is None:
            return Response({'message': '해당 id의 task가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 01-04 task 삭제
    def delete(self, request, pk):
        task = self.get_object(pk)
        if task is not None:
            task.delete()
            return Response({'message': 'task가 정상적으로 삭제되었습니다.'}, status=status.HTTP_200_OK)
        return Response({'message': '해당 id의 task가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)


class TaskListAPIView(APIView):
    def get(self, request):
        queryset = Task.objects.all()
        date = self.request.query_params.get('date')
        # 02-01 task list 불러오기
        if date is None:
            serializer = TaskSerializer(queryset, many=True)
        # 03-01 날짜별 task list 불러오기
        else:
            queryset = queryset.filter(task_date=date)
            serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)