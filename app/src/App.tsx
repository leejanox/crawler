import { useEffect, useState } from "react";
import 'react-datepicker/dist/react-datepicker.css';
import './App.css';
import { SearchIcon } from "lucide-react";

type Post = {
  게시판: string;
  번호: number;
  제목: string;
  작성자: string;
  작성일: string;
  조회수: number;
  링크: string;
  site: string;
};

type GroupedPosts = {
  [board: string]: Post[];
};

function App() {
  const menus = ['all', 'cook82', 'momsHolic', 'momBeBe', 'lemonT', 'powderRoom'];
  const [posts, setPosts] = useState<GroupedPosts>({});
  const [date, setDate] = useState<string>('20250604');
  const [order, setOrder] = useState<'desc' | 'asc'>('desc');
  const [page, setPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [search, setSearch] = useState<string>('');
  const [menu, setMenu] = useState<string>('all');

  const handleMenuClick = (menu: string) => {
    setMenu(menu);
    setPage(1); // 메뉴 바뀌면 페이지 초기화
  };

  const fetchPosts = async () => {
    try {
      const url = `http://localhost:8000/posts/rank?date=${date}&order=${order}&page=${page}&size=20${menu !== 'all' ? `&menu=${menu}` : ''}${search ? `&search=${encodeURIComponent(search)}` : ''}`;
      const response = await fetch(url);
      const data = await response.json();
      console.log('API 응답:', data);

      if (data.posts && typeof data.posts === 'object') {
        setPosts(data.posts);
        setTotalPages(data.total_pages || 1);
      } else {
        setPosts({});
        setTotalPages(1);
      }
    } catch (error) {
      console.error('데이터 로드 실패:', error);
      setPosts({});
      setTotalPages(1);
    }
  };

  useEffect(() => {
    fetchPosts();
  }, [ menu, page]);

  return (
    <div className="container">
      <section id="all-posts" className="section">
        <h1>아카이브</h1>

        <div className="menu">
          {menus.map((menuName) => (
            <button key={menuName}
              className={`menu__item ${menu === menuName ? 'active' : ''}`}
              onClick={() => handleMenuClick(menuName)}
            >
              {menuName}
            </button>
          ))}
        </div>

        <div className="search-bar">
          <input
            type="text"
            placeholder="검색어를 입력하세요"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <button  onClick={() => { setPage(1); fetchPosts(); }}>
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
              {Object.entries(posts).map(([boardName, postList]) => (
                <>
                  <tr key={boardName}>
                    <td colSpan={7} style={{ fontWeight: 'bold', backgroundColor: '#eee' }}>
                      {boardName}
                    </td>
                  </tr>
                  {postList.map((post, index) => (
                    <tr key={`${boardName}-${index}`}>
                      <td>{post.게시판}</td>
                      <td>{post.번호}</td>
                      <td>{post.제목}</td>
                      <td>{post.작성자}</td>
                      <td>{post.작성일}</td>
                      <td>{post.조회수}</td>
                      <td>
                        <a href={post.링크} target="_blank" rel="noopener noreferrer">바로가기</a>
                      </td>
                    </tr>
                  ))}
                </>
              ))}
            </tbody>
          </table>
        </div>

        <div className="pagination">
          <button onClick={() => setPage(1)} disabled={page === 1}>처음</button>
          <button onClick={() => setPage(prev => Math.max(1, prev - 1))} disabled={page === 1}>이전</button>
          <span>{page} / {totalPages}</span>
          <button onClick={() => setPage(prev => Math.min(totalPages, prev + 1))} disabled={page >= totalPages}>다음</button>
          <button onClick={() => setPage(totalPages)} disabled={page >= totalPages}>마지막</button>
        </div>
      </section>
    </div>
  );
}

export default App;
