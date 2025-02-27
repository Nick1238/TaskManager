▎Описание задания

Вам необходимо разработать консольное приложение — трекер времени. Это приложение должно позволять пользователю управлять несколькими одновременно выполняемыми задачами и отслеживать время, затраченное на каждую из них, в режиме реального времени. 

▎Основные функции приложения

1. Добавление задачи: Пользователь должен иметь возможность добавлять новую задачу с уникальным названием.

2. Отслеживание задач: Приложение должно отображать список текущих задач с информацией о времени, затраченном на каждую из них.

3. Изменение названия задачи: Пользователь должен иметь возможность изменять название уже существующей задачи.

4. Удаление задачи: Пользователь должен иметь возможность удалять задачу из списка активных.

5. Остановка и завершение задачи: Пользователь должен иметь возможность останавливать и завершать задачи, чтобы фиксировать общее время выполнения.

6. Хранение данных: Все задачи должны быть записаны в SQL базу данных с использованием ORM (выбор драйвера на ваше усмотрение: MySQL, PostgreSQL или SQLite).

▎Рекомендации к реализации

• Приложение должно быть написано на Python.

• Используйте мультипарадигмальный подход (поддержка объектно-ориентированного и функционального программирования).

• Код должен быть чистым и идиоматически правильным, с соблюдением PEP 8.

• Необходимо использовать тестирование (например, с помощью библиотеки unittest или pytest).

• Обеспечьте обработку ошибок и валидацию ввода пользователя.

• Для отслеживания множества тасков единовременно можете использовать любую библиотеку на ваше усмотрение (например threading)

▎Критерии оценивания

1. Чистый и идиоматически правильный код: Код должен быть читаемым, структурированным и соответствовать стандартам Python.

2. Использование мультипарадигмального подхода: Применение как объектно-ориентированных, так и функциональных концепций в коде.

3. Архитектура приложения: Логика приложения должна быть четко разделена на слои (например, модель, представление и контроллер).

4. Тестирование: Наличие тестов для основных функций приложения.

5. Документация: Код должен содержать комментарии и документацию, объясняющую его работу.

▎Дополнительные рекомендации

• Рассмотрите возможность использования библиотеки для работы с временем (например, datetime или pendulum).

• Подумайте о том, как можно улучшить пользовательский опыт (например, добавление команды для вывода справки по доступным командам).

• Убедитесь, что ваше приложение работает корректно при одновременном выполнении нескольких задач.

▎Сдача задания

Пожалуйста, отправьте ваш код в репозитории на GitHub или другом аналогичном сервисе. Убедитесь, что ваш проект содержит файл README.md, в котором описаны шаги по установке и запуску приложения, а также инструкции по использованию.

Удачи!