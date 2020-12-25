import pytest
from tests.conftest import Jira


@pytest.mark.usefixtures('app_class')
class APITestCase(Jira):
    pass
