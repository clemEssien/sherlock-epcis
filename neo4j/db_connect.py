from neo4j import GraphDatabase

class Neo4jConnection:

    def __init__(self, uri, user, password):
        self.__uri = uri
        self.__user = user
        self.__password= password
        self.__driver = None
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__password))
        except Exception as e:
            print("Unable to create the driver:", e)

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def query(self, query, parameters=None, db='Neo4j'):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
            response = list(session.run(query, parameters))
        except Exception as e:
            response = str(e)
            print("Query was not successful:", e)
        finally: 
            if session is not None:
                session.close()
        return response
