import sys
import frida

def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)
 
 
PACKAGE_NAME = "org.thoughtcrime.securesms"


jscode = """
    Java.perform(function(){
       // var context = Java.use("android.content.Context");
       // console.log(context.databaseList());
        console.log("[+]in app");
        var sqlopener = Java.use("org.thoughtcrime.securesms.database.helpers.SQLCipherOpenHelper");
       // sqlopener.onCreate.implementation = function(arg){
        //    console.log("----------------------");
            //console.log("context : "+ ctx);
        //    console.log("arg: " + arg);
       // }
      /*  sqlopener.getWritableDatabase.implementation = function(str){
            console.log("----------------------------------------");
            var ret = this.getWritableDatabase();
            console.log(str);
        }*/
        var Msenderf = Java.use("org.whispersystems.signalservice.api.SignalServiceMessageSender");
        var Msenderc = Msenderf.sendMessage.implementation = function(){
            console.log("in message send");
        }

    })
"""


try:
    device = frida.get_usb_device(timeout=10)
    pid = device.spawn([PACKAGE_NAME]) 
    print("App is starting ... pid : {}".format(pid))
    process = device.attach(pid)
    device.resume(pid)
    script = process.create_script(jscode)
    script.on('message',on_message)
    print('[*] Running Frida')
    script.load()
    sys.stdin.read()
except Exception as e:
    print(e)
