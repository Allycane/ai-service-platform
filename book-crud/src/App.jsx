import { useState, useEffect } from 'react';

const initialBooks = [
  { id: 1, title: '자바의 정석', author: '남궁성', publisher: '도우출판', year: 2016, status: '대여가능' },
  { id: 2, title: '클린 코드', author: '로버트 마틴', publisher: '인사이트', year: 2013, status: '대여중' },
  { id: 3, title: '이펙티브 자바', author: '조슈아 블로크', publisher: '인사이트', year: 2018, status: '대여가능' },
];

const emptyForm = { title: '', author: '', publisher: '', year: '', status: '대여가능' };

export default function App() {
  // const [books, setBooks] = useState(initialBooks);
  const [form, setForm] = useState(emptyForm);
  const [editingId, setEditingId] = useState(null);
  const [keyword, setKeyword] = useState('');
  const [books, setBooks] = useState([]);
  const [isLoad, setIsLoad] = useState(true);

  const isEditing = editingId !== null;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async(e) => {
    e.preventDefault();
    if (!form.title.trim() || !form.author.trim()) {
      alert('제목과 저자는 필수입니다.');
      return;
    }

    if (isEditing) {
      // 수정 - id, formdata
      const response = await fetch(
        `/fastapi/book/${editingId}`,
        {
          "method" : "PUT",
          "headers" : {
            "Content-Type" : "application/json"
          },
          "body" : JSON.stringify(form)
        }
      )
      const data = await response.json()
      if(data.isUpdate) setIsLoad(!isLoad)
      console.log(data)

    } else {
      const newBook = {
        ...form,
        year: String(form.year) || '',
      };
      setBooks((prev) => [newBook, ...prev]);


      // FastAPI 연동 로직
      // console.log('newBook =>', newBook);
      const response = await fetch(
        '/fastapi/book',
        {
          "method" : "POST",
          "headers" : {
            "Content-Type" : "application/json"
          },
          "body" : JSON.stringify(newBook)
        }
      )
      const data = await response.json()
      if(data !== null) setIsLoad(!isLoad)

      console.log('data =>', data.message)
      // console.log('data =>', data.book.title)
      
    }
    handleCancel();
  };

  const handleEdit = (book) => {
    setEditingId(book.id);
    setForm({
      title: book.title,
      author: book.author,
      publisher: book.publisher,
      year: book.year,
      status: book.status,
    });
  };

  const handleDelete = async(id) => {
    if (!confirm('이 도서를 삭제하시겠습니까?')) return;
    // DB 연동하는 형태로 변경
    const response = await fetch(
        `/fastapi/book/${id}`,
        {
          "method" : "DELETE",
          "headers" : {
            "Content-Type" : "application/json"
          },
          "body" : null
        }
      )
      const data = await response.json()
      console.log(data)
      if(data.isDelete) setIsLoad(!isLoad)
  };

  const handleCancel = () => {
    setEditingId(null);
    setForm(emptyForm);
  };

  const filteredBooks = books.filter(
    (b) =>
      b.title.toLowerCase().includes(keyword.toLowerCase()) ||
      b.author.toLowerCase().includes(keyword.toLowerCase())
  );

  useEffect(() => {
    const loadFetch = async() => {
      const response = await fetch('/fastapi/books')
      const data = await response.json();
      setBooks(data.books);
    }
    // 해당 함수를 호출해야 정상적으로 실행됨
    loadFetch()
  }, [isLoad])

  return (
    <div className="page">
      <h1 className="page-title">📚 도서 관리</h1>

      <form className="book-form" onSubmit={handleSubmit}>
        <div className="form-row">
          <input
            name="title"
            placeholder="제목"
            value={form.title}
            onChange={handleChange}
          />
          <input
            name="author"
            placeholder="저자"
            value={form.author}
            onChange={handleChange}
          />
          <input
            name="publisher"
            placeholder="출판사"
            value={form.publisher}
            onChange={handleChange}
          />
          <input
            name="year"
            type="number"
            placeholder="출판년도"
            value={form.year}
            onChange={handleChange}
          />
          <select name="status" value={form.status} onChange={handleChange}>
            <option value="대여가능">대여가능</option>
            <option value="대여중">대여중</option>
          </select>
        </div>
        <div className="form-actions">
          <button type="submit" className="btn btn-primary">
            {isEditing ? '수정 완료' : '도서 등록'}
          </button>
          {isEditing && (
            <button type="button" className="btn btn-ghost" onClick={handleCancel}>
              취소
            </button>
          )}
        </div>
      </form>

      <div className="toolbar">
        <input
          className="search-input"
          placeholder="제목 또는 저자로 검색"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
        />
        <span className="book-count">총 {filteredBooks.length}권</span>
      </div>

      <table className="book-table">
        <thead>
          <tr>
            <th>제목</th>
            <th>저자</th>
            <th>출판사</th>
            <th>출판년도</th>
            <th>상태</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {books.length === 0 ? (
            <tr>
              <td colSpan={6} className="empty-row">
                등록된 도서가 없습니다.
              </td>
            </tr>
          ) : (
            books.map((book) => (
              <tr key={book.id} className={editingId === book.id ? 'row-editing' : ''}>
                <td>{book.title}</td>
                <td>{book.author}</td>
                <td>{book.publisher}</td>
                <td>{book.year}</td>
                <td>
                  <span className={`badge ${book.status === '대여가능' ? 'badge-ok' : 'badge-out'}`}>
                    {book.status}
                  </span>
                </td>
                <td className="row-actions">
                  <button className="btn btn-small" onClick={() => handleEdit(book)}>
                    수정
                  </button>
                  <button className="btn btn-small btn-danger" onClick={() => handleDelete(book.id)}>
                    삭제
                  </button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
