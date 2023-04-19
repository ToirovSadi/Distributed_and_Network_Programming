import sqlite3
from concurrent.futures import ThreadPoolExecutor

import grpc
import schema_pb2 as stub
import schema_pb2_grpc as service

SERVER_ADDR = '0.0.0.0:1234'
SQL_FILE = 'db.sqlite'

class Database(service.DatabaseServicer):
    def __init__(self, db_filename):
        self.db_filename = db_filename
        
        # create a table for user
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('create table if not exists Users(id interger, name string)')
        conn.commit()
        conn.close()


    def get_connection(self):
        return sqlite3.connect(self.db_filename)
    
    
    def PutUser(self, request, context):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(' \
                                    insert or replace \
                                    into Users(id, name) \
                                    values (?, ?)', 
                                    (request.user_id, request.user_name)
                            )
            conn.commit()
            print(f"PutUser({request.user_id}, '{request.user_name}')")
            return stub.Status(status=True)
        except Exception as e:
            print(f'{(SERVER_ADDR)}: PutUser() failed with an error: {e}')
            return stub.Status(status=False)
        finally:
            conn.close()


    def GetUsers(self, request, context):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor = conn.cursor()
        try:
            cursor.execute(
                                'select id, name \
                                    from Users'
                                )
            data = cursor.fetchall()
            users = []
            for user in data:
                users.append(
                    stub.User(
                        user_id=user[0],
                        user_name=user[1]
                    )
                )
            print("GetUsers()")
            return stub.UsersResponse(users=users)
        except Exception as e:
            print(f'{(SERVER_ADDR)}: GetUsers() failed with an error: {e}')
            return stub.UsersResponse()
        finally:
            conn.close()

    def DeleteUser(self, request, context):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor = conn.cursor()
        try:
            cursor.execute(
                                    'delete from Users \
                                    where id = ?',
                                    (request.user_id,)
                                )
            conn.commit()
            print(f"DeleteUser({request.user_id})")
            return stub.Status(status=True)
        except Exception as e:
            print(f'{(SERVER_ADDR)}: DeleteUser() failed with an error: {e}')
            return stub.Status(status=False)
        finally:
            conn.close()


if __name__ == '__main__':
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    service.add_DatabaseServicer_to_server(Database(SQL_FILE), server)
    server.add_insecure_port(SERVER_ADDR)
    server.start()
    
    print(f'gRPC server is listening on {SERVER_ADDR}')
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)
