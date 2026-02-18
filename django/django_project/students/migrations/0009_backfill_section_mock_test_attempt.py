from django.db import migrations, models, transaction


def forwards(apps, schema_editor):
    SectionAttempt = apps.get_model("students", "SectionAttempt")
    MockTestAttempt = apps.get_model("students", "MockTestAttempt")
    db_alias = schema_editor.connection.alias

    with transaction.atomic(using=db_alias):
        qs = (
            SectionAttempt.objects.using(db_alias)
            .filter(mock_test_attempt__isnull=True)
            .select_related("mock_test_tab__mock_test")
        )
        for sa in qs:
            mock = sa.mock_test_tab.mock_test if sa.mock_test_tab_id else None
            candidate = None
            if mock:
                candidate = (
                    MockTestAttempt.objects.using(db_alias)
                    .filter(mock_test_id=mock.id)
                    .order_by("-started_at", "-id")
                    .first()
                )
            if candidate:
                sa.mock_test_attempt_id = candidate.id
                sa.save(update_fields=["mock_test_attempt"])
            else:
                # Orphaned section attempt without a matching mock test attempt; delete to maintain integrity
                sa.delete()


def backwards(apps, schema_editor):
    SectionAttempt = apps.get_model("students", "SectionAttempt")
    db_alias = schema_editor.connection.alias
    with transaction.atomic(using=db_alias):
        SectionAttempt.objects.using(db_alias).update(mock_test_attempt=None)


class Migration(migrations.Migration):

    dependencies = [
        ("students", "0008_auto_20260219_0145"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
        migrations.AlterField(
            model_name="sectionattempt",
            name="mock_test_attempt",
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                related_name="section_attempts",
                to="students.mocktestattempt",
                null=False,
                blank=False,
            ),
        ),
    ]
