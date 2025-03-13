Fast Api sources- https://campus.datacamp.com/courses/introduction-to-fastapi/fastapi-basics?ex=5
                  https://www.educative.io/courses/rest-api-python-microsoft-azure/introduction-to-fastapi
                  https://talibilat.medium.com/api-beginner-to-advance-building-user-registration-in-fastapi-73db80eed71f

Error Handaling - ChatGpt(Delete the existing database (users.db)
                          (Old passwords are stored in plain text)
                            powershell
                            Copy
                            Edit
                            del users.db  # For Windows
                            rm users.db   # For Linux/Mac
                            Restart FastAPI server
                            bash
                            Copy
                            Edit
                            uvicorn main:app --reload
                            Register again (New users will have their passwords securely hashed)
                            Test login with proper POST request.)
                            
                    **https://stackoverflow.com/questions/66622020/fastapi-detailmethod-not-allowed**

UI - Geeksforgeeks.
