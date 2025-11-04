from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Note
from .serializers import RegisterSerializer, LoginSerializer, NoteSerializer


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health(request):
    """Health check endpoint."""
    return Response({"message": "Server is up!"})


class IsOwner(permissions.BasePermission):
    """Permission to ensure user only accesses own objects."""
    # PUBLIC_INTERFACE
    def has_object_permission(self, request, view, obj):
        """This is a public function."""
        return getattr(obj, "user_id", None) == request.user.id


class RegisterView(generics.CreateAPIView):
    """
    Create a new user account.

    Request:
      - username: string
      - email: string (optional)
      - password: string (min 8)
    Response: created user info (id, username, email).
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(APIView):
    """
    Log a user in using session authentication.

    Request:
      - username
      - password
    Response: { message: "Logged in" }
    """
    permission_classes = [permissions.AllowAny]

    # PUBLIC_INTERFACE
    def post(self, request):
        """This is a public function."""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request, user)
        return Response({"message": "Logged in"}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    Log the current user out (session based).
    """
    permission_classes = [permissions.IsAuthenticated]

    # PUBLIC_INTERFACE
    def post(self, request):
        """This is a public function."""
        django_logout(request)
        return Response({"message": "Logged out"}, status=status.HTTP_200_OK)


class NoteViewSet(viewsets.ModelViewSet):
    """
    CRUD endpoints for Notes under /api/notes/.

    - list: List notes for the authenticated user, filter by ?archived=true/false (optional).
    - retrieve: Get a note owned by the user.
    - create: Create a note for the user.
    - update/partial_update: Update a note (owner required).
    - destroy: Delete a note.
    - archive: POST /api/notes/{id}/archive/
    - unarchive: POST /api/notes/{id}/unarchive/
    """
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        qs = Note.objects.filter(user=self.request.user)
        archived = self.request.query_params.get("archived")
        if archived is not None:
            if archived.lower() in ("1", "true", "yes"):
                qs = qs.filter(is_archived=True)
            elif archived.lower() in ("0", "false", "no"):
                qs = qs.filter(is_archived=False)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"], url_path="archive", permission_classes=[permissions.IsAuthenticated, IsOwner])
    def archive(self, request, pk=None):
        note = self.get_object()
        note.is_archived = True
        note.save(update_fields=["is_archived", "updated_at"])
        return Response(self.get_serializer(note).data)

    @action(detail=True, methods=["post"], url_path="unarchive", permission_classes=[permissions.IsAuthenticated, IsOwner])
    def unarchive(self, request, pk=None):
        note = self.get_object()
        note.is_archived = False
        note.save(update_fields=["is_archived", "updated_at"])
        return Response(self.get_serializer(note).data)
