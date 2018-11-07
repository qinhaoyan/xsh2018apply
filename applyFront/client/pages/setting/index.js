import React from 'react';
import SortMessage from '@components/sortmessage';
import {post,get} from '@util/request';
import {browserHistory} from 'react-router';
import './index.scss';

export default class Setting extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			BU:''
		}
		get('/api/admin/getBUName')
		.then(re=>{
			if (re.success == 2) {
				this.setState({
					BU: re.BU
				})
			}
			if (re.success == 0) {
				alert(re.message);
				browserHistory.push('/admin/login')
			}
		})
		.catch(err=>{
			alter('系统错误，请稍后重试！')
		})
	}
	render() {
		return (
			<div className='setting'>
				<div className="setting-title">短信设置</div>
				<div className="content">
					<SortMessage 
						title='一面通知短信'
						template={`【重邮学生会】XXX同学：你好，你已成功报名重庆邮电大学学生会${this.state.BU}，校会君诚邀你参加第一轮面试。
									<br/>
									面试时间：①
									<br/>
									面试地点：② 
									<br/>
									期待你的精彩表现，祝面试顺利。`}
						count='2'
						type="1"
					/>
					<SortMessage 
						title='二面通知短信'
						template={`【重邮学生会】XXX同学：你好，恭喜你通过了重庆邮电大学学生会${this.state.BU}第一轮面试，校会君诚邀你参加第二轮面试。
									<br/>
									面试时间：①
									<br/>
									面试地点：② 
									<br/>
									期待你的精彩表现，祝面试顺利。`}
						count='2'
						type="2"
					/>
					<SortMessage 
						title='三面通知短信'
						template={`【重邮学生会】XXX同学：你好，恭喜你通过了重庆邮电大学学生会${this.state.BU}第二轮面试，校会君诚邀你参加第三轮面试。
									<br/>
									面试时间：①
									<br/>
									面试地点：② 
									<br/>
									期待你的精彩表现，祝面试顺利。`}
						count='2'
						type="3"
					/>
					<SortMessage 
						title='通过面试通知'
						template={`【重邮学生会】XXX同学：你好，恭喜你通过了重庆邮电大学学生会${this.state.BU}第二轮面试，校会君诚邀你参加第三轮面试。
									<br/>
									面试时间：①
									<br/>
									面试地点：② 
									<br/>
									期待你的精彩表现，祝面试顺利。`}
						count='0'
						type="4"
					/>
					
				</div>
			</div>
		)
	}
}