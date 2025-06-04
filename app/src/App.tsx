import { useEffect, useState } from "react"
import DataPicker from "react-datepicker"
import 'react-datepicker/dist/react-datepicker.css'
import './App.css'
import { SearchIcon } from "lucide-react"

type Post = {
  게시판 : string;
  번호 : number;
  제목 : string;
  작성자 : string;
  작성일 : string;
  조회수 : number;
  링크 : string;
  site : string;
}

function App() {

  const menus = ['랭킹순', '82cook', 'momsHolic','mombebe','lemonTeras','powderRoom'];
  const [posts, setPosts] = useState<Post[]>([]);
  const [date, setDate] = useState<string>(new Date().toISOString().split('T')[0]);
  const [order, setOrder] = useState<'desc' | 'asc'>('desc');
  const [page, setPage] = useState<number>(1);
  const [search, setSearch] = useState<string>('');

  const [isAll, setIsAll] = useState<boolean>(false);
  const [menu, setMenu] = useState<string>('all');

  const handleMenuClick = (menu: string) => {
    setMenu(menu);
    if (menu === 'all') setIsAll(true);
    else setIsAll(false);
  }

  const fetchPosts = async () => {
    try {
      const response = await fetch(`http://localhost:8000/posts/rank?date=${date}&order=${order}&page=${page}&size=20`);
      const data = await response.json();
      setPosts(data.posts);
    } catch (error) {
      console.error('데이터를 불러오는데 실패했습니다.', error);
    }
  }


  useEffect(()=>{

  },[date, order, search, menu, page])
  
  return (
    <div className="container">
      <section id="all-posts" className="section">
        <h1>아카이브</h1>
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
        <div className="search-bar">
          <input type="text" placeholder="검색어를 입력하세요" />
          <button>
            <SearchIcon />
          </button>
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
                <th>링크</th>
              </tr>
            </thead>
            <tbody>
              {/* {Array.from({length:30}).map((_, index) => (
                <tr key={index}>
                  <td>게시판</td>
                  <td>1</td>
                  <td>제목</td>
                  <td>작성자</td>
                  <td>작성일</td>
                  <td>조회수</td>
                </tr>
              ))} */}
              {posts.map((post, index) => (
                <tr key={index}>
                  <td>{post.게시판}</td>
                  <td>{post.번호}</td>
                  <td>{post.제목}</td>
                  <td>{post.작성자}</td>
                  <td>{post.작성일}</td>
                  <td>{post.조회수}</td>
                  <td>{post.링크}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="pagination">
          <button
            onClick={() => setPage(1)}
          >
            처음
          </button>
          <button
            onClick={() => setPage(page - 1)}
          >
            이전
          </button>
          <button
            onClick={() => setPage(page)}
          >{page}</button>
          <button
            onClick={() => setPage(page + 1)}
          >{page+1}</button>
          <button
            onClick={() => setPage(page + 2)}
          >{page+2}</button>
          <button
            onClick={() => setPage(page + 3)}
          >{page+3}</button>
          <button
            onClick={() => setPage(page + 1)}
          >
            다음
          </button>
          <button
            onClick={() => setPage(page + 10)}
          >
            마지막
          </button>
        </div>
      </section>
    </div>
  )
}

export default App
