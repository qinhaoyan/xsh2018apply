import React from 'react';
import './index.scss';

export default class Switchpage extends React.Component {
	constructor(props) {
		super(props);
		this.page = 0;
	}
	onGetData(page) {
		if (page > 0 && page <= this.page) {
			this.props.newData(page, this.props.order);
		}
	}
	render() {
		let count = this.props.count;
		this.page = Math.ceil(count / 20);
		let curentpage = this.props.curentpage;
		let div = []
		for (let i = 1; i <= this.page; i++) {
			if (i == curentpage) {
				div.push(<div className="curent" key={i}>{i}</div>)
			}
			else {
				div.push(<div key={i} onClick={this.onGetData.bind(this, i)}>{i}</div>)
			}
		} 
		return (
			<div className='switchpage'>
				<span>共 {count} 条数据</span>
				{this.props.curentpage == 1 || this.props.count == 0 ? null : <div onClick={this.onGetData.bind(this, this.props.curentpage - 1)}>&lt;</div>}
				
				{div}
				{this.props.curentpage == this.page || this.props.count == 0 ? null : <div onClick={this.onGetData.bind(this, this.props.curentpage - 1 + 2)}>&gt;</div>}
				
			</div>
		)
	}
}