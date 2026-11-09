import pandas as pd
import clickhouse_connect
import mysql.connector

def ucitaj_posete_iz_clickhouse():
    client = clickhouse_connect.get_client(
        host="1",
        port=8123,
        username="zadatak",
        password="z",
        database="zadatak"
    )

    upit = """
        SELECT
            toMonth(log_time) AS mesec,
            multiIf(
                position(request_uri, 'ad_id=') > 0,
                extract(request_uri, 'ad_id=([0-9]+)'),

                position(request_uri, '/eds/') > 0,
                extract(request_uri, '/eds/([0-9]+)'),

                position(request_uri, 'oglas/') > 0,
                extract(request_uri, 'oglas/([0-9]+)'),

                ''
            ) AS ad_id,
            count() AS broj_poseta
        FROM app_hits_v2
        WHERE event_type = 'ad_view'
          AND (
              position(request_uri, 'ad_id=') > 0
              OR position(request_uri, '/eds/') > 0
              OR position(request_uri, 'oglas/') > 0
          )
        GROUP BY
            mesec,
            ad_id
        HAVING ad_id != ''
        ORDER BY
            mesec,
            broj_poseta DESC
    """
    rezultat = client.query_df(upit)
    client.close()

    return rezultat

def ucitaj_oglase_iz_mysql():
    konekcija = mysql.connector.connect(
        host="1",
        port=3306,
        user="zadatak",
        password="z",
        database="zadatak"
    )

    upit = """
        SELECT
            a.ad_id,
            a.group_id,
            c.name AS category_name
        FROM ad AS a
        LEFT JOIN category AS c
            ON a.category_id = c.category_id
    """

    kursor = konekcija.cursor(dictionary=True)
    kursor.execute(upit)

    podaci = kursor.fetchall()

    kursor.close()
    konekcija.close()

    return pd.DataFrame(podaci)