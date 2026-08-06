# /books or /book => CRUD
class Book = {
    id : int
    item : BookItem
}

class BookItem = {
    title : str
    publisher : str
    price : int
    isbn : int
}