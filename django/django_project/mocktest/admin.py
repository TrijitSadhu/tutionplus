from django.contrib import admin, messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.apps import apps
from django.db import models, transaction

from bank.admin import admin_site
from mocktest.models import (
	MockDistributionRule,
	MockTest,
	MockTestQuestion,
	MockTestTab,
	Tab,
)
from mocktest.services.mock_generator import MockTestGeneratorService


def _resolve_model(model_name: str):
	if not model_name:
		return None
	try:
		return apps.get_model("bank", model_name)
	except LookupError:
		return None


def _bank_model_choices():
	try:
		return [m._meta.model_name for m in apps.get_app_config("bank").get_models()]
	except LookupError:
		return []


def _logical_field(model, logical: str):
	mapping = {
		"subject": ["subject", "subject_name"],
		"chapter": ["chapter"],
		"sub_chapter": ["sub_chapter"],
		"section": ["section"],
		"difficulty": ["difficulty", "difficult_level"],
		"question": ["question", "question_text", "text"],
	}
	for cand in mapping.get(logical, []):
		if hasattr(model, cand):
			return cand
	return None


def _distinct_values(model_name: str, logical_field: str, filters=None):
	model = _resolve_model(model_name)
	actual_field = _logical_field(model, logical_field) if model else None
	if not model or not actual_field:
		return []
	filters = filters or {}
	qs = model.objects.all()
	if filters:
		clean = {}
		for logical, val in filters.items():
			actual = _logical_field(model, logical)
			if val and actual:
				clean[actual] = val
		if clean:
			qs = qs.filter(**clean)
	return list(qs.order_by(actual_field).values_list(actual_field, flat=True).distinct())


class MockDistributionRuleInline(admin.TabularInline):
	model = MockDistributionRule
	extra = 0
	fields = (
		"mcq_model",
		"subject",
		"chapter",
		"sub_chapter",
		"section",
		"difficulty",
		"question_type",
		"question_count",
		"percentage",
	)


class MockTestTabInline(admin.TabularInline):
	model = MockTestTab
	extra = 0
	fields = ("tab", "selection_mode", "total_questions", "time_limit_minutes", "order")


class MockTestQuestionInline(admin.TabularInline):
	model = MockTestQuestion
	extra = 0
	can_delete = False
	readonly_fields = ("mcq_id", "order", "marks", "negative_marks", "added_manually", "mock_test_tab")
	fields = readonly_fields


@admin.register(Tab, site=admin_site)
class TabAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "exam", "order")
	list_filter = ("exam",)
	search_fields = ("name", "exam")


