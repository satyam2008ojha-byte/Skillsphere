import React, {useEffect, useState} from 'react'

const API='http://127.0.0.1:8000/api'

function Login({onLogin}) {
  const [email,setEmail]=useState('trainee@skillsphere.com')
  const [password,setPassword]=useState('123456')
  const [error,setError]=useState('')
  async function submit(e){
    e.preventDefault()
    const r=await fetch(API+'/auth/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email,password})})
    if(!r.ok){setError('Invalid login');return}
    onLogin(await r.json())
  }
  return <div className="center"><form className="card login" onSubmit={submit}>
    <h1>SkillSphere</h1><p>CAPACITY CONNECT • SIH26075</p>
    <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="Email"/>
    <input value={password} onChange={e=>setPassword(e.target.value)} type="password" placeholder="Password"/>
    <button>Login</button>{error&&<p className="error">{error}</p>}
    <small>Demo: trainee@skillsphere.com / trainer@skillsphere.com / admin@skillsphere.com — password 123456</small>
  </form></div>
}

function Trainee({user,logout}){
  const [courses,setCourses]=useState([])
  const [selected,setSelected]=useState(null)
  const [quiz,setQuiz]=useState([])
  const [answers,setAnswers]=useState([])
  const [result,setResult]=useState(null)
  useEffect(()=>{fetch(API+'/courses').then(r=>r.json()).then(setCourses)},[])
  async function enroll(id){await fetch(API+'/courses/enroll',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user_id:user.id,course_id:id})}); alert('Enrolled')}
  async function openQuiz(c){setSelected(c);setResult(null);setAnswers([]);setQuiz(await fetch(API+'/quizzes/'+c.id).then(r=>r.json()))}
  async function submit(){const r=await fetch(API+'/quizzes/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user_id:user.id,course_id:selected.id,answers})});setResult(await r.json())}
  return <><Header user={user} logout={logout}/><main><h2>Trainee Dashboard</h2>
    {!selected ? <div className="grid">{courses.map(c=><div className="card" key={c.id}><h3>{c.title}</h3><p>{c.description}</p><span className="tag">{c.skill_tag}</span><div><button onClick={()=>enroll(c.id)}>Enroll</button> <button onClick={()=>openQuiz(c)}>Quiz</button></div></div>)}</div>:
    <div className="card"><button onClick={()=>setSelected(null)}>← Courses</button><h2>{selected.title} Quiz</h2>
    {quiz.map((q,i)=><div className="question" key={q.id}><b>{i+1}. {q.question}</b>{q.options.map(o=><label key={o}><input type="radio" name={'q'+i} onChange={()=>{let a=[...answers];a[i]=o;setAnswers(a)}}/> {o}</label>)}</div>)}
    <button onClick={submit}>Submit Quiz</button>
    {result&&<div className="result"><h3>Score: {result.score}%</h3>{result.weak_skill?<><p>⚠️ Skill Gap: <b>{result.weak_skill}</b></p><p>Recommended: {result.recommendations.join(', ')}</p></>:<p>🎉 No skill gap detected.</p>}</div>}</div>}
  </main></>
}

function Trainer({user,logout}){return <><Header user={user} logout={logout}/><main><h2>Trainer Dashboard</h2><div className="card"><h3>Course Management</h3><p>Create courses, upload resources and track learner performance.</p><button onClick={()=>alert('Demo action: course creation module')}>Create Course</button></div></main></>}
function Admin({user,logout}){const [a,setA]=useState({});useEffect(()=>{fetch(API+'/analytics').then(r=>r.json()).then(setA)},[]);return <><Header user={user} logout={logout}/><main><h2>Admin Analytics</h2><div className="grid stats"><div className="card"><b>Users</b><strong>{a.users||0}</strong></div><div className="card"><b>Courses</b><strong>{a.courses||0}</strong></div><div className="card"><b>Quiz Attempts</b><strong>{a.attempts||0}</strong></div><div className="card"><b>Average Score</b><strong>{a.average_score||0}%</strong></div></div></main></>}
function Header({user,logout}){return <header><b>SkillSphere</b><span>{user.name} • {user.role}</span><button onClick={logout}>Logout</button></header>}

export default function App(){
 const [user,setUser]=useState(()=>JSON.parse(localStorage.getItem('ss_user')||'null'))
 function login(u){setUser(u);localStorage.setItem('ss_user',JSON.stringify(u))}
 function logout(){setUser(null);localStorage.removeItem('ss_user')}
 if(!user)return <Login onLogin={login}/>
 if(user.role==='trainer')return <Trainer user={user} logout={logout}/>
 if(user.role==='admin')return <Admin user={user} logout={logout}/>
 return <Trainee user={user} logout={logout}/>
}
