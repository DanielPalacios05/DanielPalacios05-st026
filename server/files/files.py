# files.py

import sqlite3
import grpc
from concurrent import futures
import files_pb2
import files_pb2_grpc
import traceback

# Initialize an SQLite database (create or connect to an existing one)
db_connection = sqlite3.connect("files.db")
db_cursor = db_connection.cursor()

# Create a table to store file information
db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY,
        filename TEXT,
        filepath TEXT
    )
""")
db_connection.commit()

class FilesServicer(files_pb2_grpc.FilesServicer):
    def listAvailableFiles(self, request, context):
        try:
            conn = sqlite3.connect('files.db')
            c = conn.cursor()
            c.execute("SELECT filename, filepath FROM files")
            files = c.fetchall()
            response = files_pb2.AvailableFilesResponse()
            for filename, filepath in files:
                file_info = files_pb2.File(filename=filename,filepath=filepath)
                response.file.append(file_info)

            conn.close()
            return response
        except Exception as e:
            print(traceback.format_exc())
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return files_pb2.AvailableFilesResponse()

    def addFile(self, request, context):
        try:
            conn = sqlite3.connect('files.db')
            c = conn.cursor()
            filename = request.file.filename
            print(request)
            filepath = request.file.filepath
            c.execute("SELECT id FROM files WHERE filename=?", (filename,))
            existing_file = c.fetchone()
            if existing_file:
                # Update the existing file's filepath
                c.execute("UPDATE files SET filepath=? WHERE id=?", (filepath, existing_file[0]))
            else:
                # Insert a new file
                c.execute("INSERT INTO files (filename, filepath) VALUES (?, ?)", (filename, filepath))
            conn.commit()
            conn.close()
            return files_pb2.AddFileResponse(isFileUploaded=True)
        except Exception as e:
            print(traceback.format_exc())
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return files_pb2.AddFileResponse(isFileUploaded=False)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    files_pb2_grpc.add_FilesServicer_to_server(FilesServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server listening on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
