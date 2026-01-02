from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Count
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .models import Idea, IdeaStar
from .forms import IdeaForm


def idea_list(request):
    qs = Idea.objects.select_related("devtool").annotate(star_count=Count("stars"))
    sort = request.GET.get("sort", "latest")

    sort_map = {
        "latest": "-created_at",
        "old": "created_at",
        "name": "title",
        "stars": "-star_count",
        "interest": "-interest",
    }
    qs = qs.order_by(sort_map.get(sort, "-created_at"))

    paginator = Paginator(qs, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    starred_ids = set()
    if request.user.is_authenticated:
        starred_ids = set(
            IdeaStar.objects.filter(user=request.user, idea__in=page_obj.object_list)
            .values_list("idea_id", flat=True)
        )

    return render(request, "ideas/idea_list.html", {
        "page_obj": page_obj,
        "sort": sort,
        "starred_ids": starred_ids,
    })


def idea_create(request):
    if request.method == "POST":
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save()
            return redirect("ideas:detail", pk=idea.pk)
    else:
        form = IdeaForm()
    return render(request, "ideas/idea_form.html", {"form": form})


def idea_detail(request, pk):
    idea = get_object_or_404(Idea.objects.select_related("devtool"), pk=pk)
    is_starred = False
    if request.user.is_authenticated:
        is_starred = IdeaStar.objects.filter(user=request.user, idea=idea).exists()

    return render(request, "ideas/idea_detail.html", {
        "idea": idea,
        "is_starred": is_starred,
    })


def idea_update(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if request.method == "POST":
        form = IdeaForm(request.POST, request.FILES, instance=idea)
        if form.is_valid():
            idea = form.save()
            return redirect("ideas:detail", pk=idea.pk)
    else:
        form = IdeaForm(instance=idea)
    return render(request, "ideas/idea_form.html", {"form": form, "idea": idea})


@require_POST
def idea_delete(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    idea.delete()
    return redirect("ideas:list")


@require_POST
def adjust_interest(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    delta = request.POST.get("delta")
    try:
        delta_int = int(delta)
    except (TypeError, ValueError):
        return JsonResponse({"ok": False, "error": "invalid delta"}, status=400)

    idea.interest = max(0, idea.interest + delta_int)
    idea.save(update_fields=["interest"])

    return JsonResponse({"ok": True, "interest": idea.interest})
