from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializer,CategorySerializer
from ...models import Post,Category
from django.shortcuts import get_object_or_404

from rest_framework.decorators import permission_classes
# three type of important permission
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly

from rest_framework.views import APIView

from rest_framework.generics import GenericAPIView, ListAPIView ,ListCreateAPIView
from rest_framework import mixins

from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .permissions import IsOwnerOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter

from .paginations import DefaultPagination

data = {
    'id': 777,
    'name': 'Mohammad Amin Bajelan',
    'job': 'programmer'
}


# @api_view()
# def PostList(request):
#     return Response('Ok')

# @api_view(["GET", "POST"])
# @permission_classes([IsAuthenticated])
# def PostList(request):
#     if request.method == "GET":
#         post = Post.objects.all()
#         serializer = PostSerializer(post, many=True)
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = PostSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

# class PostList(APIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = PostSerializer
#
#     def get(self, request):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = PostSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

class PostList(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()


# @api_view(["GET", "PUT", "DELETE"])
# @permission_classes([IsAuthenticated])
# def PostDetail(request, id):
#     post = get_object_or_404(Post, pk=id)
#     if request.method == "GET":
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#
#     elif request.method == "PUT":
#         serializer = PostSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     elif request.method == "DELETE":
#         post.delete()
#         return Response(data={"detail": "Item delete successfully"}, status=status.HTTP_204_NO_CONTENT)


# class PostDetail(APIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = PostSerializer
#
#     def get(self, request, pk):
#         post = get_object_or_404(Post, pk=pk)
#         serializer = self.serializer_class(post)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, pk):
#         post = get_object_or_404(Post, pk=pk)
#         post.delete()
#         return Response(data={"detail": "Item delete successfully"}, status=status.HTTP_204_NO_CONTENT)

class PostDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()


# class PostViewSet(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = PostSerializer
#     queryset = Post.objects.all()
#
#     def list(self, request):
#         serializer = self.serializer_class(self.queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         post_object = get_object_or_404(Post, pk=pk)
#         serializer = self.serializer_class(post_object)
#         return Response(serializer.data)

class PostModelViewSet(viewsets.ModelViewSet,IsOwnerOrReadOnly):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['category', 'author', 'status']
    search_fields = ['title', 'content']
    ordering_fields = ['published_date']
    pagination_class = DefaultPagination

class CategoryModelViewSet(viewsets.ModelViewSet,IsOwnerOrReadOnly):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()