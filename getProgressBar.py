#  coding:utf-8
import json
def getProgressBar(_data):
	result="\r  ["
	_data=json.dumps(_data)
	data=json.loads(_data)
	progress=data["progress"]
	parameter=data["parameter"]
	p=float(progress)/float(parameter)*100
	c=0
	while(c<p):
		result+="="
		c+=10
	result+=">"

	while(c<=100):
		result+=" "
		c+=10
	result+="]"
	return result
