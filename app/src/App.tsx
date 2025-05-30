import { useState } from "react"
import DataPicker from "react-datepicker"
import 'react-datepicker/dist/react-datepicker.css'
import './App.css'

type Data = {
  site: string;
  board: string;
  id: number;
  title: string;
  writer: string;
  date: string;
  view: number;
}
function App() {

  const menus = ['all', '82cook', 'momsHolic','mombebe','lemonTeras','powderRoom'];
  const [menu, setMenu] = useState<string>('all');
  const [selectedDate, setSelectedDate] = useState<Date | null>(null);
  const [isOpen, setIsOpen] = useState<boolean>(false);

  const handleMenuClick = (menu: string) => {
    setMenu(menu);
  }

  const handleDateChange = (date: Date) => {
    setSelectedDate(date);
  }


  return (
    <div className="container">
      <section id="all-posts" className="section">
        <h2>전체 사이트 게시글</h2>
        <div className='menu'>
          {menus.map((menu) => (
            <button key={menu}
              className={`menu__item ${menu === menu ? 'active' : ''}`} 
              onClick={() => handleMenuClick(menu)}
            >
              {menu}
            </button>
          ))}
        </div>
        <div id="post-list" className="post-list">
          <table>
            <thead>
              <tr>
                <th>게시판</th>
                <th>번호</th>
                <th>제목</th>
                <th>작성자</th>
                <th>작성일</th>
                <th>조회수</th>
              </tr>
            </thead>
            <tbody>
              {Array.from({length:30}).map((_, index) => (
                <tr key={index}>
                  <td>게시판</td>
                  <td>1</td>
                  <td>제목</td>
                  <td>작성자</td>
                  <td>작성일</td>
                  <td>조회수</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="pagination">
          <button>이전</button>
          <button>1</button>
          <button>2</button>
          <button>3</button>
          <button>4</button>
          <button>5</button>
          <button>다음</button>
        </div>
      </section>
      <aside id="all-ranking" className="ranking-section">
        <h2>랭킹</h2>
        <div className='date-picker-container'>
            <DataPicker
              id="date-picker"
              selected={selectedDate}
              onChange={(date) => handleDateChange(date ?? new Date())}
              onCalendarOpen={() => setIsOpen(true)}
              onCalendarClose={() => setIsOpen(false)}
              dateFormat="yyyy-MM-dd"
              className="date-picker"
              placeholderText="날짜 선택"
            />
        </div>
        <div id="ranking-list" className="ranking-list">
          <table>
            <thead>
              <tr>
                <th>순위</th>
                <th>사이트 이름</th>
                <th>게시판</th>
                <th>제목</th>
              </tr>
            </thead>
            <tbody>
              {Array.from({length:10}).map((_, index) => (
                <tr key={index}>
                  <td>순위</td>
                  <td>82cook</td>
                  <td>게시판</td>
                  <td>제목</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </aside>
    </div>
  )
}

export default App