@admin.register(MockTest, site=admin_site)
class MockTestAdmin(admin.ModelAdmin):
	list_display = ("id", "title", "mock_type", "total_questions", "total_marks", "is_active", "created_at")
	list_filter = ("mock_type", "is_active")
	search_fields = ("title", "exam")
	readonly_fields = ("total_questions", "total_marks")
	inlines = (MockTestTabInline, MockTestQuestionInline)
	actions = ("action_generate_mock", "action_regenerate_mock", "action_validate_distribution", "action_update_config_from_existing")
	change_form_template = "admin/mocktest/mocktest/change_form.html"

	def get_urls(self):
		urls = super().get_urls()
		custom = [
			path(
				"<int:mocktest_id>/modify/",
				self.admin_site.admin_view(self.modify_view),
				name="mocktest_modify",
			),
			path(
				"<int:mocktest_id>/distribute/",
				self.admin_site.admin_view(self.distribute_view),
				name="mocktest_distribute",
			),
			path(
				"ajax/models/",
				self.admin_site.admin_view(self.ajax_models),
				name="mocktest_ajax_models",
			),
			path(
				"ajax/search_mcqs/",
				self.admin_site.admin_view(self.ajax_search_mcqs),
				name="mocktest_ajax_search_mcqs",
			),
			path(
				"ajax/subjects/",
				self.admin_site.admin_view(self.ajax_subjects),
				name="mocktest_ajax_subjects",
			),
			path(
				"ajax/chapters/",
				self.admin_site.admin_view(self.ajax_chapters),
				name="mocktest_ajax_chapters",
			),
			path(
				"ajax/sub_chapters/",
				self.admin_site.admin_view(self.ajax_sub_chapters),
				name="mocktest_ajax_sub_chapters",
			),
			path(
				"ajax/sections/",
				self.admin_site.admin_view(self.ajax_sections),
				name="mocktest_ajax_sections",
			),
			path(
				"ajax/add_mcq/",
				self.admin_site.admin_view(self.ajax_add_mcq),
				name="mocktest_ajax_add_mcq",
			),
			path(
				"ajax/remove_mcq/",
				self.admin_site.admin_view(self.ajax_remove_mcq),
				name="mocktest_ajax_remove_mcq",
			),
			path(
				"ajax/update_mcq/",
				self.admin_site.admin_view(self.ajax_update_mcq),
				name="mocktest_ajax_update_mcq",
			),
			path(
				"ajax/reorder_mcq/",
				self.admin_site.admin_view(self.ajax_reorder_mcq),
				name="mocktest_ajax_reorder_mcq",
			),
			path(
				"ajax/replace_mcq/",
				self.admin_site.admin_view(self.ajax_replace_mcq),
				name="mocktest_ajax_replace_mcq",
			),
			path(
				"ajax/add_rule/",
				self.admin_site.admin_view(self.ajax_add_rule),
				name="mocktest_ajax_add_rule",
			),
			path(
				"ajax/delete_rule/",
				self.admin_site.admin_view(self.ajax_delete_rule),
				name="mocktest_ajax_delete_rule",
			),
			path(
				"ajax/regenerate_mock/",
				self.admin_site.admin_view(self.ajax_regenerate_mock),
				name="mocktest_ajax_regenerate_mock",
			),
			path(
				"ajax/regenerate_tab/",
				self.admin_site.admin_view(self.ajax_regenerate_tab),
				name="mocktest_ajax_regenerate_tab",
			),
		]
		return custom + urls

	def modify_view(self, request, mocktest_id, *args, **kwargs):
		obj = self.get_object(request, mocktest_id)
		tabs = obj.tabs.select_related("tab").prefetch_related("questions").all()

		# Fetch question text and related fields per model for the selected MCQs (respecting stored mcq_model)
		mcq_lookup = {}
		model_to_ids = {}
		fallback_ids = set()
		for tab in tabs:
			for q in tab.questions.all():
				if q.mcq_model:
					model_to_ids.setdefault(q.mcq_model, set()).add(q.mcq_id)
				else:
					fallback_ids.add(q.mcq_id)
		# Query per recorded model first
		for model_name, ids in model_to_ids.items():
			model = _resolve_model(model_name)
			if not model:
				continue
			question_field = _logical_field(model, "question")
			subject_field = _logical_field(model, "subject")
			chapter_field = _logical_field(model, "chapter")
			sub_chapter_field = _logical_field(model, "sub_chapter")
			section_field = _logical_field(model, "section")
			difficulty_field = _logical_field(model, "difficulty") or _logical_field(model, "difficult_level")
			fields = ["id"]
			for f in [question_field, subject_field, chapter_field, sub_chapter_field, section_field, difficulty_field]:
				if f:
					fields.append(f)
			for row in model.objects.filter(id__in=ids).values(*fields):
				mcq_lookup[(model_name, row["id"])] = {
					"model": model._meta.model_name,
					"question": row.get(question_field) if question_field else "",
					"subject": row.get(subject_field) if subject_field else "",
					"chapter": row.get(chapter_field) if chapter_field else "",
					"sub_chapter": row.get(sub_chapter_field) if sub_chapter_field else "",
					"section": row.get(section_field) if section_field else "",
					"difficulty": row.get(difficulty_field) if difficulty_field else "",
				}
		# Fallback: try all models for ids without a stored model
		if fallback_ids:
			for model_name in _bank_model_choices():
				model = _resolve_model(model_name)
				if not model:
					continue
				question_field = _logical_field(model, "question")
				subject_field = _logical_field(model, "subject")
				chapter_field = _logical_field(model, "chapter")
				sub_chapter_field = _logical_field(model, "sub_chapter")
				section_field = _logical_field(model, "section")
				difficulty_field = _logical_field(model, "difficulty") or _logical_field(model, "difficult_level")
				fields = ["id"]
				for f in [question_field, subject_field, chapter_field, sub_chapter_field, section_field, difficulty_field]:
					if f:
						fields.append(f)
				for row in model.objects.filter(id__in=fallback_ids).values(*fields):
					key = (model_name, row["id"])
					if key in mcq_lookup:
						continue
					mcq_lookup[key] = {
						"model": model._meta.model_name,
						"question": row.get(question_field) if question_field else "",
						"subject": row.get(subject_field) if subject_field else "",
						"chapter": row.get(chapter_field) if chapter_field else "",
						"sub_chapter": row.get(sub_chapter_field) if sub_chapter_field else "",
						"section": row.get(section_field) if section_field else "",
						"difficulty": row.get(difficulty_field) if difficulty_field else "",
					}

		for tab in tabs:
			for q in tab.questions.all():
				key = (q.mcq_model, q.mcq_id) if q.mcq_model else None
				info = mcq_lookup.get(key) if key else None
				if not info:
					# fallback lookup by id only if unique
					matches = [v for (m, mid), v in mcq_lookup.items() if mid == q.mcq_id]
					info = matches[0] if len(matches) == 1 else {}
				q.display_model = info.get("model", "") if info else ""
				q.display_question = info.get("question", "") if info else ""
				q.display_subject = info.get("subject", "") if info else ""
				q.display_chapter = info.get("chapter", "") if info else ""
				q.display_sub_chapter = info.get("sub_chapter", "") if info else ""
				q.display_section = info.get("section", "") if info else ""
				q.display_difficulty = info.get("difficulty", "") if info else ""
		context = dict(
			self.admin_site.each_context(request),
			mocktest=obj,
			tabs=tabs,
			opts=self.model._meta,
		)
		return TemplateResponse(request, "mocktest/mocktest_summary.html", context)

	def distribute_view(self, request, mocktest_id, *args, **kwargs):
		obj = self.get_object(request, mocktest_id)
		tabs = obj.tabs.select_related("tab").prefetch_related("distribution_rules", "questions").all()
		for t in tabs:
			t.current_questions = len(t.questions.all()) if hasattr(t, "questions") else t.questions.count()
		context = dict(
			self.admin_site.each_context(request),
			mocktest=obj,
			tabs=tabs,
			opts=self.model._meta,
		)
		return TemplateResponse(request, "mocktest/mocktest_distribute.html", context)

	# ---------- AJAX helpers ----------
	def _json_error(self, message: str, status: int = 400):
		return JsonResponse({"error": message}, status=status)

	def _validate_marks(self, marks, negative):
		try:
			m = float(marks)
			n = float(negative)
		except (TypeError, ValueError):
			return None, None, "marks and negative_marks must be numbers"
		if m <= 0:
			return None, None, "marks must be > 0"
		if n < 0:
			return None, None, "negative_marks must be >= 0"
		if n > m:
			return None, None, "negative_marks cannot exceed marks"
		return m, n, None

	@transaction.atomic
	def ajax_add_mcq(self, request):
		if request.method != "POST":
			return self._json_error("POST required")
		tab_id = request.POST.get("tab_id")
		mcq_id = request.POST.get("mcq_id")
		mcq_model = request.POST.get("model")
		marks = request.POST.get("marks", 1)
		negative = request.POST.get("negative_marks", 0)
		added_manually = request.POST.get("added_manually", "true").lower() == "true"
		if not (tab_id and mcq_id):
			return self._json_error("tab_id and mcq_id required")
		try:
			tab = MockTestTab.objects.select_for_update().select_related("mock_test").get(id=tab_id)
		except MockTestTab.DoesNotExist:
			return self._json_error("Tab not found", 404)
		m, n, err = self._validate_marks(marks, negative)
		if err:
			return self._json_error(err)
		if MockTestQuestion.objects.filter(mock_test=tab.mock_test, mcq_id=mcq_id).exists():
			return self._json_error("MCQ already in mock")
		current_in_tab = MockTestQuestion.objects.filter(mock_test_tab=tab).count()
		if tab.total_questions and current_in_tab >= tab.total_questions:
			return self._json_error(
				f"Tab capacity ({tab.total_questions}) reached; cannot add more questions"
			)
		next_order = (
			MockTestQuestion.objects.filter(mock_test_tab=tab).aggregate(max_o=models.Max("order"))["max_o"] or 0
		) + 1
		q = MockTestQuestion.objects.create(
			mock_test=tab.mock_test,
			mock_test_tab=tab,
			mcq_model=mcq_model,
			mcq_id=int(mcq_id),
			order=next_order,
			marks=m,
			negative_marks=n,
			added_manually=added_manually,
		)
		service = MockTestGeneratorService()
		service._recalc_mock_totals(tab.mock_test)
		return JsonResponse({"id": q.id, "order": q.order, "mcq_id": q.mcq_id, "mcq_model": q.mcq_model, "marks": q.marks, "negative_marks": q.negative_marks})

	@transaction.atomic
	def ajax_remove_mcq(self, request):
		if request.method != "POST":
			return self._json_error("POST required")
		qid = request.POST.get("question_id")
		if not qid:
			return self._json_error("question_id required")
		try:
			q = MockTestQuestion.objects.select_related("mock_test", "mock_test_tab").get(id=qid)
		except MockTestQuestion.DoesNotExist:
			return self._json_error("Question not found", 404)
		tab = q.mock_test_tab
		mock = q.mock_test
		removed_mcq_id = q.mcq_id
		q.delete()
		# Repack ordering
		for idx, obj in enumerate(MockTestQuestion.objects.filter(mock_test_tab=tab).order_by("order", "id"), start=1):
			if obj.order != idx:
				obj.order = idx
				obj.save(update_fields=["order"])
		# Remove deleted MCQ from rule tracking so the distribute page stays in sync
		for rule in tab.distribution_rules.all():
			if not rule.selected_mcq_ids:
				continue
			if removed_mcq_id in rule.selected_mcq_ids:
				updated_ids = [mid for mid in rule.selected_mcq_ids if mid != removed_mcq_id]
				rule.selected_mcq_ids = updated_ids
				rule.mcq_list = ",".join(str(mid) for mid in updated_ids)
				rule.question_count = len(updated_ids) if updated_ids else 0
				rule.save(update_fields=["selected_mcq_ids", "mcq_list", "question_count"])
		service = MockTestGeneratorService()
		service._recalc_mock_totals(mock)
		return JsonResponse({"ok": True})

	@transaction.atomic
	def ajax_update_mcq(self, request):
		if request.method != "POST":
			return self._json_error("POST required")
		qid = request.POST.get("question_id")
		marks = request.POST.get("marks")
		negative = request.POST.get("negative_marks")
		if not qid:
			return self._json_error("question_id required")
		try:
			q = MockTestQuestion.objects.select_related("mock_test", "mock_test_tab").get(id=qid)
		except MockTestQuestion.DoesNotExist:
			return self._json_error("Question not found", 404)
		m, n, err = self._validate_marks(marks, negative)
		if err:
			return self._json_error(err)
		q.marks = m
		q.negative_marks = n
		q.save(update_fields=["marks", "negative_marks"])
		service = MockTestGeneratorService()
		service._recalc_mock_totals(q.mock_test)
		return JsonResponse({"ok": True})

	@transaction.atomic
	def ajax_reorder_mcq(self, request):
		if request.method != "POST":
			return self._json_error("POST required")
		ordered_ids = request.POST.getlist("ordered_ids[]") or request.POST.getlist("ordered_ids")
		if not ordered_ids:
			return self._json_error("ordered_ids required")
		# Ensure all belong to same tab
		qs = list(MockTestQuestion.objects.filter(id__in=ordered_ids).select_related("mock_test_tab", "mock_test"))
		if not qs:
			return self._json_error("No questions found", 404)
		tab = qs[0].mock_test_tab
		for idx, qid in enumerate(ordered_ids, start=1):
			MockTestQuestion.objects.filter(id=qid, mock_test_tab=tab).update(order=idx)
		return JsonResponse({"ok": True})

	@transaction.atomic
	def ajax_replace_mcq(self, request):
		if request.method != "POST":
			return self._json_error("POST required")
		qid = request.POST.get("question_id")
		new_mcq = request.POST.get("mcq_id")
		mcq_model = request.POST.get("model")
		marks = request.POST.get("marks")
		negative = request.POST.get("negative_marks")
		if not (qid and new_mcq):
			return self._json_error("question_id and mcq_id required")
		try:
			q = MockTestQuestion.objects.select_related("mock_test", "mock_test_tab").get(id=qid)
		except MockTestQuestion.DoesNotExist:
			return self._json_error("Question not found", 404)
		if MockTestQuestion.objects.filter(mock_test=q.mock_test, mcq_id=new_mcq).exclude(id=qid).exists():
			return self._json_error("MCQ already present in mock")
		m, n, err = self._validate_marks(marks or q.marks, negative or q.negative_marks)
		if err:
			return self._json_error(err)
		q.mcq_id = int(new_mcq)
		q.mcq_model = mcq_model or q.mcq_model
		q.marks = m
		q.negative_marks = n
		q.save(update_fields=["mcq_id", "mcq_model", "marks", "negative_marks"])
		service = MockTestGeneratorService()
		service._recalc_mock_totals(q.mock_test)
		return JsonResponse({"ok": True, "mcq_id": q.mcq_id, "mcq_model": q.mcq_model})

	@transaction.atomic
	def ajax_add_rule(self, request):
		if request.method != "POST":
			return self._json_error("POST required")
		tab_id = request.POST.get("tab_id")
		model_name = request.POST.get("model")
		subject = request.POST.get("subject") or ""
		chapter = request.POST.get("chapter") or None
		sub_chapter = request.POST.get("sub_chapter") or None
		section = request.POST.get("section") or None
		difficulty = request.POST.get("difficulty") or None
		question_type = request.POST.get("question_type") or None
		question_count = request.POST.get("question_count") or None
		auto = str(request.POST.get("auto", "false")).lower() == "true"
		if not tab_id:
			return self._json_error("tab_id required")
		if not model_name:
			return self._json_error("model required")
		try:
			tab = MockTestTab.objects.select_for_update().select_related("mock_test").get(id=tab_id)
		except MockTestTab.DoesNotExist:
			return self._json_error("Tab not found", 404)

		clean_count = None
		if question_count:
			try:
				clean_count = int(question_count)
			except (TypeError, ValueError):
				return self._json_error("question_count must be an integer")
			if clean_count <= 0:
				return self._json_error("question_count must be > 0")

		# Prepare rule for filtering without saving yet
		temp_rule = MockDistributionRule(
			mock_test_tab=tab,
			mcq_model=model_name,
			subject=subject,
			chapter=chapter,
			sub_chapter=sub_chapter,
			section=section,
			difficulty=difficulty,
			question_type=question_type,
			question_count=clean_count,
		)

		target = clean_count or 0
		if not target and tab.total_questions:
			target = tab.total_questions

		inserted = []
		if auto:
			service = MockTestGeneratorService()
			qs, model = service._filtered_queryset(temp_rule)
			existing_pairs = set(
				MockTestQuestion.objects.filter(mock_test=tab.mock_test).values_list("mcq_model", "mcq_id")
			)
			model_key = (model._meta.model_name if model else model_name) or ""
			existing_ids = {mid for m, mid in existing_pairs if (m or "") == model_key}
			current_in_tab = MockTestQuestion.objects.filter(mock_test_tab=tab).count()
			if tab.total_questions:
				remaining_capacity = tab.total_questions - current_in_tab
				if remaining_capacity < target:
					return self._json_error(
						f"Tab capacity ({tab.total_questions}) allows only {remaining_capacity} more questions"
					)
			available_qs = qs.exclude(id__in=existing_ids)
			available_count = available_qs.count()
			if available_count < target:
				return self._json_error(
					f"Only found {available_count} available MCQs for this rule (requested {target})"
				)
			picked = list(available_qs.order_by("?").values_list("id", flat=True)[:target])
			if len(picked) != target:
				return self._json_error(
					f"Only found {len(picked)} available MCQs for this rule (requested {target})"
				)
			order_cursor = MockTestQuestion.objects.filter(mock_test_tab=tab).aggregate(max_order=models.Max("order"))[
				"max_order"
			] or 0
			for mcq_id in picked:
				if (model_key, mcq_id) in existing_pairs:
					continue
				order_cursor += 1
				MockTestQuestion.objects.create(
					mock_test=tab.mock_test,
					mock_test_tab=tab,
					mcq_model=model_key or None,
					mcq_id=mcq_id,
					order=order_cursor,
					marks=1.0,
					negative_marks=0.0,
					added_manually=False,
				)
				inserted.append(mcq_id)
		service._recalc_mock_totals(tab.mock_test)

		# Persist rule only after successful checks/inserts
		rule = MockDistributionRule.objects.create(
			mock_test_tab=tab,
			mcq_model=model_name,
			subject=subject,
			chapter=chapter,
			sub_chapter=sub_chapter,
			section=section,
			difficulty=difficulty,
			question_type=question_type,
			question_count=clean_count,
		)
		rule.selected_mcq_ids = inserted
		rule.mcq_list = ",".join(str(mid) for mid in inserted)
		rule.save(update_fields=["selected_mcq_ids", "mcq_list"])

		return JsonResponse({
			"ok": True,
			"rule_id": rule.id,
			"mcq_ids": inserted,
			"requested": target,
			"added": len(inserted),
			"partial": False,
		})

	@transaction.atomic
	def ajax_delete_rule(self, request):
		if request.method != "POST":
			return self._json_error("POST required")
		rule_id = request.POST.get("rule_id")
		if not rule_id:
			return self._json_error("rule_id required")
		try:
			rule = MockDistributionRule.objects.select_related("mock_test_tab", "mock_test_tab__mock_test").get(id=rule_id)
		except MockDistributionRule.DoesNotExist:
			return self._json_error("Rule not found", 404)
		tab = rule.mock_test_tab
		mock = tab.mock_test
		model_key = rule.mcq_model or ""
		ids_to_remove = rule.selected_mcq_ids or []
		if ids_to_remove:
			MockTestQuestion.objects.filter(
				mock_test_tab=tab,
				mcq_id__in=ids_to_remove,
				mcq_model=model_key or None,
				added_manually=False,
			).delete()
		rule.delete()
		service = MockTestGeneratorService()
		service._recalc_mock_totals(mock)
		return JsonResponse({"ok": True})

	@transaction.atomic
	def ajax_regenerate_mock(self, request):
		if request.method != "POST":
			return self._json_error("POST required")
		mock_id = request.POST.get("mock_id")
		if not mock_id:
			return self._json_error("mock_id required")
		try:
			mock = MockTest.objects.get(id=mock_id)
		except MockTest.DoesNotExist:
			return self._json_error("Mock not found", 404)
		service = MockTestGeneratorService()
		service.generate_mock(mock.id)
		mock.refresh_from_db()
		return JsonResponse({"ok": True, "total_questions": mock.total_questions, "total_marks": mock.total_marks})

	@transaction.atomic
	def ajax_regenerate_tab(self, request):
		if request.method != "POST":
			return self._json_error("POST required")
		tab_id = request.POST.get("tab_id")
		if not tab_id:
			return self._json_error("tab_id required")
		try:
			tab = MockTestTab.objects.select_related("mock_test").get(id=tab_id)
		except MockTestTab.DoesNotExist:
			return self._json_error("Tab not found", 404)
		service = MockTestGeneratorService()
		service.regenerate_tab(tab.id)
		service._recalc_mock_totals(tab.mock_test)
		tab.mock_test.refresh_from_db()
		current_questions = MockTestQuestion.objects.filter(mock_test_tab=tab).count()
		return JsonResponse({
			"ok": True,
			"tab_id": tab.id,
			"current_questions": current_questions,
			"tab_total": tab.total_questions,
			"mock_total_questions": tab.mock_test.total_questions,
			"mock_total_marks": tab.mock_test.total_marks,
		})

	def _mcq_field_exists(self, model, field: str) -> bool:
		return bool(model and field in {f.name for f in model._meta.get_fields()})  # type: ignore

	def ajax_search_mcqs(self, request):
		model_name = request.GET.get("model")
		model = _resolve_model(model_name)
		if not model:
			return self._json_error("MCQ model not found", 500)
		# Map logical fields to actual field names to support variations
		field_map = {
			"subject": "subject" if self._mcq_field_exists(model, "subject") else "subject_name" if self._mcq_field_exists(model, "subject_name") else None,
			"chapter": "chapter" if self._mcq_field_exists(model, "chapter") else None,
			"sub_chapter": "sub_chapter" if self._mcq_field_exists(model, "sub_chapter") else None,
			"section": "section" if self._mcq_field_exists(model, "section") else None,
			"question_type": "question_type" if self._mcq_field_exists(model, "question_type") else None,
			"difficulty": "difficulty" if self._mcq_field_exists(model, "difficulty") else "difficult_level" if self._mcq_field_exists(model, "difficult_level") else None,
			"question": "question" if self._mcq_field_exists(model, "question") else "question_text" if self._mcq_field_exists(model, "question_text") else "text" if self._mcq_field_exists(model, "text") else None,
		}
		qs = model.objects.all()
		for logical, actual in field_map.items():
			val = request.GET.get(logical)
			if val and actual:
				qs = qs.filter(**{actual: val})
		results = []
		for obj in qs.order_by("id")[:200]:
			item = {"id": obj.id, "source": model._meta.model_name}
			for logical, actual in field_map.items():
				if actual:
					item[logical] = getattr(obj, actual, None)
			results.append(item)
		return JsonResponse({"results": results})

	def ajax_models(self, request):
		return JsonResponse({"results": _bank_model_choices()})

	def ajax_subjects(self, request):
		model_name = request.GET.get("model")
		chapter = request.GET.get("chapter")
		if not model_name:
			return JsonResponse({"results": _bank_model_choices()})
		filters = {}
		if chapter:
			filters["chapter"] = chapter
		return JsonResponse({"results": _distinct_values(model_name, "subject", filters)})

	def ajax_chapters(self, request):
		model_name = request.GET.get("model")
		return JsonResponse({"results": _distinct_values(model_name, "chapter", {})})

	def ajax_sub_chapters(self, request):
		model_name = request.GET.get("model")
		subject = request.GET.get("subject")
		chapter = request.GET.get("chapter")
		filters = {}
		if chapter:
			filters["chapter"] = chapter
		if subject:
			filters["subject"] = subject
		return JsonResponse({"results": _distinct_values(model_name, "sub_chapter", filters)})

	def ajax_sections(self, request):
		model_name = request.GET.get("model")
		subject = request.GET.get("subject")
		chapter = request.GET.get("chapter")
		sub_chapter = request.GET.get("sub_chapter")
		filters = {}
		if chapter:
			filters["chapter"] = chapter
		if subject:
			filters["subject"] = subject
		if sub_chapter:
			filters["sub_chapter"] = sub_chapter
		return JsonResponse({"results": _distinct_values(model_name, "section", filters)})

	def action_generate_mock(self, request, queryset):
		service = MockTestGeneratorService()
		for mock in queryset:
			try:
				service.generate_mock(mock.id)
				self.message_user(request, f"Generated mock {mock.id}")
			except Exception as exc:  # pragma: no cover - admin feedback only
				self.message_user(request, f"Failed to generate mock {mock.id}: {exc}", level=messages.ERROR)

	action_generate_mock.short_description = "Generate Mock"

	def action_regenerate_mock(self, request, queryset):
		service = MockTestGeneratorService()
		for mock in queryset:
			try:
				for tab in mock.tabs.all():
					service.regenerate_tab(tab.id)
				self.message_user(request, f"Regenerated mock {mock.id}")
			except Exception as exc:  # pragma: no cover - admin feedback only
				self.message_user(request, f"Failed to regenerate mock {mock.id}: {exc}", level=messages.ERROR)

	action_regenerate_mock.short_description = "Regenerate Mock"

	def action_validate_distribution(self, request, queryset):
		service = MockTestGeneratorService()
		for mock in queryset:
			issues = service.validate_distribution(mock.id)
			if issues:
				for issue in issues:
					self.message_user(request, issue, level=messages.WARNING)
			else:
				self.message_user(request, f"Mock {mock.id} distribution valid")

	action_validate_distribution.short_description = "Validate Distribution"

	def action_update_config_from_existing(self, request, queryset):
		service = MockTestGeneratorService()
		for mock in queryset:
			service.update_config_from_existing(mock.id)
			self.message_user(request, f"Updated config_json for mock {mock.id} from existing questions")

	action_update_config_from_existing.short_description = "Update JSON config from existing questions"


