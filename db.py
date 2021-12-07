import os
from typing import Dict, List, Tuple
import sqlite3

connec = sqlite3.connect(os.path.join("db", "finance.db"))
curs = connec.cursor()
curs.execute('pragma encoding')

def insert(table: str, col_val: Dict):
	cols = ', '.join(col_val.keys())
	vals = [tuple(col_val.values())]
	place = ', '.join("?" * len(col_val.keys()))
	curs.executemany(
		f"INSERT INTO {table} "
		f"({cols}) "
		f"VALUES ({place})",
		vals)
	connec.commit()

def fetchall(table: str, columns: List[str]) -> List[Tuple]:
	columns_join = ', '.join(columns)
	curs.execute(f"SELECT {columns_join} FROM {table}")
	rows = curs.fetchall()
	result = []
	for row in rows:
		dict_row = {}
		for index, column in enumerate(columns):
			dict_row[column] = row[index]
		result.append(dict_row)
	return result

def delete(table: str, row_id: int) -> None:
	row_id = int(row_id)
	curs.execute(f"delete from {table} where id={row_id}")
	connec.commit()

def get_cursor():
	return curs

#Инициализирует БД
def _init_db():
	with open("createdb.sql", "r") as f:
		sql = f.read()
	curs.executescript(sql)
	connec.commit()

#Проверяет, инициализирована ли БД, если нет — инициализирует
def check_db_exists():
	curs.execute("SELECT name FROM sqlite_master "
				"WHERE type='table' AND name='expense'")
	table_exists = curs.fetchall()
	if table_exists:
		return
	_init_db()

check_db_exists()
