# CI/CD с Gitea Runner

Gitea Runner — это инструмент для выполнения CI/CD задач, интегрированный с Gitea. Он позволяет автоматизировать
процессы сборки, тестирования и развертывания приложений.

В нашем репозии входим в "Настройки" -> "Действия" -> "Ранеры" и создаем новый Runner. Для это получим регистрационный
токен.

## Настройка Gitea Runner на macOS

```shell
docker run -d --restart always \                                                                                                                                                                                                             [±main ●]
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e GITEA_INSTANCE_URL=https://git.cube2.ru \
  -e GITEA_RUNNER_REGISTRATION_TOKEN=здест_полученный_токен \
  -e GITEA_RUNNER_REGISTRATION_TOKEN=здесь_вставляем_полученный_токен \
  -e GITEA_RUNNER_NAME=mac-mini-runner \
  --name gitea-runner \
  gitea/act_runner:latest
```

 Увидим:
 ```txt
 Unable to find image 'gitea/act_runner:latest' locally
latest: Pulling from gitea/act_runner
6e174226ea69: Pull complete 
adcf2c0b73c2: Pull complete 
e0c151a1a72f: Pull complete 
3333c50851c8: Pull complete 
Digest: sha256:0000000000000000000000000000000000000000000000000000000000000000
Status: Downloaded newer image for gitea/act_runner:latest
f000000000000000000000000000000000000000000000000000000000000000
```

## Обновление в продакшен

Наш `.gitea/workflows/docker-publish.yaml` настроен на публикацию Docker образа при создании тега, который начинается
с `v`. Образ собирается на компьютпере разработчика (см. главу Настройка Gitea Runner на macOS) и пакет загружается
в Gitea.

На хостинге работает Docker Stack с нашим проектом. Кроме `etpgrf-site-etpgrf-backend` и `etpgrf-site-etpgrf-nginx`
в нем работает `etpgrf-site-watchtower`, который следит за обновлениями образов на Gitea и если находит обновление, то
получает новый образ и перезапускает контейнер с новым образом.

Т.о. если мы хотим обновить продакшен, нам нужно просто создать новый тег в репозитории:

```shell
git tag v0.1.x
git push origin v0.1.x
```

sudo docker exec -it etpgrf-site-etpgrf-backend-1 python etpgrf_site/manage.py createsuperuser
    


e-serg
f0b01jLq$eRyID