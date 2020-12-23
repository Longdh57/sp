import pytest
from app.tests.conftest import Jira


@pytest.mark.usefixtures('app_class')
class APITestCase(Jira):
    pass
