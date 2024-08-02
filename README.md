#  Агрегатор статей (REST/GraphQL)
Простой **CRUD**-сервис для работы со статьями пользователей, предоставляющий взаимодействие через **REST API** и **GraphQL**, и реализованный вокруг фреймворка **FastAPI**.
Приложение придерживается слоистой архитектуры, общение между слоями происходит с помощью **DTO**, а зависимости внедряются с помощью библиотеки **dependency-injector**.

## Фичи
- Сервис предоставляет возможность создавать, получать, редактировать и удалять статьи с помощью запросов как на привычные **REST**-эндпоинты, так и с помощью запросов на языке **GraphQL**, получая только необходимые поля. Такое поведение достигается за счет использования отдельных слоев работы приложения: entrypoints, service, repositories, uow. Пользователь имеет возможность переключить тип взаимодействия с помощью переменной окружения `IS_REST`. 
- В сервисе реализована аутентификация с помощью **JWT access** и **refresh**-токенов, которые шифруются алгоритмом **HS256** и **БД Redis**, хранящей **refresh**-токены.
- Пользователи имеют возможность получить самые популярные статьи на сервисе в количестве 10 штук, которые хранятся в **БД Redis** для быстрого доступа. Каждый день популярные статьи обновляются и перезаписываются на основе количества их просмотров. Это достигается с помощью настроенного шедулера, который раз в сутки ходит в **Postgres**, забирает актуальные популярные статьи и пишет их в **Redis**.

##  Разворачивание приложения
- Приложение разворачивается через `docker-compose`.
- Пример файла с переменными окружения `/src/env.example`. Для корректной работы необходимо создать файл `.env` и вписать туда необходимые переменные окружения.
- Далее из директории `/ci` прописать `docker-compose up -d`. Будут собраны контейнеры **Redis**, **Postgres** и сам бэкенд. Далее с помощью bash-скрипта будут накатаны миграции **alembic** и запущен сервис.

## Работы с приложением

- Режим работы **REST**: эндпоинты поделены на категории аутентификации `/auth` ,
работы с пользователями `/users`, работы со статьями `/articles`. Документация доступна по адресу `localhost:7777/docs`
- Режим работы **GraphQL**: для создания запроса с целью аутентификации следует обратиться на адрес `localhost:7777/auth-graphql`, для работы с пользователями следует обратиться на адрес `localhost:7777/users-graphql`, для работы со статьями следует обратиться на адрес `localhost:7777/articles-graphql`. При переходе на соответствующий адрес появляется интерактивный редактор запросов **GraphQL**, предоставляемый библиотекой **strawberry**.