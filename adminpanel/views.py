from django.shortcuts import render, redirect,get_object_or_404
from users.decorators import *
from django.contrib.auth.decorators import login_required
from .models import *
from courses.models import Course, Module, Lesson
from .forms import CourseForm,ModuleForm, LessonForm, TestCaseForm, TestCase


@admin_required
def admin_dashboard(request):
    return render(request, "adminpanel/admin_dashboard.html", {
        "course_count": Course.objects.count(),
        "module_count": Module.objects.count(),
        "lesson_count": Lesson.objects.count(),
    })

@login_required
def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("adminpanel:course_list")
    else:
        form = CourseForm()

    return render(request, "adminpanel/add_course.html", {"form": form})

@admin_required
def course_list(request):
    courses = Course.objects.all().order_by("id")
    return render(
        request,
        "adminpanel/course_list.html",
        {"courses": courses}
    )

@admin_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('adminpanel:course_list')
    else:
        form = CourseForm(instance=course)

    return render(request, 'adminpanel/edit_course.html', {'form': form, 'course': course})

@admin_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return redirect('adminpanel:course_list')



@admin_required
def add_module(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            module.save()
            return redirect('adminpanel:course_modules', course_id=module.course.id)
    else:
        form = ModuleForm()

    return render(request, 'adminpanel/add_module.html', {'form': form, 'course': course})

@admin_required
def module_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    modules = course.modules.all() 
    return render(request, 'adminpanel/module_list.html', {'course': course, 'modules': modules})

@admin_required
def edit_module(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    if request.method == "POST":
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            return redirect('adminpanel:course_modules', course_id=module.course.id)
    else:
        form = ModuleForm(instance=module)

    return render(request, 'adminpanel/edit_module.html', {'form': form, 'module': module})

@admin_required
def delete_module(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    course_id = module.course.id
    module.delete()
    return redirect('adminpanel:course_modules', course_id=course_id)

@admin_required
def add_lesson(request, module_id):
    module = get_object_or_404(Module, id=module_id)

    if request.method == "POST":
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.module = module
            lesson.save()
            return redirect('adminpanel:module_lessons', module_id=module.id)
    else:
        form = LessonForm()

    return render(request, 'adminpanel/add_lesson.html', {'form': form, 'module': module})


@admin_required
def lesson_list(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    lessons = module.lessons.all()
    return render(request, 'adminpanel/lesson_list.html', {'module': module, 'lessons': lessons})

@admin_required
def edit_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method == "POST":
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('adminpanel:module_lessons', module_id=lesson.module.id)
    else:
        form = LessonForm(instance=lesson)

    return render(request, 'adminpanel/edit_lesson.html', {'form': form, 'lesson': lesson})

@admin_required
def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    module_id = lesson.module.id
    lesson.delete()
    return redirect('adminpanel:module_lessons', module_id=module_id)

@admin_required
def add_testcase(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method == "POST":
        form = TestCaseForm(request.POST)
        if form.is_valid():
            testcase = form.save(commit=False)
            testcase.lesson = lesson
            testcase.save()
            return redirect(
                "adminpanel:testcase_list",
                lesson_id=lesson.id
            )
    else:
        form = TestCaseForm()

    return render(
        request,
        "adminpanel/add_testcase.html",
        {
            "form": form,
            "lesson": lesson
        }
    )

@admin_required
def testcase_list(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    testcases = lesson.testcases.all()
    return render(request, "adminpanel/testcase_list.html", {"lesson": lesson,"testcases": testcases})

@admin_required
def edit_testcase(request, testcase_id):
    testcase = get_object_or_404(TestCase, id=testcase_id)

    if request.method == "POST":
        form = TestCaseForm(request.POST, instance=testcase)
        if form.is_valid():
            form.save()
            return redirect(
                'adminpanel:testcase_list',
                lesson_id=testcase.lesson.id
            )
    else:
        form = TestCaseForm(instance=testcase)

    return render(
        request,
        'adminpanel/edit_testcase.html',
        {
            'form': form,
            'testcase': testcase
        }
    )

@admin_required
def delete_testcase(request, testcase_id):
    testcase = get_object_or_404(TestCase, id=testcase_id)
    lesson_id = testcase.lesson.id
    testcase.delete()
    return redirect('adminpanel:testcase_list', lesson_id=lesson_id)

