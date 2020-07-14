from django.utils.html import format_html_join, format_html

def help_text():
    help_texts = ['Ваш пароль не может быть слишком похож на другую вашу личную информацию.',
                  'Ваш пароль должен содержать минимум 8 символов.',
                  'Ваш пароль не может быть часто использованным паролем.',
                  'Ваш пароль не может быть полностью цифровым.']
    help_items = format_html_join('', '<li>{}</li>', ((help_text,) for help_text in help_texts))
    return format_html('<ul>{}</ul>', help_items) if help_items else ''
