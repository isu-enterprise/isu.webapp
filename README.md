# An enterprise automation developing platform `isu.enterprise`

An enterprise platform prototype based on component architecture

Setup ISU proxy.
```bash
git config --global http.proxy http://proxy.isu.ru:3128
```

Setup user name and e-mail

```bash
git config --global user.name "ISU student."
git config --global user.email "lab@irnok.net"
```

Clone project with

```bash
git clone https://github.com/<GITHUB-USER-NAME>/isu.enterprise.git
cd isu.enterprise
```

Substitution `<GITHUB-USER-NAME>` may be `eugeneai`.

Then install required packages and make the package a package itself.

```bash
pip install -r requirements.txt
python setup.py develop
```

Run the WEB-server

```bash
pserve development.ini --reload
```

Develop something

## Creating PostreSQL storage

Хранилище инсталлируется множеством способов, но один из удобных - это
устанавливать его в Linux в системе виртуальных машин Docker.

```bash
docker run --name generic-postgres -e POSTGRES_PASSWORD=<Пароль суперпользователя> \
           -p 15432:5432 -d --restart always postgres
```

Здесь `<Пароль суперпользователя>` - пароль, который задаете вы, он вам понадобиться для
подключения к серверу `PostreSQL` суперпользователем `postgres`.

Затем, если у вас есть утилита `psql` набираем `CREATE`- и `GRANT` - команды. Перед подключением
`psql` затребует ввод пароля.

```bash
$ psql -h 127.0.0.1 -U postgres -p 15432
Password for user postgres:
psql (9.6.1, server 9.6.2)
Type "help" for help.

postgres=# CREATE USER acc WITH PASSWORD 'acc';
postgres=# CREATE DATABASE acc;
postgres=# GRANT ALL PRIVILEGES ON DATABASE acc TO acc;
postgres=# \q
```
Теперь надо проверить результат создания базы данных `acc` и пользователя
`acc` - администратора этой базы.  Его пароль - `acc`.

```bash
$ psql -h 127.0.0.1 -U acc -p 15432 acc
Password for user acc:
psql (9.6.1, server 9.6.2)
Type "help" for help.

acc=> \q
```
В командной строке `-U acc` - указание пользователя, а последний `acc` - имя базы данных.
Если `psql` выдал `acc=>`, то значит все сработало.

# Методический материал

  * Методичка по компонентной архитектуре Питона - https://github.com/eugeneai/ZCA/raw/hb/zca.pdf;
  * Оригинал на английском - http://muthukadan.net/docs/zca.html;

**надо найти методический материал по ведению бухгалтерии в стиле 1С**

# This file requires editing

Note to the author: Please add something informative to this README **before**
releasing your software, as `a little documentation goes a long way`_.  Both
README.rst (this file) and NEWS.rst (release notes) will be included in your
package metadata which gets displayed in the PyPI page for your project.

You can take a look at other projects, such as `pyramid's README.txt
<https://github.com/Pylons/pyramid/blob/master/README.rst>` for some ideas.

`a little documentation goes a long way`: http://www.martinaspeli.net/articles/a-little-documentation-goes-a-long-way

Credits
-------

- `Distribute`_
- `modern-package-template`_

Distribute: http://code.activestate.com/pypm/distribute/

`modern-package-template`: http://code.activestate.com/pypm/modern-package-template/
