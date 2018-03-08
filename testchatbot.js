
function userSend(){
  console.log("User Send A Message")
  var apigClient = apigClientFactory.newClient({
      accessKey: "ASIAIKPKG6OGNPUF7MRQ",
      secretKey: "IMZGHE3v2hiDx+syCoFw+grpgVCbgOb/c++BgwPD",
      sessionToken: "AgoGb3JpZ2luEKH//////////wEaCXVzLXdlc3QtMiKAAl4V/DKul+hg7CMFkDVKF+aUzU7zgiXmkFXe47wadXtNyDZbu+Hzw4H6STV8l7B4N1H4IS1/28g4Uo9tDdTLQWiVJ36yHb3Z+XRjePcEFUcn5TjbGPY7Jbg48hD9vSgJyPAoPSyXYbZ6lZuYJrUHbJOy7c+CrnkVCgGX9KKwrBj7RaF1jKtSmYM25WcUtb1Yag8uz4wnBhX0n2FpL0iC8FbYmYUuiRuUW04sjGKlpsQRyJSiAogBsHHoaR5gDW9HTz0J2wgdrAzW8y1ebEkEmwSixxFuo1g9tPkshIIEIAb9m1JQBgfKiyEWV3qrHj//RHLKTGiuVRw+luQIbXt+BX0qrwUIlv//////////ARAAGgw2ODgwMzE1NzE2ODUiDHsPizDgl8CWMiCKCSqDBV8q09MMqlZz8l/3QRhCF+sy0GBMJxi+oBCmKA0ghzC2TdvaONlQiu1x5qQmEeOvnbOe2tYLeqZxTuRgfoewpeOtxywJGbWpBEDUlP1H4BXAgA9uXxyHPeoyDe74oK4XZYVV5Dm7DkpACOYJqZogiRj+5KwnDC48XvmZkZAFkC44cGRdYcRqG+Q/qWT+5sX+Ru6OjWkXggOpJT3wRUTfttwORfjhUY/NLHoswQnV0AErEIbG06oz0R7puClTuZh4zLRuewaPLMsiREpVsBQMu6hKYPC5p7qgqBj2KQU7Nw8dY5KXOEi5W5rtL6yg7CmHOdgffRuxP0g79kWESdy8bmGN7O+FQ/RkXi6Br1wY5mGrHrD5N0o5SkMFV8G/BNUNuW5GVsTvM7l1Y9KLfYRgLcD10ETh3cE+m1kan0LgN6aVAJymDvt+AAU8DUJE50NRhvz+ERuaJT2pGrN7/rcmoVBNVDtK2mK7ZOjmdQgb6NaIUJRjSpW+CbHwKabRWWeuUN5n9+ul255unSnxUsDnGygSHvzmQOQpnUHAsT3rnRSex2tsgav6is4p/PJuFEhOcg46obxXLuZo9PqMhTUv7pO6UPDQoxvNknZRK0WLhrLNXmA//Yk7t8QmlS5HQTWbfIKJ4LtDlmp121KJ3LYEfL/Nw/XzG1OBOf1VMqxiSMthg+RMv8BAUw6PPjiwa0REM2wLU5WWgGBLiNk0DsJhj1abAGaQIqEQ0J19S8vbe+s+aWl35fUnO6QwNCGKcOe2XLIME0Fa8u4HOdXvJA928PqeB1Cjo/Hgu5EDX32OFc7zTNYZryxKggUAwCO1pCmPcbcn7fCY3XizqzyCINJQ8VppdXwwwaGB1QU=", 
      region: 'us-west-2'
  });
  var params = {'Access-Control-Allow-Origin':'*'};
  var additionalParams ={};
  var body = {
  "messages": [
    {
      "type": "userSendAMessage",
      "unstructured": {
        "id": new Date().getTime(),
        "text": "Hello",
        "timestamp": new Date().getTime()
      }
    }
    ]
  };
  //console.log(body)
  apigClient.chatbotPost(params, body, additionalParams)
    .then(function(result){
      console.log("TEST-Success:")
      console.log(result)
      data = result["data"]
      messages = data["messages"]
      message = messages[0]
      text = message["text"]
      timestamp = message["timestamp"]
      //console.log(text,timestamp)
    }).catch(function(result){
      console.log("TEST-Error:")
      console.log(result)
    });  
}

