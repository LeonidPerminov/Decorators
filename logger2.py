import os
import datetime
import types

# Параметризованный логгер: путь к файлу передается как аргумент.
def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            # Получаем дату и время вызова функции
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Имя функции, которую мы оборачиваем
            function_name = old_function.__name__
            # Формируем строку из всех переданных аргументов
            args_str = ', '.join([str(arg) for arg in args] + [f"{key}={value}" for key, value in kwargs.items()])
            # Вызываем оригинальную функцию и сохраняем результат
            result = old_function(*args, **kwargs)
            # Формируем строку лога
            log_message = f"{now} - Вызвана функция: {function_name}, Аргументы: {args_str}, Результат: {result}\n"
            # Открываем указанный лог-файл в режиме дозаписи и записываем лог-сообщение
            with open(path, 'a') as log_file:
                log_file.write(log_message)
            return result
        return new_function
    return __logger

# Применяем логгер к генераторной функции.
@logger('flat_generator.log')
def flat_generator(list_of_lists):
    for sublist in list_of_lists:
        for item in sublist:
            yield item

def test_2():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]
    # Тестируем последовательное получение элементов через генератор
    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]):
        assert flat_iterator_item == check_item

    # Преобразование генератора в список для проверки всех элементов
    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)

if __name__ == '__main__':
    # Удаляем старый лог-файл, если он существует, чтобы начать чисто
    if os.path.exists('flat_generator.log'):
        os.remove('flat_generator.log')
    test_2()
