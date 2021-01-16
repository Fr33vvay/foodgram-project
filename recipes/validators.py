from django.core.exceptions import ValidationError


def validate_file(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 2.0
    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError(f'Максимальный размер файла - 2 Мб')