from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from courses.models import Course, Lesson
from students.models import LessonProgress
import sys, io
from .code_runner import run_user_code

@login_required
def course_list(request):
    courses = Course.objects.all()
    course_progress = {}
    for course in courses:
        total_lessons = sum(module.lessons.count() for module in course.modules.all())
        completed_lessons = LessonProgress.objects.filter(
            user=request.user, 
            lesson__module__course=course, 
            is_completed=True
        ).count()
        progress_percent = 0
        if total_lessons > 0:
            progress_percent = int(completed_lessons / total_lessons * 100)
        course_progress[course.id] = progress_percent

    return render(request, 'students/course_list.html', {
        'courses': courses,
        'course_progress': course_progress
    })


@login_required
def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    modules = course.modules.prefetch_related('lessons').all()

    # Прогресс по урокам
    lesson_progress = {lp.lesson_id: lp.is_completed for lp in LessonProgress.objects.filter(user=request.user)}

    # Прогресс по модулям
    module_progress = {}
    for module in modules:
        lessons = module.lessons.all()
        total = lessons.count()
        completed = sum(1 for l in lessons if lesson_progress.get(l.id))
        module_progress[module.id] = int((completed / total) * 100) if total > 0 else 0

    return render(request, 'students/course_detail.html', {
        'course': course,
        'modules': modules,
        'lesson_progress': lesson_progress,
        'module_progress': module_progress
    })




@login_required
def lesson_detail(request, lesson_id):
    import io, sys
    from django.contrib import messages

    lesson = get_object_or_404(Lesson, id=lesson_id)
    module = lesson.module
    course = module.course

    # 🔹 очищаем старые сообщения
    storage = messages.get_messages(request)
    for _ in storage:
        pass

    # =============================
    # 1️⃣ Проверка предыдущих модулей
    # =============================
    previous_modules = course.modules.filter(order__lt=module.order)
    for prev_module in previous_modules:
        if prev_module.lessons.exclude(
            students_lesson_progress__user=request.user,
            students_lesson_progress__is_completed=True
        ).exists():
            messages.error(request, "Сначала пройдите все уроки предыдущего модуля")
            return redirect('students:course_detail', slug=course.slug)

    # =============================
    # 2️⃣ Проверка предыдущих уроков
    # =============================
    if module.lessons.filter(order__lt=lesson.order).exclude(
        students_lesson_progress__user=request.user,
        students_lesson_progress__is_completed=True
    ).exists():
        messages.error(request, "Сначала пройдите предыдущие уроки этого модуля")
        return redirect('students:course_detail', slug=course.slug)

    # =============================
    # 3️⃣ Прогресс
    # =============================
    progress, _ = LessonProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )

    result = None
    feedback = []
    user_code = ""

    # =============================
    # 4️⃣ ТЕКСТ
    # =============================
    if lesson.lesson_type == 'text' and not progress.is_completed:
        progress.is_completed = True
        progress.save()
        messages.success(request, "Урок отмечен как пройденный")

    # =============================
    # 5️⃣ ВИДЕО
    # =============================
    elif lesson.lesson_type == 'video' and request.method == 'POST':
        progress.is_completed = True
        progress.save()
        messages.success(request, "Видео отмечено как пройденное")

    # =============================
    # 6️⃣ ЗАДАЧА
    # =============================
    elif lesson.lesson_type == 'task' and request.method == 'POST':
        user_code = request.POST.get('code', '').strip()

        if not user_code:
            messages.error(request, "Код не может быть пустым")
            result = "fail"
        else:
            all_passed = True

            for testcase in lesson.testcases.all().order_by('order'):
                passed = False
                output = ""

                try:
                    # Подготовка входных переменных как списка (сохранение порядка строк)
                    inputs = []
                    for line in testcase.input_data.splitlines():
                        if "=" in line:
                            var, value = line.split("=", 1)
                            inputs.append((var.strip(), value.strip()))

                    # Запускаем код пользователя в отдельном процессе
                    run_result = run_user_code(user_code, inputs, timeout=5)

                    # Если в stderr что-то пришло — считаем ошибкой выполнения
                    stderr = (run_result.get('error') or '').strip()
                    stdout = (run_result.get('output') or '').strip()

                    if stderr:
                        output = stderr
                        passed = False
                        all_passed = False
                    else:
                        output = stdout
                        expected = testcase.expected_output.strip()
                        try:
                            passed = float(output) == float(expected)
                        except:
                            passed = output == expected
                        if not passed:
                            all_passed = False

                except Exception as e:
                    output = f"{type(e).__name__}: {e}"
                    passed = False
                    all_passed = False

                feedback.append({
                    "input": testcase.input_data,
                    "expected": testcase.expected_output,
                    "output": output,
                    "passed": passed
                })

            if all_passed:
                progress.is_completed = True
                progress.save()
                result = "success"
                messages.success(request, "🎉 Все тесты пройдены!")
            else:
                result = "fail"
                messages.error(request, "Не все тесты пройдены")

    # =============================
    # 7️⃣ Следующий урок
    # =============================
    next_lesson = None
    if progress.is_completed:
        next_lesson = module.lessons.filter(order__gt=lesson.order).first()
        if not next_lesson:
            next_module = course.modules.filter(order__gt=module.order).first()
            if next_module:
                next_lesson = next_module.lessons.order_by('order').first()

    return render(request, 'students/lesson_detail.html', {
        "lesson": lesson,
        "course": course,
        "module": module,
        "progress": progress,
        "result": result,
        "feedback": feedback,
        "next_lesson": next_lesson,
        "user_code": user_code or lesson.code_template,
    })
