from django.apps import AppConfig


class MocktestConfig(AppConfig):
    name = 'mocktest'

    def ready(self):
        import mocktest.signals  # noqa: F401
