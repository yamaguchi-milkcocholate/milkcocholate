import pymysql.cursors
import pickle


def toggle_sell_and_stay(genome):
    new_genome = list()
    for el in genome:
        el_genome = list()
        for cell in el:
            if cell == 1:
                el_genome.append(1)
            elif cell == 2:
                el_genome.append(3)
            elif cell == 3:
                el_genome.append(2)
            else:
                raise TypeError()
        new_genome.append(el_genome)
    return new_genome


user = 'milkcocholate'
password = 'milkchocolate22'
db = 'milkcocholate'
charset = 'utf8'
host = 'localhost'

try:
    connection = pymysql.connect(
        host=host,
        user=user,
        db=db,
        password=password,
        charset=charset,
        cursorclass=pymysql.cursors.DictCursor
    )
except pymysql.err.OperationalError:
    raise

sql = "SELECT * FROM `populations` WHERE 1;"

try:
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
except Exception:
    connection.close()
    raise
finally:
    connection.close()

update_list = list()

for population in result:
    update_list.append(dict())
    update_list[-1]['id'] = population['id']
    update_list[-1]['genome'] = toggle_sell_and_stay(pickle.loads(population['genome']))


sql = "UPDATE `populations` SET `genome` = %s WHERE `id` = %s;"
for update in update_list:
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            db=db,
            password=password,
            charset=charset,
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.err.OperationalError:
        raise

    placeholder = list()
    placeholder.append(pickle.dumps(update['genome']))
    placeholder.append(update['id'])
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, placeholder)
            connection.commit()
    except Exception:
        connection.rollback()
        connection.close()
        raise
    finally:
        connection.close()
