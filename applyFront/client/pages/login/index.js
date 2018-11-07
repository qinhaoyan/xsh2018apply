import React from 'react';
import {browserHistory} from 'react-router';
import {post} from '@util/request';
import hex_md5 from '@util/md5';
import './index.scss';

export default class Login extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			isloading: false,
			isNameFocus: false,
			isPWDFocus: false
		}
		this.onSubmit = this.onSubmit.bind(this);
	}
	onSubmit(){
		let name = this.refs.name.value;
		let pwd = this.refs.pwd.value;
		if (!this.state.isloading) {
			this.setState({
				isloading: true
			})
			post('/api/admin/login', {name: name, pwd: hex_md5(pwd+'cquptxsh')})
			.then(re=>{
				if (re.success === 0) {
					alert(re.message);
				}
				if (re.success === 1) {
					alert(re.message);
				}
				if (re.success === 2) {
					browserHistory.push('/admin');
				}
				this.setState({
					isloading: false
				})
			})
			.catch(re=>{
				alert('系统错误,请稍后重试');
				this.setState({
					isloading: false
				})
			})
		}
		
	}
	inputFocus(type) {
		if (type === 'name') {
			this.setState({
				isNameFocus: true
			})
		}
		else {
			this.setState({
				isPWDFocus: true
			})
		}
	}
	inputBlur(type) {
		if (type === 'name') {
			this.setState({
				isNameFocus: false
			})
		}
		else {
			this.setState({
				isPWDFocus: false
			})
		}
	}
	render() {
		return (
			<div className='login' style={{height: window.innerHeight}}>
				<div className="content">
					<div className="title">
						重庆邮电大学学生会
					</div>
					<div>
						<i className={"iconfont icon-yonghu " + (this.state.isNameFocus ? 'input-focus' : '')}/>
						<input type="text" ref="name" onFocus={this.inputFocus.bind(this, 'name')} onBlur={this.inputBlur.bind(this, 'name')} placeholder="请输入用户名"/>
					</div>
					<div>
						<i className={"iconfont icon-mima " + (this.state.isPWDFocus ? 'input-focus' : '')}/>
						<input type="password" ref="pwd" onFocus={this.inputFocus.bind(this, 'pwd')} onBlur={this.inputBlur.bind(this, 'pwd')}  placeholder="请输入密码"/>
					</div>
					<div className="button" onClick={this.onSubmit}>
						<div className="word" style={{display: this.state.isloading ? 'none':'block'}}>登录</div>
						<i className="iconfont icon-icon-loading" style={{display: this.state.isloading ? 'block':'none'}}/>
					</div>
				</div>
				<div className="copy">Copyright &copy; 重庆邮电大学学生会宣传部</div>
			</div>
		)
	}
} 