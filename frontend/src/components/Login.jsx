import React, {useState} from 'react'

function Login() {
	const [username, setUsername] = useState("")
	const [password, setPassword] = useState("")

	const handleSubmit = () => {
		var data = new FormData();
		data.append("username", username);
		data.append("password", password);
		const response = fetch("https://6228-103-213-210-210.in.ngrok.io/login", {
			method: "POST",
			crossDomain: true,
			headers: { "Content-Type": "application/x-www-form-urlencoded" },
			body: data
		}).then((response) => response.json()).then((res)=>{console.log(res)})
	}
	return (

		<div className="auth-wrapper">
		<div className="auth-inner">


		<form onSubmit={(e)=>{
			e.preventDefault()
			console.log(username, password)
			handleSubmit()
		}}>
		  <h3>Sign In</h3>
		  <div className="mb-3">
			<label>Username</label>
			<input
			  type="username"
			  className="form-control"
			  placeholder="Enter username"
			  value={username}
			  onChange={(e)=>{
				  setUsername(e.target.value)
				}}
				/>
		  </div>
		  <div className="mb-3">
			<label>Password</label>
			<input
			  type="password"
			  className="form-control"
			  placeholder="Enter password"
			  value={password}
			  onChange={(e)=>{
				  setPassword(e.target.value)
				}}
				/>
		  </div>
		  <div className="mb-3">
			<div className="custom-control custom-checkbox">
			  <input
				type="checkbox"
				className="custom-control-input"
				id="customCheck1"
				/>
			  <label className="custom-control-label" htmlFor="customCheck1">
				Remember me
			  </label>
			</div>
		  </div>
		  <div className="d-grid">
			<button type="submit" className="btn btn-primary">
			  Submit
			</button>
		  </div>
		</form>
				</div>
			  </div>
	  )
}

export default Login