var ec_left2 = echarts.init(document.getElementById("l2"),"dark")	//容器初始化


var ec_left2_option = {
    title: {
        text: '全国疫情新增趋势',
		top:20,
		left:140,
		
    },
    tooltip: {
        trigger: 'axis',
		axisPointer:{
			type:'line',
			lineStyle:{
				color:'#7171C6'
			}
		},
    },
    legend: {
        data: ['现有确诊','现有疑似','新增确诊','新增疑似'],
		left:"auto",
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    toolbox: {
        feature: {
            saveAsImage: {}
        },
		top:20,
    },
    xAxis:[ {
        type: 'category',
        boundaryGap: false,
        data: []
    }],
    yAxis: [{
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
		
    }],
    series: [
        {
            name: '现有确诊',
            type: 'line',
			smooth:true,
            data: []
        },
        {
            name: '现有疑似',
            type: 'line',
			smooth:true,
            data: []
        },
        {
            name: '新增确诊',
            type: 'line',
			smooth:true,
            data: []
        },
		{
		    name: '新增疑似',
		    type: 'line',
			smooth:true,
		    data: []
		},
    ]
};

ec_left2.setOption(ec_left2_option);


