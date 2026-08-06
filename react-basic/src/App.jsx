import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
// import './App.css'

export default function App() {
  const [form, setForm] = useState({
                              "title" : "",
                              "price" : "",
                              "isbn" : ""
                            })
  const handleformChange = (e) => {
    // e(이벤트)로 불러온 정보 구조분해 할당
    const {name, value} = e.target
    // console.log(name, value)
    setForm({...form, [name]:value})
  }

  // console.log(form)

  const handleSubmit = async (e) => {
    e.preventDefault()
    console.log(form)
    // validation 생략

    // fastAPI 호출 : fastAPI 주소 http://http://127.0.0.1:8000/book => POST
    const response = await fetch(
      "/api/book",
      {
        method : "POST",
        headers : {
          "Content-Type" : "application/json"
        },
        body : JSON.stringify(form)
      }
    )

    const result = await response.json()
    console.log(result)
  }

  return (
    <>
      <h2>도서 관리 프로그램</h2>
      <form onSubmit={handleSubmit}>
        <ul>
          <li>
            <label>제목 : </label>
            <input type="text" name='title' value={form.title} onChange={handleformChange}/>
          </li>
          <li>
            <label>가격 : </label>
            <input type="text" name='price'value={form.price} onChange={handleformChange}/>
          </li>
          <li>
            <label>ISBN : </label>
            <input type="text" name='isbn'value={form.isbn} onChange={handleformChange}/>
          </li>
          <li>
            <button type='submit'>등록</button>
          </li>
        </ul>
      </form>
    </>
  )
}
