from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Question, Choice, Submission


def submit(request):
    if request.method == "POST":
        score = 0
        total = 0
        results = []

        for question in Question.objects.all():
            choice_id = request.POST.get(str(question.id))

            if choice_id:
                choice = get_object_or_404(
                    Choice,
                    id=choice_id,
                    question=question
                )

                total += 1

                if choice.is_correct:
                    score += 1

                results.append({
                    "question": question.question_text,
                    "selected_choice": choice.choice_text,
                    "is_correct": choice.is_correct
                })

                Submission.objects.create(
                    question=question,
                    selected_choice=choice
                )

        request.session["score"] = score
        request.session["total"] = total
        request.session["results"] = results

        return redirect("show_exam_result")

    return redirect("course_list")


def show_exam_result(request):
    score = request.session.get("score", 0)
    total = request.session.get("total", 0)
    results = request.session.get("results", [])

    return render(request, "OnlineCourse/exam_result.html", {
        "score": score,
        "total": total,
        "results": results
    })
