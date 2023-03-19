from django import template


register = template.Library()


# Регистрируем наш фильтр под именем censor, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(text: str):
    """
    text: строка, к которой нужно применить фильтр
    """

    censor_list = [
        'Зенит',
        'new',
        'New', 
        #'news', 
        'уничтожит', 
        'уничтожение',
        'сражением',
    ]

    if isinstance(text, str):
        text_list = text.split(' ')

        for i, word in enumerate(text_list):
            if word in censor_list:
                text_list[i] = ''.join([word[0], '*'*(len(word)-1)])
    else:
        raise KeyError('Введена не строка')
    
    return ' '.join(text_list)

