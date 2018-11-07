import React from 'react';
import {get} from '@util/request';
import Row from './tablerow';
import './index.scss';


export default class Table extends React.Component {
	constructor(props) {
		super(props);
		
		/*this.onAllChoose = this.onAllChoose.bind(this);
		this.onChildChoose = this.onChildChoose.bind(this);*/
	}
	/*onAllChoose() {
		let id = this.props.stu_id;
		let chooseList = [];
		if (this.state.allchoose) {
			this.setState({
				allchoose: false,
				choose: -1,
				chooseList: []
			})
		}
		else {
			chooseList = this.state.data.map((re, i)=>{return re.stu_id});
			this.setState({
				allchoose: true,
				choose: 1,
				chooseList: chooseList
			})
		}
		this.props.getChooseList(chooseList);
	}
	onChildChoose(stu_id, type) {
		let chooseList = this.state.chooseList;
		if (type === 1) {
			chooseList.push(stu_id);
		}
		else {
			let index = chooseList.indexOf(stu_id);
			chooseList.splice(index, 1);
		}
		this.setState({
			choose: 0,
			allchoose: false,
			chooseList: chooseList
		})
		this.props.getChooseList(chooseList);
	}*/
	changeOrder(order){
		this.props.onChangeOrder(order);
	}
	render() {
		let row = this.props.data.map((re, i)=>{
			/*return (<Row {...re} key={i} choose={this.state.choose} onChildChoose={this.onChildChoose}/>)*/
			return (<Row {...re} key={i} signed={this.props.signed}/>)
		});
		return (
			<div className="content">
				<table border='0' cellSpacing='0' cellPadding='0' className="table">
					<thead >
						<tr>
							{/*<td>
								<div className="checkbox" onClick={this.onAllChoose}>
									<i className="iconfont icon-xuanzhong" style={{opacity: this.state.allchoose ? 1 : 0}}></i>
								</div>
							</td>*/}
							<td className='name'>姓名</td>
							<td className='stu-id'>学号</td>
							<td className='sex'>性别</td>
							<td className='academy'>学院</td>
							<td className='tel'>电话</td>
							<td className='QQ'>QQ</td>
							<td className='asp'>志愿</td>
							{!this.props.signed ? <td className="isAdjust">调剂</td> : null}
							{!this.props.signed ? <td colSpan="2" className="func" onClick={this.changeOrder.bind(this, 'scale1')}>初试<i className="iconfont icon-sort-up-copy1" /></td> : null}
							{!this.props.signed ? <td colSpan="2" className="func" onClick={this.changeOrder.bind(this, 'scale2')}>复试<i className="iconfont icon-sort-up-copy1" /></td> : null}
							{!this.props.signed ? <td colSpan="2" className="func" onClick={this.changeOrder.bind(this, 'scale3')}>终面<i className="iconfont icon-sort-up-copy1" /></td> : null}		
						</tr>
					</thead>
					<tbody>
						{row.length == 0 ? null : row}
					</tbody>
				</table>
					{row.length == 0 ? <div className='no-data'>暂时还没有数据</div> : null}
				
			</div>
		)
	}
}