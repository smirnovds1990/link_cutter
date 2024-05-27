Проект созданный для преобразования длинных ссылок в более удобочитаемые варианты. Пользователь вводит длинную ссылку и свой вариант короткой, если свой вариант короткой ссылки не был предоставлен, то приложение создаёт вариант короткой ссылки для пользователя.


Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Запустить приложение

```
flask run
```

Перейти по http://127.0.0.1:5000


###### Автор: [https://github.com/smirnovds1990](https://github.com/smirnovds1990)