@admin.register(MockTestTab, site=admin_site)
class MockTestTabAdmin(admin.ModelAdmin):
	list_display = ("id", "mock_test", "tab", "selection_mode", "total_questions", "order")
	list_filter = ("selection_mode",)
	search_fields = ("mock_test__title", "tab__name")


@admin.register(MockDistributionRule, site=admin_site)
class MockDistributionRuleAdmin(admin.ModelAdmin):
	list_display = (
		"id",
		"mock_test_tab",
		"mcq_model",
		"subject",
		"chapter",
		"sub_chapter",
		"section",
		"question_count",
		"percentage",
	)
	list_filter = ("mcq_model", "subject")
	search_fields = ("subject", "chapter", "sub_chapter", "section")


@admin.register(MockTestQuestion, site=admin_site)
class MockTestQuestionAdmin(admin.ModelAdmin):
	list_display = ("id", "mock_test", "mock_test_tab", "mcq_id", "order", "marks", "negative_marks", "added_manually")
	list_filter = ("added_manually",)
	search_fields = ("mcq_id",)
	change_form_template = "admin/mocktest/mocktestquestion/change_form.html"


# ===============================
# EXAM MANAGEMENT SYSTEM START
# ===============================

from mocktest.forms import ExamForm
from mocktest.models import Exam, ExamSummary, Segment
from mocktest.signals import recalc_exam_summary


