openerp.time_control = function (instance) {
instance.web.client_actions.add('example.action', 'instance.time_control.Action');
instance.time_control.Action = instance.web.Widget.extend({
    template: 'time_control.action',
    events: {
            'click .oe_time_control_timer button': 'get_model'
    },

	start: function () {
		this._watch = setInterval(this.proxy('display_ct'), 1000);
		var inp = document.getElementById('employee_number');
		inp.setAttribute("type", "password");
		//mytime=setTimeout(this.display_ct(),1000);
	},
    
    get_model: function() 
    {
    	var employee = document.getElementById('employee_number').value
    	var input = document.getElementById('employee_number')
	    input.value= "";
	    var model = new instance.web.Model("time_control");
	    model.call("search_employee",[[employee]]).done(function (result){
	    	alert(result)
	    });

  	},

    display_ct: function () {
    	document.getElementsByTagName("body")[0].setAttribute("onload", "display_ct();");
	    var strcount
		var x = new Date()
		var x1=x.getDate() + "/" + (x.getMonth()+1) + "/" + x.getFullYear();
		x1 = x1 + " - " + x.getHours( )+ ":" + x.getMinutes() + ":" + x.getSeconds();
		var doc = document.getElementById('ct');
		if (doc != null) {
			doc.innerHTML = x1;
		}
	},

});
};
