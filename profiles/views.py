from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Profile
from .serializers import ProfileSerializer, ProfileListSerializer
from .services import get_name_data, ExternalAPIException


CORS_HEADER = {"Access-Control-Allow-Origin": "*"}


class ProfileListCreateView(APIView):

    def get(self, request):
        queryset = Profile.objects.all()

        gender = request.query_params.get("gender")
        country_id = request.query_params.get("country_id")
        age_group = request.query_params.get("age_group")

        if gender:
            queryset = queryset.filter(gender__iexact=gender)

        if country_id:
            queryset = queryset.filter(country_id__iexact=country_id)

        if age_group:
            queryset = queryset.filter(age_group__iexact=age_group)

        serializer = ProfileListSerializer(queryset, many=True)

        return Response(
            {
                "status": "success",
                "count": queryset.count(),
                "data": serializer.data,
            },
            status=200,
            headers=CORS_HEADER,
        )

    def post(self, request):
        name = request.data.get("name")

        #Validation
        if name is None or name == "":
            return Response(
                {"status": "error", "message": "Missing or empty name"},
                status=400,
                headers=CORS_HEADER,
            )

        if not isinstance(name, str):
            return Response(
                {"status": "error", "message": "Invalid type"},
                status=422,
                headers=CORS_HEADER,
            )

        name = name.strip().lower()

        #Idempotency
        existing = Profile.objects.filter(name__iexact=name).first()
        if existing:
            return Response(
                {
                    "status": "success",
                    "message": "Profile already exists",
                    "data": ProfileSerializer(existing).data,
                },
                status=200,
                headers=CORS_HEADER,
            )

        #External APIs
        try:
            data = get_name_data(name)
        except ExternalAPIException as e:
            return Response(
                {
                    "status": "error",
                    "message": f"{e.api_name} returned an invalid response",
                },
                status=502,
                headers=CORS_HEADER,
            )
        except Exception:
            return Response(
                {"status": "error", "message": "Server error"},
                status=500,
                headers=CORS_HEADER,
            )

        #Save
        profile = Profile.objects.create(
            name=name,
            **data,
        )

        return Response(
            {
                "status": "success",
                "data": ProfileSerializer(profile).data,
            },
            status=201,
            headers=CORS_HEADER,
        )


class ProfileDetailView(APIView):

    def get(self, request, id):
        try:
            profile = Profile.objects.get(id=id)
        except Profile.DoesNotExist:
            return Response(
                {"status": "error", "message": "Profile not found"},
                status=404,
                headers=CORS_HEADER,
            )

        return Response(
            {"status": "success", "data": ProfileSerializer(profile).data},
            status=200,
            headers=CORS_HEADER,
        )

    def delete(self, request, id):
        try:
            profile = Profile.objects.get(id=id)
        except Profile.DoesNotExist:
            return Response(
                {"status": "error", "message": "Profile not found"},
                status=404,
                headers=CORS_HEADER,
            )

        profile.delete()
        return Response(status=204, headers=CORS_HEADER)