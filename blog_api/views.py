from rest_framework import generics
from blog.models import Post
from .serializers import *
from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAdminUser, DjangoModelPermissions




class PostUserWritePermission(BasePermission):
    message = 'Editing posts is restricted to the author only'

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user


class PostList(generics.ListCreateAPIView):
    permission_classes = [DjangoModelPermissions]
    # queryset = Post.postobjects.all()
    serializer_class = PostSerializer

    def get_queryset(self):

        if not self.request.user.is_superuser:
            return Post.objects.filter(author=self.request.user, status='published')

        return Post.objects.filter(status='published')


    # def get_serializer_class(self):
    #     if self.request.user.is_superuser:
    #         return PostSerializer
    #     return PostUserSerializer


    def perform_create(self, serializer):
        # if self.request.user.is_superuser:
        #     serializer.save()
        # else:
        #     serializer.save(author=self.request.user)
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView, PostUserWritePermission):
    permission_classes = [PostUserWritePermission]
    queryset = Post.objects.all()
    serializer_class = PostSerializer






