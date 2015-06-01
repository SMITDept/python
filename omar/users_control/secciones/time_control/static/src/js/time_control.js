openerp.time_control = function (instance) {
instance.web.client_actions.add('example.action', 'instance.time_control.Action');
instance.time_control.Action = instance.web.Widget.extend({
    template: 'time_control.action',
    events: {
            'click .oe_time_control_timer center,button' : 'get_model'
    },

	start: function () {
		//this.display_ct();
		//var counter=setInterval(this.display_ct(), 1000);
		mytime=setTimeout(this.display_ct(),1000);
	},
    
    get_model: function() 
    {
    	var employee = document.getElementById('employee_number').value
    	var input = document.getElementById('employee_number')
	    input.value= "";
	    var model = new instance.web.Model("time_control");
	    model.call("search_employee",[[employee]]).done(function (result){

	    });

  	},

    display_ct: function () {
    	document.getElementsByTagName("body")[0].setAttribute("onload", "display_ct();");
	    var strcount
		var x = new Date()
		var x1=x.getMonth() + "/" + x.getDate() + "/" + x.getYear();
		x1 = x1 + " - " + x.getHours( )+ ":" + x.getMinutes() + ":" + x.getSeconds();
		document.getElementById('ct').style.fontSize='30px';
		document.getElementById('ct').style.color='#0030c0';
		document.getElementById('ct').innerHTML = x1;
	//tt=this.display_c();
	},

});
};
