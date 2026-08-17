import frappe
from frappe.model.document import Document


class DSAProblem(Document):

    def after_insert(self):
        self.create_lesson()

    def create_lesson(self):

        difficulty = self.difficulty.strip().capitalize()

        chapter = frappe.db.get_value(
            "Course Chapter",
            {"title": difficulty},
            ["name", "course"],
            as_dict=True
        )

        if not chapter:
            frappe.throw(
                f"No Course Chapter found for difficulty: {difficulty}"
            )

        lesson = frappe.get_doc({
			"doctype": "Course Lesson",
			"title": self.title,
			"chapter": chapter.name,
			"course": chapter.course,
			"custom_dsa_problem": self.name,
		})

        lesson.insert()

        chapter_doc = frappe.get_doc(
            "Course Chapter",
            chapter.name
        )

        chapter_doc.append("lessons", {
            "lesson": lesson.name
        })

        chapter_doc.save()

        frappe.msgprint(
            f"Lesson created successfully: {lesson.name}"
        )