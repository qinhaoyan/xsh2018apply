import React from 'react';
import { Link } from 'react-router';
import './index.scss';

export default class App extends React.Component {
	render() {
		return (
			<div>
				<div className="nav">
					<div className="content">
						<div className="logo">
							重庆邮电大学学生会招新系统
						</div>
						<Link to="/admin">首页</Link>
						<Link to="/admin/signed">签到信息</Link>
						<Link to="/admin/setting">短信设置</Link>
					</div>
				</div>
				{this.props.children}
				<div className="footer">
					Copyright &copy;  重庆邮电大学学生会宣传部
				</div>
			</div>
		)
	}
}