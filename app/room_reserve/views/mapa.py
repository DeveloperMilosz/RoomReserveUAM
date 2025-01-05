from django.shortcuts import render, get_object_or_404
from room_reserve.models import RoomPlan, Room, Meeting
from django.utils.timezone import now
from django.db.models import Exists, OuterRef


def building_plan_view(request, building_name, floor):
    current_time = now()
    plans = (
        RoomPlan.objects.filter(building_name=building_name, floor=floor)
        .select_related("room")
        .annotate(
            is_busy=Exists(
                Meeting.objects.filter(room=OuterRef("room"), start_time__lte=current_time, end_time__gte=current_time)
            )
        )
    )
    plan_image = plans.first().plan_image.url if plans.exists() and plans.first().plan_image else None

    return render(
        request,
        "pages/building_plan.html",
        {
            "plans": plans,
            "plan_image": plan_image,
            "building_name": building_name,
            "floor": floor,
        },
    )


def building_plan_view(request, building_name, floor):
    current_time = now()
    plans = (
        RoomPlan.objects.filter(building_name=building_name, floor=floor)
        .select_related("room")
        .annotate(
            is_busy=Exists(
                Meeting.objects.filter(room=OuterRef("room"), start_time__lte=current_time, end_time__gte=current_time)
            )
        )
    )
    plan_image = plans.first().plan_image.url if plans.exists() else None

    return render(
        request,
        "pages/building_plan.html",
        {
            "plans": plans,
            "plan_image": plan_image,
            "building_name": building_name,
            "floor": floor,
        },
    )
