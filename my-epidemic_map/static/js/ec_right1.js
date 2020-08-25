var ec_right1 = echarts.init(document.getElementById("r1"),"dark");

var ec_right1_option = {
	title:{
		text: '自治区、直辖市及行政区今日疫情新增趋势top5',
		top:30,
		left:20,
		textStyle:{fontSize:15},
		},
    legend: {},
    tooltip: {},
    dataset: {
        source: []
    },
    xAxis: {
		type: 'category',
		
	},
    yAxis: {
		type: 'value',
		//y轴字体设置
		axisLabel:{
			show:true,
			color:'white',
			fontSize:12,
			formatter:function(value){
				if(value>=1000){
					value = value / 1000 + "k";
				}
				return value;
			}
		},
		//y轴线设置显示
		axisLine:{
			show:true
		},
		//与x轴平行的线样式
		splitLine:{
			show:true,
			lineStyle:{
				color:'#6d606c',
				width:1,
				type:"solid",
			}
		}
	},
    // Declare several bar series, each will be mapped
    // to a column of dataset.source by default.
    series: [
        {type: 'bar'},
        {type: 'bar'},
    ]
};

ec_right1.setOption(ec_right1_option);