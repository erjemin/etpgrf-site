# Заметки по деплою проекту

 В финальном комите перед новой версией (*ТОЛЬ ПОСЛЕ ТЕСТИРОВАНИЯ:) не забываем менять:
    - `CHANGELOG.md` делать описание изменений.
    - `typograph/templates/typograph/base.html` в шаблоне циферки в подвале


 Затем, когда код готов к релизу, нужно обновить версию в `pyproject.toml`:
 ```shell
 poetry version patch
 ```

 Финальный коммит, таким образом, должен включать в себя:
    - Обновление `CHANGELOG.md` с описанием изменений.
    - Обновление версии в `pyproject.toml` (через `poetry version patch`).
    - Обновление шаблона `base.html` (циферки в подвале).
    — Обновление в `etpgrf_site/__init__.py`.
    - И, конечно же, все изменения, которые были сделаны в коде.

После комита и пуша:
```shell
git add .
git commit -am "Обновление версии для релиза vX.Y.Z"
git push origin main
```

Для запуска деплоя CI/CD, через Gitea Actions, создаем `git tag` и пушим его в репозиторий:
```shell
git tag vX.Y.Z && git push origin vX.Y.Z
```


