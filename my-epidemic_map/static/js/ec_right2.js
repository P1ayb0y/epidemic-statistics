var ec_right2 = echarts.init(document.getElementById('r2'), 'dark');

// var mydata = [

// 	{
// 		name: 'Amy Schumer',
// 		value: 4386
// 	},
// 	{
// 		name: 'Jurassic World',
// 		value: 4055
// 	},
// 	{
// 		name: 'Charter Communications',
// 		value: 2467
// 	},
// 	{
// 		name: 'Chick Fil A',
// 		value: 2244
// 	},
// 	{
// 		name: 'Planet Fitness',
// 		value: 1898
// 	},
// 	{
// 		name: 'Pitch Perfect',
// 		value: 1484
// 	},
// 	{
// 		name: 'Express',
// 		value: 1112
// 	},
// 	{
// 		name: 'Home',
// 		value: 965
// 	},
// 	{
// 		name: 'Johnny Depp',
// 		value: 847
// 	},
// 	{
// 		name: 'Lena Dunham',
// 		value: 582
// 	},
// 	{
// 		name: 'Lewis Hamilton',
// 		value: 555
// 	},
// 	{
// 		name: 'KXAN',
// 		value: 550
// 	},
// 	{
// 		name: 'Mary Ellen Mark',
// 		value: 462
// 	},
// 	{
// 		name: 'Farrah Abraham',
// 		value: 366
// 	},
// 	{
// 		name: 'Rita Ora',
// 		value: 360
// 	},
// 	{
// 		name: 'Serena Williams',
// 		value: 282
// 	},
// 	{
// 		name: 'NCAA baseball tournament',
// 		value: 273
// 	},
// 	{
// 		name: 'Point Break',
// 		value: 265
// 	}
// ]

var ec_right2_option = {
	title:{text:"今日疫情热搜"},
	tooltip: {},
	series: [{
		type: 'wordCloud',
		gridSize: 1,
		sizeRange: [12, 55],
		right:null,
		bottom:null,
		left:"left",
		rotationRange: [-45, 0, 25, 90],
		shape: 'pentagon',
		width: "auto",
		height: 300,
		drawOutOfBound: false,
		textStyle: {
			normal: { //添加随机色
				color: function() {
					return 'rgb(' + [
						Math.round(Math.random() * 255),
						Math.round(Math.random() * 255),
						Math.round(Math.random() * 255)
					].join(',') + ')';
				}
			},
			emphasis: {
				shadowBlur: 10,
				shadowColor: '#333'
			}
		},
		data:[]
	}]
};

ec_right2.setOption(ec_right2_option);
