import pytest
from datetime import date
from datetime import timedelta

from document_units.models import DocumentFormat, DocumentUnit
from document_units.exceptions import InvalidFormatData

from projects.models import Project

pytestmark = pytest.mark.django_db

# FIXTURES ----


@pytest.fixture
def project() -> Project:
    return Project.objects.create(
        name="Test Project 1",
        end_date=date.today() + timedelta(days=2)
    )


@pytest.fixture
def project_format(project) -> DocumentFormat:
    dict_format = dict(
        field_1='text',
        field_2='text'
    )

    return DocumentFormat.objects.create(
        name="Format_One",
        project=project,
        data=dict_format
    )

# TESTS -----


def test_create_document_format(project):
    dict_format = dict(
        field_1='text',
        field_2='text'
    )

    format_ = DocumentFormat.objects.create(
        name="Format_One",
        project=project,
        data=dict_format
    )

    assert DocumentFormat.objects.count() == 1
    assert format_.project.name == 'Test Project 1'
    assert len(format_.data.keys()) == 2
    assert format_.data.get('field_1') == 'text'


def test_create_document_format_assign_list_data(project):
    list_data = ['smth', 'smth2']

    with pytest.raises(InvalidFormatData):
        DocumentFormat.objects.create_format(
            name='Format 1',
            project=project,
            data=list_data
        )


def test_create_document_unit(project, project_format):
    DocumentUnit.objects.create(
        name="Document 1",
        project=project,
        document_format=project_format
    )

    assert DocumentUnit.objects.count() == 1
