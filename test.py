from requests import delete

print(delete('http://localhost:5000/api/v2/news/999').json())
# новости с id = 999 нет в базе

print(delete('http://localhost:5000/api/v2/news/2').json())