@admin.register(Segment, site=admin_site)
class SegmentAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "created_at")
	search_fields = ("name",)


@admin.register(Exam, site=admin_site)
class ExamAdmin(admin.ModelAdmin):
	form = ExamForm
	change_form_template = "admin/mocktest/exam/change_form.html"
	filter_horizontal = ("mock_tests",)
	list_display = ("name", "year", "state", "display_total_mock_tests")
	search_fields = ("name",)
	list_filter = ("year", "state")

	def get_urls(self):
		urls = super().get_urls()
		custom = [
			path(
				"<int:exam_id>/select/mocktests/",
				self.admin_site.admin_view(self.select_mocktests_view),
				name="mocktest_exam_select",
			),
		]
		return custom + urls

	def get_form(self, request, obj=None, **kwargs):
		base_form = super().get_form(request, obj, **kwargs)

		class RequestBoundExamForm(base_form):
			def __init__(self, *args, **form_kwargs):
				form_kwargs["request"] = request
				super().__init__(*args, **form_kwargs)

		return RequestBoundExamForm

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		return qs.select_related("segment").prefetch_related("summary")

	def display_total_mock_tests(self, obj):
		summary = getattr(obj, "summary", None)
		return summary.total_mock_tests if summary else 0

	display_total_mock_tests.short_description = "Mock Tests"

	def select_mocktests_view(self, request, exam_id, *args, **kwargs):
		exam = self.get_object(request, exam_id)
		if not exam:
			return self._get_obj_does_not_exist_redirect(request, self.model._meta, None)
		if not self.has_change_permission(request, exam):
			return self._get_obj_does_not_exist_redirect(request, self.model._meta, None)

		selected_qs = exam.mock_tests.all()
		selected_ids = list(selected_qs.values_list("id", flat=True))

		if request.method == "POST":
			form = ExamForm(request.POST, instance=exam, request=request)
			if form.is_valid():
				form.save()
				self.message_user(request, "Exam updated with selected mock tests")
				return redirect(reverse("admin:mocktest_exam_change", args=[exam_id]))
		else:
			form = ExamForm(instance=exam, request=request)

		context = dict(
			self.admin_site.each_context(request),
			form=form,
			exam=exam,
			selected_qs=selected_qs,
			selected_ids=selected_ids,
			opts=self.model._meta,
			title=f"Select Mock Tests for {exam}",
		)
		return TemplateResponse(request, "admin/mocktest/exam/select_mocktests.html", context)


@admin.register(ExamSummary, site=admin_site)
class ExamSummaryAdmin(admin.ModelAdmin):
	list_display = (
		"exam",
		"total_mock_tests",
		"total_questions",
		"total_marks",
		"total_tabs",
		"total_distribution_rules",
		"total_question_objects",
		"updated_at",
	)
	search_fields = ("exam__name",)
	list_filter = ("exam__state",)

	def save_model(self, request, obj, form, change):
		super().save_model(request, obj, form, change)
		if obj.exam_id:
			recalc_exam_summary(obj.exam)


@admin.register(Exam.mock_tests.through, site=admin_site)
class ExamMockTestThroughAdmin(admin.ModelAdmin):
	list_display = ("id", "exam", "mocktest")
	list_filter = ("exam", "mocktest")
	search_fields = ("exam__name", "mocktest__title")
