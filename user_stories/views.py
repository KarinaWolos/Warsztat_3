from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views import View
from user_stories.models import *
from django.urls import reverse
from django.utils.datetime_safe import datetime


# Create your views here.

class IndexView(View):
    def get(self, request):
        rooms = Sale.objects.all()
        ctx = dict(
            rooms=rooms
        )
        return render(request, 'user_stories/main.html', context=ctx)


class RoomNewView(View):
    def get(self, request):
        return render(request, "user_stories/add_new_room.html")

    def post(self, request):
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        projector = request.POST.get("projector")

        if projector == "True":
            Sale.objects.create(
                name=name,
                capacity=capacity,
                projector=projector
            )
        else:
            Sale.objects.create(
                name=name,
                capacity=capacity,
                projector="False"
            )

        return HttpResponse(f"Sala {name} została pomyślnie zapisana w bazie danych!")


class RoomModifyView(View):
    def get(self, request, id):
        rooms = Sale.objects.all().filter(id=id)
        return render(request, "user_stories/modify_room.html", {"rooms": rooms})

    def post(self, request, id):
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        projector = request.POST.get("projector")

        if projector == "False":
            Sale.objects.all().filter(id=id).update(
                name=name,
                capacity=capacity,
                projector="True"
            )
        else:
            Sale.objects.all().filter(id=id).update(
                name=name,
                capacity=capacity,
                projector="False"
            )

        return HttpResponse("Dane zostały zedytowane pomyślnie")


class RoomDeleteView(View):
    def get(self, request, id):
        Sale.objects.get(id=id).delete()

        return HttpResponse("Usunięto salę !")


class RoomView(View):
    def get(self, request, id):
        room = Sale.objects.get(id=id)
        return render(request, "user_stories/view_room.html", {"room": room})


class MakeReservation(View):
    def get(self, request, id):
        return render(request, "user_stories/make_reservation.html")

    def post(self, request, id):
        date = request.POST.get("date")
        comment = request.POST.get("comment")
        room = Sale.objects.get(id=id)

        if date < str(datetime.today().date()):
            return HttpResponse("Nie można zarezerwować sali z datą wsteczną")

        elif room.is_unavailable(date) == False:

            Reservation.objects.create(
                date=date,
                comment=comment,
                sale_id=id
            )

            return HttpResponseRedirect(reverse('main'))

        else:

            return HttpResponse("Sala konferencyjna jest zarezerwowana w danym terminie. Proszę podać inną datę")


class RoomSearchView(View):
    def get(self, request):
        return HttpResponseRedirect('main')

    def post(self, request):
        room_name = request.POST.get("room_name")
        min_room_capacity = request.POST.get("min_room_capacity")
        date_reservation = request.POST.get("date_reservation")
        room_projector = request.POST.get("room_projector")

        if not room_name == "":
            rooms = Sale.objects.all().filter(name__icontains=room_name)
            return render(request, 'user_stories/search.html', {"rooms": rooms})

        elif min_room_capacity is not None:
            rooms = Sale.objects.all().filter(capacity__gte=min_room_capacity)
            return render(request, 'user_stories/search.html', {"rooms": rooms})

        elif date_reservation is not None:
            rooms = Sale.objects.all().exclude(reserv__date=date_reservation)
            return render(request, 'user_stories/search.html', {"rooms": rooms})

