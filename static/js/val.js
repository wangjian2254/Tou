function valSubmit(formid,autosubmit,resultinput){
	var input_arr=[];
	if(formid){
		input_arr=$j('#'+formid+' input');
	}else{
		input_arr=$j('input');
	}
	if(input_arr.length==0){
		return true;
	}
	var input=null;
	var valdict=null;
	for(var i=0;i<input_arr.length;i++){
		input=input_arr[i];
		if(input.attributes.getNamedItem('val')==undefined){
			continue;
		}
        //valdict=$j.parseJSON(input.attributes.getNamedItem('val').value.replace(/'/g,'"'));
		valdict=JSON2.parse(input.attributes.getNamedItem('val').value.replace(/'/g,'"'));
		if(valdict.required&&input.value==''){
			art.dialog({title:'提示',content:valdict.title+' 不能为空！',icon:'warning',lock: true,ok:true});
			return false;
		}else if(valdict.type=='int'&& input.value!=''&&isNaN(input.value)){
			art.dialog({title:'提示',content:valdict.title+' 必须为数字！',icon:'warning',lock: true,ok:true});
			return false;
		}else if(valdict.hasOwnProperty('min')&& input.value!=''&&Number(input.value)<valdict.min){
			art.dialog({title:'提示',content:valdict.title+' 必须大于 '+valdict.min+' ！',icon:'warning',lock: true,ok:true});
			return false;
		}else if(valdict.hasOwnProperty('max')&& input.value!=''&&Number(input.value)>valdict.max){
			art.dialog({title:'提示',content:valdict.title+' 必须小于 '+valdict.max+' ！',icon:'warning',lock: true,ok:true});
			return false;
		}
	}
    if(autosubmit){

        var param=new Object();
        var checkarr='';
        $j('#'+formid+' input').each(function(i,inp){
            var type=$j(inp).attr('type');
            var name=$j(inp).attr('name');
            var value=$j(inp).val();
            if(type=='text'||type=='hidden'||type=='password'){
                if(name){
                    param[name]=value;
                }
            }else if(type=='radio'||type=='checkbox'){
                if(name&&$j(inp).attr('checked')){
                    if(!param[name]){
                        param[name]=''
                    }
                    if(type=='radio'){
                        param[name]+=value;
                    }else{
                        param[name]+=value+',';
                        checkarr.replace(name+',','');
                        checkarr+=name+',';
                    }
                }
            }

        });
        $j('#'+formid+' select').each(function(i,inp){
            var name=$j(inp).attr('name');
            var value=$j(inp).val();
            if(name){
                param[name]=value;
            }
        });
        $j('#'+formid+' textarea').each(function(i,inp){
            var name=$j(inp).attr('name');
            var value=$j(inp).val();
            if(name){
                param[name]=value;
            }
        });
        if(checkarr){
            var car=checkarr.split(',');
            for(var i=0;i<car.length;i++){
                if(param[car[i]]){
                    param[car[i]]=param[car[i]].substring(0,param[car[i]].length-1);
                }
            }
        }
        var url=$j('#'+formid).attr('action');
        var method=$j('#'+formid).attr('method');
        if(method.toUpperCase()=="GET"){
            $j.get(url,param,function(data){
                success(data,resultinput);
            });
        }else{
            $j.post(url,param,function(data){
                success(data,resultinput);
            });
        }

        return false;
    }
	return true;
}
function AjaxError(){
     art.dialog({id:'msg',title:'提示',content:'网络错误，请稍后再试。',icon:'warning',lock: true,ok:true});
}
function success(data,resultid){
            if(typeof data == 'string'){
                data=JSON2.parse(data);
            }
            if(data.success){
                result_alert2("succeed",data.message);
                $j('#'+resultid).val(data.result);
            }else{
                result_alert2("warning",data.message);
            }
}
function result_alert2(type,content)
{
    switch (type)
    {
        case "succeed":
	        {
	        	art.dialog({id:'msg',title:'提示',content:content,icon:'succeed',lock: true,ok:true});
	        }
	        break;
        case "warning":
            {
           	 art.dialog({id:'msg',title:'提示',content:content,icon:'warning',lock: true,ok:true});
        	}
            break;
     }
}
function confirm_alert2(type,content,url)
{
    switch (type)
    {
        case "success":
	        {
	        	art.dialog({title:'提示',content:content,icon:'succeed',lock: true,cancel:true,ok:function(){
                    window.location.href=url;
                }});
	        }
	        break;
        case "warn":
            {
           	 art.dialog({title:'提示',content:content,icon:'warning',lock: true,cancel:true,ok:function(){
           	                     window.location.href=url;
           	                 }});
        	}
            break;
     }
}