//Start Chatting
text1 = "Nice to meet you.";
text2 = "How can I help you?";
text3 = "By the way, my name is Peter."
function addResponseToList(text){
  var node = document.createElement("li"); 
  var font = document.createElement('font');
  font.color = "red";
  var time = new Date().toLocaleTimeString();
  var data =  "Robot: "+ text + "("+ time + ")";
  font.innerText = data;         
  node.appendChild(font);
  document.getElementById("content").appendChild(node);
}
setTimeout("addResponseToList(text1)",1000);
setTimeout("addResponseToList(text2)",2000);
setTimeout("addResponseToList(text3)",3000);


function userSend(){
  console.log("User Send A Message")
  var node = document.createElement("li"); 
  var font = document.createElement('font');
  font.color = "Chartreuse"
  var text = document.getElementById("question").value 
  document.getElementById("question").value = ""
  var time = new Date().toLocaleTimeString();
  var data =  "You: "+ text + "("+ time + ")";
  //var textnode = document.createTextNode(data);
  font.innerText = data;         
  node.appendChild(font);                              
  document.getElementById("content").appendChild(node);

  if(AWS.config.credentials){
    var apigClient = apigClientFactory.newClient({
      accessKey: AWS.config.credentials.data.Credentials.AccessKeyId,
      secretKey: AWS.config.credentials.data.Credentials.SecretKey,
      sessionToken: AWS.config.credentials.data.Credentials.SessionToken, 
      region: 'us-west-2'
  });}
  else{
    var apigClient = apigClientFactory.newClient();
  }
  var params = {'Access-Control-Allow-Origin':'*'};
  var additionalParams ={};
  var body = {
  "messages": [
    {
      "type": "userSendAMessage",
      "unstructured": {
        "id": new Date().getTime(),
        "text": text,
        "timestamp": new Date().getTime()
      }
    }
    ]
  };
  apigClient.chatbotPost(params, body, additionalParams)
    .then(function(result){
      console.log("Success:")
      console.log(result)
      data = result["data"]
      messages = data["messages"]
      message = messages[0]
      text = message["text"]
      timestamp = message["timestamp"]
      addResponseToList(text)
      //console.log(text,timestamp)
    }).catch(function(result){
      console.log("Error:")
      console.log(result)
      addResponseToList("Oops, it seems you are not authorized.")
    });  
}