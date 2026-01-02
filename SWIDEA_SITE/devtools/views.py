from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.db.models.deletion import ProtectedError
from django.contrib import messages
from .models import DevTool
from .forms import DevToolForm
from ideas.models import Idea


def devtool_list(request):
    devtools = DevTool.objects.all().order_by("name")
    return render(request, "devtools/devtool_list.html", {"devtools": devtools})


def devtool_create(request):
    if request.method == "POST":
        form = DevToolForm(request.POST)
        if form.is_valid():
            devtool = form.save()
            return redirect("devtools:detail", pk=devtool.pk)
    else:
        form = DevToolForm()
    return render(request, "devtools/devtool_form.html", {"form": form, "mode": "create"})


def devtool_detail(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    ideas = Idea.objects.filter(devtool=devtool).order_by("-created_at")
    return render(request, "devtools/devtool_detail.html", {"devtool": devtool, "ideas": ideas})


def devtool_update(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    if request.method == "POST":
        form = DevToolForm(request.POST, instance=devtool)
        if form.is_valid():
            devtool = form.save()
            return redirect("devtools:detail", pk=devtool.pk)
    else:
        form = DevToolForm(instance=devtool)
    return render(request, "devtools/devtool_form.html", {"form": form, "mode": "update", "devtool": devtool})



@require_POST
def devtool_delete(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)

    try:
        devtool.delete()
        messages.success(request, "개발툴이 삭제되었습니다.")
        return redirect("devtools:list")
    except ProtectedError:
        messages.error(
            request,
            "이 개발툴을 사용하는 아이디어가 있어 삭제할 수 없습니다."
        )
        return redirect("devtools:detail", pk=pk)