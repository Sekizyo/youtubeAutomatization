import sqlite3
from sqlite3 import Error

class databaseManager():
  def __init__(self):
    self.databasePath = '/media/joseph/HDD1/Py_projects/youtubeAutomatization/modules/storage/database.sqlite'
    self.connection = self.createConnection()

  def createConnection(self):
    connection = None
    try:
        connection = sqlite3.connect(self.databasePath)
        print("Connection to SQLite DB successful")

    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

  def closeConnection(self):
    if self.connection:
      self.connection.close()

  def createVideoTableQuery(self):
    query = f"""CREATE TABLE IF NOT EXISTS videos(
      ID INTEGER PRIMARY KEY AUTOINCREMENT,
      authorID INTEGER,
      title TEXT NOT NULL,
      description TEXT,
      uploaded BOOL NOT NULL,
      localization TEXT NOT NULL,
      soundcloudLink TEXT NOT NULL
      );
      """
      
    response = self.executeQuery(query)
    return response

  def createAuthorTableQuery(self):
    query = f"""CREATE TABLE IF NOT EXISTS author(
      ID INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      soundcloudLink TEXT NOT NULL
      );
      """

    response = self.executeQuery(query)
    return response


  def basicSelectQuery(self, data, table):
    query = f'SElECT {data} FROM {table} WHERE 1'
    
    response = self.executeQuery(query)
    return response

  def insertIntotQuery(self, tableName, columns, values):
    query = f'INSERT INTO {tableName}({", ".join(columns)}) VALUES ({", ".join(values)});'
    
    response = self.executeQuery(query)
    return response

  def dropTabletQuery(self, tableName):
    try:
        query = f'DROP TABLE {tableName}'

        response = self.executeQuery(query)
        return response

    except:
      raise

  def executeQuery(self, query):
    cursor = self.connection.cursor()

    try:
      response = cursor.execute(query).fetchall()
      print(f'---- response - {response}')

      self.connection.commit()
      print("Query executed successfully")

      return response

    except:
      raise




manager = databaseManager()
manager.basicSelectQuery('*', 'videos')
# manager.dropTabletQuery('videos')