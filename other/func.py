def check_text(text:str) -> bool:
    '''Функция которая определяет есть ли ключевое слово в тексте'''
    text = text.lower()#уменьшаем текст

    with open('stop_word.txt', 'r', encoding='utf-8') as stop_words_file:#открываем файл с стоп словами
        stop_words_list = stop_words_file.read().lower().split(',')#составляем список стоп слов
        word_list_stop = []
        for word in stop_words_list:
            if len(word) <3:
                continue
            word_list_stop.append(word.strip())#пополняем список стоп слов

    for stop_word in word_list_stop:
        if stop_word in text:
            return False #Если есть стоп слово в тексте то сразу возвращаем False

    with open('key_word.txt', 'r', encoding='utf-8') as key_words_file:#открываем файл с ключевыми словами
        key_words_list = key_words_file.read().lower().split(',')#составляем список ключевых слов
        word_list = []
        for word in key_words_list:
            if len(word) < 3:
                continue
            word_list.append(word.strip()) #пополняем список ключевых слов
    for key_word in word_list:
        if key_word in text:#Если ключевое слово есть в тексте
            return True
    return False


