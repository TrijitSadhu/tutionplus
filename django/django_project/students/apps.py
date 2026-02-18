from django.apps import AppConfig


class StudentsConfig(AppConfig):
    name = "students"

    def ready(self):  # pragma: no cover - import side effect
        import students.signals  # noqa: F401
