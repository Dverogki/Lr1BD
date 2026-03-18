# Пункт 1:
def get_column_sorted(self, table_name, column_name, descending=False):
    order = "DESC" if descending else "ASC"
    query = f"SELECT {column_name} FROM '{table_name}' ORDER BY '{column_name}' {order}"
    return self._execute_read(query)

# Пункт 2:
def get_rows_by_id_range(self, table_name, start_id, end_id, id_column="id"):
    query = f"SELECT * FROM '{table_name}' WHERE {id_column} BETWEEN %s AND %s"
    return self._execute_read(query, (start_id, end_id))

# Пункт 3:
def delete_rows_by_id_range(self, table_name, start_id, end_id, id_column="id"):
    query = f"DELETE FROM '{table_name}' WHERE {id_column} BETWEEN %s AND %s"
    return self._execute_write(query, (start_id, end_id))

# Пункт 4:
def get_table_structure(self, table_name):
    query = f"DESCRIBE '{table_name}'"
    return self._execute_read(query)

# Пункт 5:
def get_rows_by_value(self, table_name, column_name, value):
    query = f"SELECT * FROM '{table_name}' WHERE {column_name} = %s"
    return self._execute_read(query, (value))

# ПУНКТ 6:

def drop_table(self, table_name):
    query = f"DROP TABLE IF EXISTS `{table_name}`"
    self._execute_write(query)
    print(f"Таблица `{table_name}` успешно удалена (если существовала).")

# Пункт 7:

def add_column(self, table_name, column_name, data_type):
    query = f"ALTER TABLE `{table_name}` ADD COLUMN `{column_name}` {data_type}"
    self._execute_write(query)
    print(f"Столбец `{column_name}` добавлен.")

def drop_column(self, table_name, column_name):
    query = f"ALTER TABLE `{table_name}` DROP COLUMN `{column_name}`"
    self._execute_write(query)
    print(f"Столбец `{column_name}` удален.")

# Пункт 8:

def export_to_csv(self, table_name, file_path):
    df = self.read(table_name)
    if not df.empty:
        df.to_csv(file_path, index=False)
        print(f"Таблица `{table_name}` успешно экспортирована в {file_path}")
    else:
        print("Таблица пуста или не существует, экспорт не выполнен.")

def import_from_csv(self, table_name, file_path):
    try:
        df = pd.read_csv(file_path)
        records = df.to_dict(orient='records')
        success_count = 0
        for record in records:
            if self.create(table_name, record):
                success_count += 1
        print(f"Успешно импортировано {success_count} строк из {file_path} в таблицу `{table_name}`.")
    except FileNotFoundError:
        print(f"Файл `{file_path}` не найден.")
    except Exception as e:
        print(f"Ошибка при импорте из CSV: {e}")