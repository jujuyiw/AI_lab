from flask import Flask,request,jsonify
import csv

app=Flask(__name__)

recommandation_data=''

@app.route('/recommand',method=['POST'])
def recommand():
    #
    data=request.get_json()
    
    if not data or 'tags' not in data:
        return jsonify({"error":"請提供tags欄位"}),400
    
    tags=data['tags']
    if not isinstance(tags,list):
        return jsonify({"error":"tags必須是list"}),400
    
    results=[]
    for tag in tags:
        if tag in recommandation_data:
            result.extend(recommandation_data[tag])
            
    results=list(set(result))[:5]
    
    return jsonify({
        "input_tag":tags,
        "recommendations":results
    })
    
if __name__=='__main__':
    app.run(debug=True)